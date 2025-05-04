import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import { AppBar, Toolbar, Typography, Button, Container } from "@mui/material";
import PendingRequests from "./components/PendingRequests";
import KnowledgeBase from "./components/KnowledgeBase";
import VideoRoom from "./components/VideoRoom";


function App() {
  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Human-in-the-Loop Supervisor
          </Typography>
          <Button color="inherit" component={Link} to="/">
            Pending Requests
          </Button>
          <Button color="inherit" component={Link} to="/knowledge">
            Knowledge Base
          </Button>
          <Button color="inherit" component={Link} to="/room">
            Video Room
          </Button>

        </Toolbar>
      </AppBar>
      <Container sx={{ marginTop: 4 }}>
        <Routes>
          <Route path="/" element={<PendingRequests />} />
          <Route path="/knowledge" element={<KnowledgeBase />} />
          <Route path="/room" element={<VideoRoom />} />
        </Routes>
      </Container>
    </div>
  );
}

export default App;
