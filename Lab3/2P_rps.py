import paho.mqtt.client as mqtt
import time

# used code that the professor/TA posted, modified to be a player in rps
player_num = 2
counter = 1
ROUND_START = 9
RPS_RESULT = 8

# callback definitions
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("ece180/test/player"+str(player_num), qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')
# The default message callback.
def on_message(client, userdata, message):
    global counter

    if(int(message.payload) == ROUND_START):
        print('Received message: "' + str(message.payload) + '" on topic "' +
            message.topic + '" with QoS ' + str(message.qos))

        my_input = input('Choose r, p, or s, for Rock, Paper, or Scissors\n')
       
        client.publish("ece180/test/player"+str(player_num), my_input, qos=1)
        print('Published message: ', my_input)

        time.sleep(2)
    elif(int(message.payload) == RPS_RESULT):
        print('Received message: "' + str(message.payload) + '" on topic "' +
            message.topic + '" with QoS ' + str(message.qos))
        time.sleep(2)

# 1. create a client instance.
client = mqtt.Client()
# add additional client options (security, certifications, etc.)
# add callbacks to client.
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
# 2. connect to a broker using one of the connect*() functions.
# client.connect_async("test.mosquitto.org")
client.connect_async('mqtt.eclipseprojects.io')
# client.connect("test.mosquitto.org", 1883, 60)
# client.connect("mqtt.eclipse.org")
# 3. call one of the loop*() functions to maintain network traffic flow with the broker.
client.loop_start()
# client.loop_forever()

while True: # perhaps add a stopping condition using some break or something
    # once we receive message that round starts
    # take in input from user
    # publish input including our player number
    # wait for result message to come in, print it
    # update score
    # repeat
    pass # do your non-blocked other stuff here, like receive IMU data or something.
# use subscribe() to subscribe to a topic and receive messages.
# use publish() to publish messages to the broker.
# use disconnect() to disconnect from the broker.
client.loop_stop()
client.disconnect()
