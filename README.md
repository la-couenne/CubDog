# CubDog, Robot who follows us
![00](https://user-images.githubusercontent.com/38251711/119193147-7ae04e00-ba81-11eb-8339-bdbdfc4213b8.png)

Hello everybody,

Here is the continuation of the adventures of CubDog my cube which follows like a doggie.

He uses a Raspberry Pi and OpenCV to locate people, here to simplify the code he will follow them with his head (with a single servo to turn it from left to right).

# Demo:
https://youtu.be/go1tbi9qKB0

https://youtu.be/-I3wBoJ9Zac

It is equipped with a webcam (under its old ultrasound eyes which are no longer used ..), a Raspberry Pi as well as a control screen. He also has 2 small arms, which fold into his stomach like Wall-E :-) The chassi is made with Makeblock pieces.

# Check the servomotors:
![000](https://user-images.githubusercontent.com/38251711/119193770-6e102a00-ba82-11eb-85f4-275d14cd629d.png)

So to turn my head I use the PCA9685 module from Adafruit, which I plug in as shown in the diagram

To install OpenCV and imutils on the raspberry:
```shell
$> sudo apt-get install python-opencv
$> sudo apt-get install libopencv-dev
$> sudo pip install imutils
```

# DC motor control:
![001](https://user-images.githubusercontent.com/38251711/119194147-f1ca1680-ba82-11eb-9848-eec20f1bb832.png)

To run the DC motors of the crawlers, I made an H-bridge available here:
http://nagashur.com/blog/2013/01/05/utilisation-dun-circuit-l293d-pour-commander-des-moteurs

Good hacks everyone!

