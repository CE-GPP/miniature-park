// Require the MQTT library
const mqtt = require("mqtt");
//import {connect} from "mqtt";

// Connect to the MQTT Broker
const client = connect('mqtt://mqtt.cetools.org')

var mqttResponse;

// Subscribe to a topic
client.on('connect', () => {
  client.subscribe('student/ucfnnbx/QEOP/buttonReturn', (error) => {
    if (!error) {
      console.log("Subscribed")
      // console.log(`Subscribed to ${topic_name}`);
    }
  });
});

// Handle incoming messages
client.on('message', function(topic, message) {
  console.log(message.toString())// Convert the message buffer to a string
  mqttResponse = message.toJSON
  //client.end()
  //console.log(`Received message`);

  // Do something with the payload

});

// Handle connection errors
client.on('error', (error) => {
  console.log(`Error: ${error}`);
});