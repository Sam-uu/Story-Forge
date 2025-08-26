import "../styles/LoadingOverlay.css";

export default function LoadingOverlay({ show }) {
  if (!show) return null;

  return (
    <div className="loading-overlay">
      <div className="spinner"></div>
      <p className="loading-text">Loading...</p>
    </div>
  );
}
