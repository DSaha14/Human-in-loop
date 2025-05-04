// Refactored PendingRequests.js
import React, { useEffect, useState } from "react";
import {
  Typography,
  Paper,
  TextField,
  Button,
  Box,
  CircularProgress,
  List,
  ListItem,
  Divider,
} from "@mui/material";
import { fetchPendingRequests, submitAnswer } from "../api/api";

const PendingRequests = () => {
  const [requests, setRequests] = useState([]);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchPendingRequests();
        console.log("Fetched requests:", data);

        const parsedRequests = Array.isArray(data)
          ? data
          : Array.isArray(data.requests)
          ? data.requests
          : [];

        setRequests(parsedRequests.filter((req) => req.status === "pending"));
      } catch (error) {
        console.error("Failed to load requests:", error);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const handleSubmit = async (id) => {
    if (!answers[id]) return;
    try {
      await submitAnswer(id, answers[id]);
      setRequests((prev) => prev.filter((req) => req.id !== id));
    } catch (error) {
      console.error("Submit failed:", error);
    }
  };

  if (loading) return <CircularProgress />;

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Pending Help Requests
      </Typography>
      {requests.length === 0 ? (
        <Typography>No pending requests.</Typography>
      ) : (
        requests.map((req) => (
          <Paper key={req.id} sx={{ p: 2, mb: 2 }}>
            <Typography><strong>Question:</strong> {req.question}</Typography>

            <Typography variant="subtitle2" sx={{ mt: 2 }}>
              Activity Log:
            </Typography>
            <List dense>
              {(req.logs || []).map((log, i) => (
                <ListItem key={i} sx={{ pl: 0 }}>
                  • {log}
                </ListItem>
              ))}
            </List>

            <Divider sx={{ my: 1 }} />

            <TextField
              fullWidth
              label="Supervisor Answer"
              value={answers[req.id] || ""}
              onChange={(e) =>
                setAnswers({ ...answers, [req.id]: e.target.value })
              }
              sx={{ mt: 2 }}
            />
            <Button
              variant="contained"
              onClick={() => handleSubmit(req.id)}
              sx={{ mt: 1 }}
            >
              Submit Answer
            </Button>
          </Paper>
        ))
      )}
    </Box>
  );
};

export default PendingRequests;
