import paho.mqtt.client as mqtt

HOST = "192.168.1.243"
PORT = 1883


def on_connect(client, userdata, flags, rc):
    print("Connesso con codice " + str(rc))
    client.subscribe("$SYS/#")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('192.168.1.246', PORT, 60)

client.loop_forever()
