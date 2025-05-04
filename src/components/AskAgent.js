import { useState } from "react";
import axios from "axios";

export default function AskAgent() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const askAgent = async () => {
    setLoading(true);
    setResponse("");

    try {
      const res = await axios.get("http://localhost:8000/ask", {
        params: { q: question },
      });

      if (res.data.answer) {
        setResponse(`🧠 AI: ${res.data.answer}`);
      } else if (res.data.request_id) {
        setResponse("🤖 AI: I’m not sure, Let me check with my supervisor and get back to you....");
      } else {
        setResponse("⚠️ Unexpected response.");
      }
    } catch (err) {
      setResponse("❌ Error: Could not contact backend.");
    }

    setLoading(false);
  };

  return (
    <div className="p-4 max-w-xl mx-auto border rounded space-y-4">
      <h2 className="text-lg font-semibold">Ask the Agent</h2>
      <input
        className="border p-2 w-full"
        placeholder="Ask a question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button
        onClick={askAgent}
        className="bg-blue-600 text-white px-4 py-2 rounded"
        disabled={loading}
      >
        {loading ? "Asking..." : "Ask"}
      </button>
      <div>{response}</div>
    </div>
  );
}
