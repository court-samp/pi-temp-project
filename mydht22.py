import Adafruit_DHT
import time

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

while True:
	humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
	if humidity is not None and temperature is not None:
		temperature = temperature * 1.8 +32
		print("Temp={0:0.1f}F Humidity={1:0.1f}%".format(temperature, humidity))
	else:
		print("Sensor failure. Check wiring.");
	time.sleep(3);
