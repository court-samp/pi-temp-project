import Adafruit_DHT
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import RPi.GPIO as GPIO
import json


DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

SHADOW_CLIENT = "myShadowClient"

HOST_NAME = "as7xdsyst39mq-ats.iot.us-east-1.amazonaws.com"

ROOT_CA = "rootca.pem"

PRIVATE_KEY = "af717b6c0f-private.pem.key"

CERT_FILE = "af717b6c0f-certificate.pem.crt.txt"

SHADOW_HANDLER = "RaspberryPi"

# Automatically called whenever the shadow is updated.
def myShadowUpdateCallback(payload, responseStatus, token):
  print()
  print('UPDATE: $aws/things/' + SHADOW_HANDLER +
    '/shadow/update/#')
  print("payload = " + payload)
  print("responseStatus = " + responseStatus)
  print("token = " + token)

# Create, configure, and connect a shadow client.
myShadowClient = AWSIoTMQTTShadowClient(SHADOW_CLIENT)
myShadowClient.configureEndpoint(HOST_NAME, 8883)
myShadowClient.configureCredentials(ROOT_CA, PRIVATE_KEY,
  CERT_FILE)
myShadowClient.configureConnectDisconnectTimeout(10)
myShadowClient.configureMQTTOperationTimeout(5)
myShadowClient.connect()

# Create a programmatic representation of the shadow.
myDeviceShadow = myShadowClient.createShadowHandlerWithName(
  SHADOW_HANDLER, True)

# Represents the GPIO21 pin on the Raspberry Pi.
channel = 4

# Use the GPIO BCM pin numbering scheme.
GPIO.setmode(GPIO.BCM)

# Receive input signals through the pin.
GPIO.setup(channel, GPIO.IN)


while True:
	humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
	if humidity is not None and temperature is not None:
		myDeviceShadow.shadowUpdate(
		'{"state":{"reported":{"temperature":"ok"}}}',
		myShadowUpdateCallback, 5)
	else:
		myDeviceShadow.shadowUpdate(
		'{"state":{"reported":{"temperature":"missing"}}}',
		myShadowUpdateCallback, 5)

	time.sleep(3);

GPIO.cleanup()
