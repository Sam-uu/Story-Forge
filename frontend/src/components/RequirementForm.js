import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { generateAll } from "../api/client";
import "../styles/RequirementForm.css";

export default function RequirementForm({ onResult, onLoading }) {
  const [text, setText] = useState("");

  const mutation = useMutation({
    mutationFn: generateAll,
    onSuccess: (data) => {
      onResult(data);
      onLoading(false);
    },
    onError: () => {
      onLoading(false);
    },
    onMutate: () => {
      onLoading(true);
    },
  });

  return (
    <div className="form-container">
      <textarea
        className="requirement-input"
        rows={4}
        placeholder="✨ Describe your requirement here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button
        onClick={() => mutation.mutate(text)}
        disabled={mutation.isLoading || !text.trim()}
        className="generate-btn"
      >
        Generate
      </button>
    </div>
  );
}