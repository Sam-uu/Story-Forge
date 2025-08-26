import { useEffect, useState } from "react";
import { Moon, Sun } from "lucide-react";
import "../styles/DarkModeToggle.css";

export default function DarkModeToggle() {
  const [dark, setDark] = useState(() =>
    window.matchMedia("(prefers-color-scheme: dark)").matches
  );

  useEffect(() => {
    if (dark) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [dark]);

  return (
    <button
      onClick={() => setDark(!dark)}
      className="dark-toggle"
      aria-label="Toggle Dark Mode"
    >
      {dark ? <Sun size={20} /> : <Moon size={20} />}
    </button>
  );
}
