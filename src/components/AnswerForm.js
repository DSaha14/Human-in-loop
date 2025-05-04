import React, { useState } from "react";
import axios from "axios";
import { Button, TextField, Box } from "@mui/material";

function AnswerForm({ requestId, onAnswered }) {
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const submitAnswer = async () => {
    if (!answer.trim()) return;
    setLoading(true);
    try {
      await axios.post("http://localhost:8000/answer", {
        request_id: requestId,
        answer: answer.trim(),
      });
      onAnswered(); // Notify parent to refresh list
      setAnswer("");
    } catch (error) {
      console.error("Failed to submit answer", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ mt: 2, display: "flex", gap: 1 }}>
      <TextField
        fullWidth
        variant="outlined"
        size="small"
        placeholder="Type your answer..."
        value={answer}
        onChange={(e) => setAnswer(e.target.value)}
      />
      <Button
        variant="contained"
        onClick={submitAnswer}
        disabled={loading}
      >
        Submit
      </Button>
    </Box>
  );
}

export default AnswerForm;
