const API_BASE = "http://localhost:8000"; // change this to match your backend

export async function fetchPendingRequests() {
  const res = await fetch(`${API_BASE}/requests`);
  return res.json();
}

export async function submitAnswer(requestId, answer) {
  const res = await fetch(`${API_BASE}/requests/${requestId}/answer`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ answer }),
  });
  return res.json();
}

export async function fetchKnowledgeBase() {
  const res = await fetch(`${API_BASE}/knowledge`);
  return res.json();
}
