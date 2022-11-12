IC2 OLED controller for Raspberry PI
=======================

Original Repo: https://github.com/adafruit/Adafruit_Python_SSD1306

Adafruit Python SSD1306
=======================

Python library to use SSD1306-based 128x64 or 128x32 pixel OLED displays with a Raspberry Pi or Beaglebone Black.

Designed specifically to work with the Adafruit SSD1306-based OLED displays ----> https://www.adafruit.com/categories/98

Adafruit invests time and resources providing this open source code, please support Adafruit and open-source hardware by purchasing products from Adafruit!

Hardware Setup
--------------
Pin setup:
```
- PIN1 : Power (3.3V / VCC)
- PIN3: SDA (I2C Data)
- PIN5: SCL (I2C Clock)
- PIN14: Ground (0V)
```

Enable i2c and SPI on the Raspberry Pi
```
sudo raspi-config
# Interface Options > SPI and I2C
```

Installing
----------
Initial apt-get installs:
```
sudo apt-get install i2c-tools git vim
```

Test I2C device is working:
```
$ i2cdetect -y 1
```

Install Python3 dependencies
```
sudo apt-get install python3-dev python3-smbus python3-pil python3-pip python3-setuptools python3-rpi.gpio
```

Install this code
```
git clone http://192.168.0.2:3000/personal/oled_ssd1306
cd oled_SSD1306
sudo python setup.py install
```

Test OLED
```
python3 oled.py
```

Create a service 
-----------------

Copy the repo file to /etc:
```
sudo cp -ri oled_ssd1306 /etc
```

Create a sym link of the service file in /etc/systemd/system, and reload it
```
sudo ln -s /etc/oled_ssd1306/oled.service /etc/systemd/system/oled.service
sudo systemctl daemon-reload
```

Test it out
```
sudo service oled start
sudo service oled stop
sudo service oled restart
```

Start on boot
```
sudo systemctl enable oled.service
```


#
#
#


# Legal Stuff Required By Adafruit
As part of the  library leveraged to produce this service, the below text needs to be copied. 

However, you can ignore the install instructions below as they've been replaced by the above.

[Original Adafruit Repository](https://github.com/adafruit/Adafruit_Python_SSD1306)

*DEPRECATED LIBRARY* Adafruit Python SSD1306
=======================

his library has been deprecated! We are leaving this up for historical and research purposes but archiving the repository.

We are now only supporting the use of our CircuitPython libraries for use with Python.

Check out this guide for info on using OLEDs with the CircuitPython library: https://learn.adafruit.com/monochrome-oled-breakouts/python-wiring

---------------------------------------

Python library to use SSD1306-based 128x64 or 128x32 pixel OLED displays with a Raspberry Pi or Beaglebone Black.

Designed specifically to work with the Adafruit SSD1306-based OLED displays ----> https://www.adafruit.com/categories/98

Adafruit invests time and resources providing this open source code, please support Adafruit and open-source hardware by purchasing products from Adafruit!

Installing
----------

```
sudo python -m pip install --upgrade pip setuptools wheel
sudo pip install Adafruit-SSD1306
```

Or alternatively:

```
sudo python -m pip install --upgrade pip setuptools wheel
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306
sudo python setup.py install
```

Copying
-------

Written by Tony DiCola for Adafruit Industries.
MIT license, all text above must be included in any redistribution
