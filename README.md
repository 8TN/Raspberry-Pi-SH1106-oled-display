# Raspberry-Pi-SH1106-oled-display
Basic python3 script to display an image using SPI on SH1106 128 by 64 monochrome Oled display.
(can be adapted to python 2.x)

Works on a Raspberry Pi 2 Model B Revision 1.1 1GB, 
with a Raspbian Strech version dated November 13th 2018.
SPI interface has been enable using 'sudo raspi-config'.

once launched, ask for the file name to be used
(can be .png; jpg..., any format supported by PIL).

If the picture is bigger than 128 x 64 pixels, only the upper/left part is displayed, 
note also that the picture is black and white converted.

Loading the display is quite fast (screen refresh rate is no visible,few msec) when using 1 MHz SPI clock speed.
It becomes much more visible if you use lower clock speed:
  - try to change the line "spi.max_speed_hz = 1000000"
  
  to
  
  - "spi.max_speed_hz = 7629"

What takes time is to prepare the display data from the input file (about 200 msec). 
