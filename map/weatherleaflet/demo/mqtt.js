// Require the MQTT library
// const mqtt = require('mqtt');
import mqtt from "mqtt";
// Connect to the MQTT Broker
const client = mqtt.connect('mqtt://mqtt.cetools.org', { //mqtt.cetools.org
  // Set the username and password if your broker require authentication
  username: 'student',
  password: 'ce2021-mqtt-forget-whale',
});
// Subscribe to a topic
client.on('connect', () => {
  client.subscribe('student/ucfnnbx/QEOP/button', (error) => {
    if (!error) {
      console.log(`Subscribed to ${'<topic_name>'}`);
    }
  });
});
// Handle incoming messages
client.on('message', (topic, message) => {
  // Convert the message buffer to a string
  const payload = message.toString();
  // Do something with the payload
  console.log(`Received message: ${payload} on topic: ${topic}`);
});
// Handle connection errors
client.on('error', (error) => {
  console.log(`Error: ${error}`);
});