# EyeSee
## HackPrinceton '17 Project
https://devpost.com/software/humanvision
First place winner in the AR/VR Category! 

About: EyeSee is an interactive headset that detects certain dangers for the user and outlines those danger to provide awareness of said danger to partially sighted users. Partially sighted refers to the condition where the individual is not completely blind but has trouble seeing and outlining objects within their surroundings. The outline of objects tend to mix in together and it becomes hard to see the shape and structure of certain things, especially when it comes to objects within the same color range. EyeSee eliminates this problem by sharpening the image and creating an outline between everything that the user sees! This is but it's main functionality of course, the beauty comes in identifying certain dangers such as stop and cross signs, traffic lights, side walks, cars? The options are endless depending on the user's environment! Not only that, but we've also developed a communication system to give a warning sign and speak out the name of the danger identified.

### Our awesome team: Emils Matiss, Mostafa Okasha, Susan Wang Xing

## Process:

We built our own headset from scratch! Got an LED screen, a webcam, a VR headset and a RasberryPi and magically connected everything together. Split the screen from the LED to create screen mirroring to give that crisp 3D effect. The rest was all programming.

Basically how it works:
* Pull image form webcam
* Process image for high contrast
* Use Machine learning to identify objects
* Warn user if object is detected

## Running
You will need OpenCV, anaconda is recomended.
Python multi.py <i>filename</i> objectname detectionThreshold(~60)
