import RPi.GPIO as GPIO
import time

encoderPinA = 23
encoderPinB = 24
buttonPin = 25

encoderValue = 0
lastEncoded = 0

def read_encoder_value():
    global encoderValue
    return encoderValue // 4

def is_button_push_down():
    if not GPIO.input(buttonPin):
        time.sleep(0.005)
        if not GPIO.input(buttonPin):
            return True
    return False

def update_encoder(channel):
    global encoderValue, lastEncoded
    MSB = GPIO.input(encoderPinA)
    LSB = GPIO.input(encoderPinB)

    encoded = (MSB << 1) | LSB
    sum = (lastEncoded << 2) | encoded

    if sum == 0b1101 or sum == 0b0100 or sum == 0b0010 or sum == 0b1011:
        encoderValue += 1
    if sum == 0b1110 or sum == 0b0111 or sum == 0b0001 or sum == 0b1000:
        encoderValue -= 1

    lastEncoded = encoded

def main():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(encoderPinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(encoderPinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(encoderPinA, GPIO.BOTH, callback=update_encoder)
    GPIO.add_event_detect(encoderPinB, GPIO.BOTH, callback=update_encoder)

    try:
        while True:
            if is_button_push_down():
                print("you push button down!!!")
            print(read_encoder_value())
            time.sleep(0.05)
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
