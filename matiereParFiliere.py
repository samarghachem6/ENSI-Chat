from bs4 import BeautifulSoup
import requests
import json
import pdfplumber

url = "https://ensi.rnu.tn/fra/s1270/pages/438/Ing%C3%A9nieur"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

pdf_infos = soup.find_all("a", class_="downloadLink-blue-round")


def subjects_extraction(pdf_path, page_num, col=1):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num]
        table = page.extract_table()
        column = []
        for row in table[4:]:  
            if row[col] and row[col].strip():  
                column.append(f"{row[col].strip()}: {row[2]}")

    
        filtered_column = [item for item in column if  "Complementary Module" not in item]
        return [item.replace("\n", " ").strip() for item in filtered_column if item]


filiere = []
titles = ["Génie Logiciel", "Intelligence Artificielle", "Data Science for Computer Vision", "Ingénierie pour la finance", "IOT ", "Systèmes et logiciels embarqués"]

for title,link in zip(titles, pdf_infos):
    pdf_url = "https://ensi.rnu.tn" + link["href"]
    pdf_response = requests.get(pdf_url)
    with open("matieres.pdf", "wb") as f:
        f.write(pdf_response.content)
    subjects = ", ".join(subjects_extraction("matieres.pdf",0))

    filiere.append({
        "question": f"Quelles sont les matières de la filière {title}?",
        "answer": subjects
    })



# Save to JSON
with open("matiere_filiere.json", "w", encoding="utf-8") as f:
    json.dump(filiere, f, indent=2, ensure_ascii=False)
