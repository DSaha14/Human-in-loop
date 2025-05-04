import React, { useEffect, useState } from "react";
import { Room } from "livekit-client";
import { Button, CircularProgress, Typography } from "@mui/material";

const VideoRoom = () => {
  const [connected, setConnected] = useState(false);
  const [room, setRoom] = useState(null);

  useEffect(() => {
    const newRoom = new Room(); // move this outside for access in cleanup

    const connectToRoom = async () => {
      try {
        const res = await fetch("http://localhost:8000/get-token?identity=supervisor");
        const data = await res.json();

        await newRoom.connect("ws://localhost:7880", data.token);

        newRoom.on("participantConnected", (participant) => {
          console.log("Participant joined:", participant.identity);
        });

        setRoom(newRoom);
        setConnected(true);
      } catch (err) {
        console.error("Failed to connect to LiveKit room:", err);
      }
    };

    connectToRoom();

    return () => {
      if (newRoom && newRoom.connected) {
        newRoom.disconnect();
      }
    };
  }, []);

  if (!connected) return <CircularProgress />;

  return (
    <div>
      <Typography variant="h5" gutterBottom>
        Live Help Room
      </Typography>
      <Typography>You're connected as Supervisor</Typography>
      <Button
        variant="contained"
        color="error"
        onClick={() => {
          if (room) {
            room.disconnect();
            setConnected(false);
          }
        }}
      >
        Leave Room
      </Button>
    </div>
  );
};

export default VideoRoom;
