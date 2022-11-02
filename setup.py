import os
import io
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

classifiers = ['Development Status :: 4 - Beta',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

setup(name              = 'pioled',
      version           = '0.1',
      author            = 'Chris Churchill',
      author_email      = 'chris@serva.co.uk',
      description       = 'Python library using the Adafruit SSD1306 python bootstrap for SSD1306-based 128x64 or 128x32 pixel OLED displays with a Raspberry Pi or Beaglebone Black.',
      long_description  = long_description,
      license           = 'MIT',
      classifiers       = classifiers,
      url               = 'http://192.168.0.2:3000/personal/oled_ssd1306',
      dependency_links  = ['https://github.com/adafruit/Adafruit_Python_GPIO/tarball/master#egg=Adafruit-GPIO-0.6.5'],
      install_requires  = ['Adafruit-GPIO>=0.6.5'],
      packages          = find_packages())
