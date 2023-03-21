const express = require("express");
const mqtt = require("mqtt");
const cors = require('cors');
const app = express();
// Serve the frontend
app.use(cors());
app.use(express.static("public"));
// MQTT client
const mqttClient = mqtt.connect("mqtt://mqtt.cetools.org");
let latestMessage = "";
mqttClient.on("connect", () => {
  console.log("Connected to the MQTT broker");
  mqttClient.subscribe("student/ucfnimx/QEOPMap/+");
});
mqttClient.on("message", (topic, message) => {
  console.log(`Received message: ${message.toString()} on topic: ${topic}`);
  message = JSON.parse(message)
  latestMessage = {topic, message};
});
// Endpoint to fetch the latest message
app.get("/latest-message", (req, res) => {
  res.json(latestMessage);
});
// Start the HTTP server
const port = process.env.PORT || 3000;
// const port = 5501
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});


