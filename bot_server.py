import json
import subprocess
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)
CORS(app)  # make requests to the backend

# Load the JSON data
def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Compute semantic similarity and return top 3 relevant entries
def find_relevant_entries(question, data, model, top_k=3):
    json_questions = [entry['question'] for entry in data]
    question_embedding = model.encode(question, convert_to_tensor=True)
    json_embeddings = model.encode(json_questions, convert_to_tensor=True)
    similarities = util.cos_sim(question_embedding, json_embeddings)[0]
    similarities = similarities.cpu().numpy()
    top_k_indices = np.argsort(similarities)[-top_k:][::-1] #it first sorts similarities in an ascending order
    return [data[idx] for idx in top_k_indices]

# Construct prompt with relevant context
def construct_prompt(question, relevant_entries):
    prompt = f"Question: {question}\n\nRelevant Information:\n"
    for entry in relevant_entries:
        prompt += f"Q: {entry['question']}\nA: {entry['answer']}\n\n"
    prompt += "Based on the provided information, answer the question concisely and accurately and don't mention anything related to having a provided data or data scope."
    return prompt

# Call Gemini API using curl
def call_gemini_api(prompt, api_key):
    curl_command = [
        'curl', '-X', 'POST',
        f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps({
            'contents': [{
                'parts': [{'text': prompt}]
            }]
        }, ensure_ascii=False).encode('utf-8')
    ]
    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, encoding='utf-8', check=True)
        response = json.loads(result.stdout)
        return response['candidates'][0]['content']['parts'][0]['text']
    except subprocess.CalledProcessError as e:
        return f"Error calling Gemini API: {e.stderr}"
    except (KeyError, IndexError) as e:
        return f"Error parsing Gemini API response: {str(e)}"

# Main function to process question
def answer_question(question, json_file_path, api_key, top_k=3):
    data = load_json_data(json_file_path)
    model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
    relevant_entries = find_relevant_entries(question, data, model, top_k)
    prompt = construct_prompt(question, relevant_entries)
    return call_gemini_api(prompt, api_key)

@app.route('/answer', methods=['POST'])
def get_answer():
    data = request.get_json()
    question = data.get('question')
    api_key = data.get('api_key')  
    if not question:
        return jsonify({"error": "Question is required"}), 400

    try:
        # Process the question using the answer_question function
        JSON_FILE_PATH = "data.json"  
        answer = answer_question(question, JSON_FILE_PATH, api_key)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": f"Failed to generate answer: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)