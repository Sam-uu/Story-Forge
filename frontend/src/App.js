import { useState } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import RequirementForm from "./components/RequirementForm";
import ResultCard from "./components/ResultCard";
import DarkModeToggle from "./components/DarkModeToggle";
import LoadingOverlay from "./components/LoadingOverlay";
import "./App.css";
import SavedCards from "./components/SavedCards";

const queryClient = new QueryClient();

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100 
                      dark:from-gray-950 dark:via-gray-900 dark:to-gray-800 
                      transition-colors duration-300 relative">

        <LoadingOverlay show={loading} />

        <div className="absolute top-6 right-6">
          <DarkModeToggle />
        </div>

        <header className="flex items-center justify-center pt-20 pb-12">
          <h1 className="app-title">Story Forge: Agile Assistant</h1>
        </header>

        <main>
          <RequirementForm onResult={setResult} onLoading={setLoading} />
          <ResultCard result={result} />
          <SavedCards />
        </main>
      </div>
    </QueryClientProvider>
  );
}
