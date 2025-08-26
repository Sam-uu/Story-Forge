import { useEffect, useState } from "react";
import { getCards, deleteCard } from "../api/client";
import { Trash2 } from "lucide-react";
import "../styles/SavedCards.css";

export default function SavedCards() {
  const [cards, setCards] = useState([]);
  const [expanded, setExpanded] = useState(null);

  const fetchCards = async () => {
    const data = await getCards();
    setCards(data);
  };

  const handleDelete = async (id) => {
    await deleteCard(id);
    fetchCards();
  };

  useEffect(() => {
    fetchCards();
    const handler = () => fetchCards();
    window.addEventListener("cardSaved", handler);
    return () => window.removeEventListener("cardSaved", handler);
  }, []);

  return (
    <div className="saved-cards">
      {cards.map((c) => (
        <div
            key={c.id}
            className={`saved-card ${expanded === c.id ? "expanded" : ""}`}
            onClick={() => setExpanded(expanded === c.id ? null : c.id)}
        >
        <div
            className={`intent-pill ${c.intent === "Feature" ? "feature" : "bug"}`}
        >
            {c.intent}
        </div>
        <div className="user-story">{c.user_story}</div>

        {expanded === c.id && (
            <div className="details">
            <hr className="divider" />
            <ul className="criteria-list">
                {c.acceptance_criteria.map((ac, i) => (
                <li key={i}>{ac}</li>
                ))}
            </ul>

            <div className="actions">
                <button
                    className="delete-btn"
                    onClick={(e) => {
                    e.stopPropagation();
                    handleDelete(c.id);
                    }}
                >
                    <Trash2 size={16} /> Delete
                </button>
            </div>
            </div>
        )}
        </div>
      ))}
    </div>
  );
}
