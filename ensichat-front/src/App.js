import { useState } from "react";
import axios from "axios";
import "./App.css";
import { FaClockRotateLeft } from "react-icons/fa6";
import { BsQuestionCircle } from "react-icons/bs";
import { RiChat1Line } from "react-icons/ri";
import { LuSend } from "react-icons/lu";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const GEMINI_API_KEY = "AIzaSyDwz34pykzm4f0QxpN8q7OMXVOmT4RMfy8";

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) {
      setError("Veuillez fournir une question.");
      return;
    }
    setLoading(true);
    setError("");
    setAnswer("");

    try {
      const response = await axios.post("http://localhost:5000/answer", {
        question,
        api_key: GEMINI_API_KEY,
      });
      const newAnswer = response.data.answer;
      setAnswer(newAnswer);
      // Store both question and answer in history
      setHistory([...history, { question, answer: newAnswer }]);
      setQuestion("");
    } catch (err) {
      setError(
        err.response?.data?.error ||
          "Échec de la récupération de la réponse du serveur."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header>
        <div>
          <img src="log-modified.png" alt="ENSI Logo" />
        </div>
        <h1>ENSIChat</h1>
        <p>
          Posez vos questions sur l'École Nationale des Sciences de
          l'Informatique
        </p>
      </header>

      <div className="main-content">
        {/* Question Input Section */}
        <div className="card">
          <h2>
            <BsQuestionCircle className="section-icon" />
            Posez votre question sur ENSI
          </h2>
          <div className="input-group">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Quelles sont les filières disponibles à l’ENSI ?"
            />
            <button onClick={handleSubmit} disabled={loading}>
              <LuSend className="send-icon" />
              <span>{loading ? "Chargement..." : "Demander"}</span>
            </button>
          </div>
          {error && <div className="error">{error}</div>}
          {answer && (
            <div className="answer">
              <h3>
                <RiChat1Line className="section-icon" />
                Réponse :
              </h3>
              <p>{answer}</p>
            </div>
          )}
        </div>

        {/* History Section */}
        <div className="card">
          <h2>
            <FaClockRotateLeft className="section-icon" />
            Historique des questions
          </h2>
          {history.length > 0 ? (
            <ul className="history-list">
              {history.map((item, index) => (
                <li key={index} className="history-item">
                  <div className="history-item-question">
                    <span>📜</span>
                    <span>{item.question}</span>
                  </div>
                  <div className="history-item-answer">{item.answer}</div>
                </li>
              ))}
            </ul>
          ) : (
            <p className="history-empty">
              Aucune question posée pour le moment.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
