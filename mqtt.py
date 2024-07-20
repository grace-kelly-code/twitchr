import paho.mqtt.client as paho
from paho import mqtt
import dotenv
import os
from sounds import play_sound
import json
from sense_hat import SenseHat
from sense import draw_alert, draw_message
sense = SenseHat()

dotenv.load_dotenv(override=True)


def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    print(str(msg.payload))
    if "type" in payload:
        if payload["type"] == "cat":
            play_sound("bark")
            draw_alert(sense, "cat", "cat seen!!")
        elif payload["type"] == "bird":
            draw_alert(sense, "bird", "bird seen")
        elif payload["type"] == "play_sound":
            draw_message(sense, "playing {}...".format(payload["sound"]))
            play_sound(payload["sound"])
    elif "weather" in payload:
        current_weather = payload["weather"].lower()
        draw_alert(sense, current_weather, current_weather)


if __name__ == '__main__':
    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set(
        os.environ['MQTT_USERNAME'], os.environ['MQTT_PASSWORD'])
    # connect to MQTT
    client.connect(os.environ["MQTT_HOST"], 8883)

    client.on_subscribe = on_subscribe
    client.on_message = on_message

    # subscribe to topic
    client.subscribe("twitchr", qos=1)
    client.loop_forever()
