import paho.mqtt.client as mqtt

def hexToRGBA(hex, alpha = 255):
    red = (hex >> 16) & 0xFF
    green = (hex >> 8) & 0xFF
    blue = hex & 0xFF
    return (red, green, blue, alpha)

def publishMQTT(broker_address, broker_port,broker_username, broker_password,topic, json_str):
    # Define the MQTT broker credentials
    broker_port = 1884
    broker_username = "student"

    # Connect to the MQTT broker with credentials
    client = mqtt.Client()
    client.username_pw_set(broker_username, broker_password)
    client.connect(broker_address, broker_port)

    # Publish the data to the MQTT topic
    result = client.publish(topic, json_str)

    # Disconnect from the MQTT broker
    client.disconnect()

    return result