import React, { useEffect, useState } from "react";
import {
  Typography,
  Paper,
  Box,
  CircularProgress,
  Divider,
} from "@mui/material";
import { fetchKnowledgeBase } from "../api/api";

const KnowledgeBase = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const res = await fetchKnowledgeBase();
        console.log("Knowledge Base Response:", res);
        const parsed = Array.isArray(res)
          ? res
          : Array.isArray(res.knowledge)
          ? res.knowledge
          : [];
        setData(parsed);
      } catch (err) {
        console.error("Failed to fetch knowledge base:", err);
        setData([]);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <CircularProgress />;

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Learned Knowledge Base
      </Typography>
      {data.length === 0 && <Typography>No learned answers yet.</Typography>}
      {data.map((item, idx) => (
        <Paper key={idx} sx={{ p: 2, mb: 2 }}>
          <Typography><strong>Q:</strong> {item.question}</Typography>
          <Divider sx={{ my: 1 }} />
          <Typography><strong>A:</strong> {item.answer}</Typography>
        </Paper>
      ))}
    </Box>
  );
};

export default KnowledgeBase;
