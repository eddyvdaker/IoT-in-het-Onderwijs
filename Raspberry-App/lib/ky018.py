import RPi.GPIO as GPIO, time, os

pin = 23
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.LOW)
time.sleep(0.1)

def RCtime():
	reading = 0
	GPIO.setup(pin, GPIO.IN)
	# This takes about 1 millisecond per loop cycle
	while (GPIO.input(pin) == GPIO.LOW):
		reading += 1
	return reading

while True:
	print(RCtime())     # Read RC timing using pin #18
