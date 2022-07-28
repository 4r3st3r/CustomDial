# Green Energy Dial

This simple project (roughly) displays the current percentage of the UK's electricity grid produced by green energy. For this I have classed Wind, Solar, Hydroelectric and (perhaps controversially) Nuclear power as being 'renewable' energy. 
>With this in mind, perhaps a better name for it is the Non-Carbon-Dioxide-Emmitting Energy Dial - but that seems like rather a mouthful!

The data is collected from the (Carbon Intensity API)[https://carbonintensity.org.uk] a **FREE** api that lists the current mix of energy - as well as lots of other great information.
*Please, do not spam the API with requests!* 

# Materials Required
- Raspberry Pi Pico W - running MicroPython
- Micro-USB cable to connect to the Pico (as well as power it, or you can just wire it up to a 5V source)
- SG92R servo motor
- 3D Printer (or the ability to 3D print, or make parts manually)
- Some paper to make the dial face

# Setup
1. Print all STL files
2. Attach servo motor to base plate and connect to Pico
3. Set up pico - instructions [here](https://datasheets.raspberrypi.com/picow/connecting-to-the-internet-with-pico-w.pdf)
4. Copy `main.py` onto Pico, changing Wi-Fi SSID and Password as you do so
5. Make dial face (use the front plate as a template)
6. The horn extender simply snaps onto the basic SG90 horn, make sure to attach it when you know the angle of the servo!
7. Enjoy!


![Front](GED1.jpeg)
![Back](GED2.jpeg)
