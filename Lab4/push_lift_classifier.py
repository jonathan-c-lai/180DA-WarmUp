import paho.mqtt.client as mqtt
import time

# used code that the professor/TA posted
# modified to read in IMU data and then classify whether or not
# the user made a push or lift motion

# classifying push in the -Y direction
PUSH_THRESH = -1500
# lift in the Z direction
LIFT_THRESH = -800

accel = [0, 0, 0]
gyro = [0, 0, 0]

def classify_push(new_ay):
    # if value of y is registered very strongly, stronger than set constant, then classified as push
    if (new_ay < PUSH_THRESH):
        print("Push Detected")

def classify_lift(new_az):
    # if value of z is registered very strongly, stronger than set constant, then classified as push
    if (new_az < LIFT_THRESH):
        print("Lift Detected")

# callback definitions
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("ece180jonimu/test", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')
# The default message callback.
def on_message(client, userdata, message):
    global accel
    global gyro

    received_msg = str(message.payload)
    # print('Received message: "' + received_msg)
    space_separated = received_msg.split()
    
    ax = space_separated[0][2:] # ax
    ay = space_separated[1] # ay
    az = space_separated[2] # az

    gx = space_separated[3] # gx
    gy = space_separated[4] # gy
    gz = space_separated[5][:-1] # gz

    classify_push(float(ay))
    classify_lift(float(az))
    
    accel[0] = ax
    accel[1] = ay
    accel[2] = az

    gyro[0] = gx
    gyro[1] = gy
    gyro[2] = gz
    # print("ax, ay, az, gx, gy, gz", accel[0], accel[1], accel[2], gyro[0], gyro[1], gyro[2])

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
    pass # do your non-blocked other stuff here, like receive IMU data or something.
# use subscribe() to subscribe to a topic and receive messages.
# use publish() to publish messages to the broker.
# use disconnect() to disconnect from the broker.
client.loop_stop()
client.disconnect()
