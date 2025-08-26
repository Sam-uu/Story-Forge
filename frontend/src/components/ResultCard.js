import { saveCard } from "../api/client";
import "../styles/ResultCard.css";
import { Save } from "lucide-react";

export default function ResultCard({ result }) {
  if (!result) return null;

  const { intent, user_story, acceptance_criteria } = result;
  const intentClass = intent === "Feature" ? "intent-pill feature" : "intent-pill bug";

    const handleSave = async () => {
    await saveCard({
      intent,
      user_story,
      acceptance_criteria,
    });
    const event = new Event("cardSaved");
    window.dispatchEvent(event);
  };

  return (
    <div className="result-card">
      <div className={intentClass}>{intent}</div>

      <h2 className="card-title">User Story</h2>
      <p className="user-story">{user_story}</p>

      <div className="divider"></div>

      <h3 className="criteria-title">Acceptance Criteria</h3>
      <ul className="criteria-list">
        {acceptance_criteria.map((c, i) => (
          <li key={i}>{c}</li>
        ))}
      </ul>
      
      <div className="actions">
        <button
            className="save-btn"
            onClick={handleSave}
        >
          <Save size={16} /> Save
        </button>
      </div>
    </div>
  );
}
