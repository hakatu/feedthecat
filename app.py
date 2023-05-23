from flask import Flask, render_template, Response
import RPi.GPIO as GPIO
from picamera import PiCamera
from io import BytesIO
import subprocess

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Set your pin numbers here
led_pin = 18
GPIO.setup(led_pin, GPIO.OUT)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/toggle_led')
def toggle_led():
    GPIO.output(led_pin, not GPIO.input(led_pin))
    led_status = "ON" if GPIO.input(led_pin) else "OFF"
    subprocess.Popen(['cvlc', 'static/sound.mp3', '--play-and-exit'])
    return led_status

def gen():
    with PiCamera() as camera:
        camera.resolution = (640, 480)  # Set the resolution
        camera.framerate = 60  # Set the framerate
        while True:
            stream = BytesIO()
            camera.capture(stream, format='jpeg')
            stream.seek(0)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + stream.read() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=80, debug=True)
    except KeyboardInterrupt:
        GPIO.cleanup()

