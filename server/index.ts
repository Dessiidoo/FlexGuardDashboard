import express from "express";
import bodyParser from "body-parser";
import { predictThreat } from "../ai/predictor.js";
import { logEvent } from "../utils/logger.js";

const app = express();
app.use(bodyParser.json());

const PORT = process.env.PORT || 3000;

// Health check
app.get("/health", (_req, res) => {
  res.json({ status: "Flex 2.0 operational" });
});

// Endpoint for sending sensor data
app.post("/sensor-data", async (req, res) => {
  const { heartRate, motion, environment } = req.body;
  try {
    const threat = await predictThreat({ heartRate, motion, environment });
    logEvent({ heartRate, motion, environment, threat });
    res.json({ threat });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`Flex 2.0 server running on port ${PORT}`);
});
