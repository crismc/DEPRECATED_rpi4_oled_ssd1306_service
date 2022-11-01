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
- PIN1 : Power (3.3V / VCC)
- PIN3: SDA (I2C Data)
- PIN5: SCL (I2C Clock)
- PIN14: Ground (0V)

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
git clone http://192.168.0.2:3000/personal/Adafruit_Python_SSD1306
cd Adafruit_Python_SSD1306
sudo python setup.py install
```

Test OLED
```
cd examples
python3 stats.py
```

Copying
-------

Written by Tony DiCola for Adafruit Industries.
MIT license, all text above must be included in any redistribution
