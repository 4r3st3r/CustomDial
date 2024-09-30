# Custom Dial

This simple project allows users to quickly, cheaply, and easily make a custom dial they can have in their homes to project any data they wish.

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
4. Copy whichever example you'd like to use onto Pico W as `main.py`, changing Wi-Fi SSID and Password as you do so (or better yet **make your own and fork this repo**)
5. Make dial face (use the front plate as a template)
6. The horn extender simply snaps onto the basic SG90 horn, make sure to attach it when you know the angle of the servo!
7. Enjoy!

# Example Projects
### 1. Green Energy Dial - `UK_green_energy.py`
This simple project (roughly) displays the current percentage of the UK's electricity grid produced by green energy. For this I have classed Wind, Solar, Hydroelectric and (perhaps controversially) Nuclear power as being 'renewable' energy. 
>With this in mind, perhaps a better name for it is the Non-Carbon-Dioxide-Emmitting Energy Dial - but that seems like rather a mouthful!

The data is collected from the [Carbon Intensity API](https://carbonintensity.org.uk) a **FREE** api that lists the current mix of energy - as well as lots of other great information.
*Please, do not spam the API with requests!*

![Front](GED1.jpeg)
![Back](GED2.jpeg)

### 2. US Presidential Election 2024 - `president_odds.py`
This calculates the odds of Kamala Harris or Donald Trump winning the 2024 Presidential election, and the outputs the percentage chance of them winning.
It uses the **FREE** (if using the basic tier) [The Odds API](https://the-odds-api.com) which also has a load of other great sports odds aggregators.  
