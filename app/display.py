# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2017 James DeVito for Adafruit Industries
# SPDX-License-Identifier: MIT

## REF https://pillow.readthedocs.io/

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!
import math
from os import stat
import time
import sys, getopt
import subprocess
import json
import pathlib

from PIL import Image, ImageDraw, ImageFont, ImageOps

import Adafruit_GPIO.SPI as SPI
import SSD1306

## Global Variables
# Default set, but can be overridden by config in addon setup.
TEMP_UNIT = "C"
SHOW_SPLASH = False
SHOW_CPU = True
SHOW_NETWORK = True
SHOW_MEMORY = True
SHOW_STORAGE = True
SHOW_SCROLLER = True
DURATION = 10

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these to the right size for your display!
RST = None
disp = SSD1306.SSD1306_128_32(rst=RST)
current_dir = str(pathlib.Path(__file__).parent.resolve())

# Clear display.
disp.begin()
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.

width = disp.width
height = disp.height

image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Load default font.
# font = ImageFont.load_default()
p = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
p_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 9)
small = ImageFont.truetype("usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 8)
smaller = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 7)
medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

img_network = Image.open(r"" + current_dir + "/img/ip-network.png") 
img_mem = Image.open(r"" + current_dir + "/img/database.png") 
img_disk = Image.open(r"" + current_dir + "/img/database-outline.png") 
img_ha_logo = m = Image.open(r"" + current_dir + "/img/home-assistant-logo.png") 
img_cpu_64 = Image.open(r"" + current_dir + "/img/cpu-64-bit.png") 

def start():
    while True:        
        if (SHOW_SPLASH) : show_splash()
        if (SHOW_SCROLLER) : show_scroller()
        if (SHOW_NETWORK) : show_network()
        if (SHOW_CPU) : show_cpu_temp()
        if (SHOW_MEMORY) : show_memory()
        if (SHOW_STORAGE) : show_storage()

        timer = reset_clock()
        

def show_storage():
    storage =  shell_cmd('df -h | awk \'$NF=="/"{printf "%d,%d,%s", $3,$2,$5}\'')
    storage = storage.split(',')

    # Clear Canvas
    draw.rectangle((0,0,128,32), outline=0, fill=0)

    # Resize and merge icon to Canvas
    icon = img_disk.resize([26,26])  
    image.paste(icon,(-2,3))

    draw.text((29, 0), "USED: " + storage[0] + ' GB \n', font=small, fill=255)
    draw.text((29, 11), "TOTAL: " + storage[1] + ' GB \n', font=small, fill=255)
    draw.text((29, 21), "UTILISED: " + storage[2] + ' \n', font=small, fill=255) 

    #image.save(r"./img/examples/storage.png")    

    disp.image(image)
    disp.display()
    time.sleep(DURATION)  

def show_memory():

    mem = shell_cmd("free -m | awk 'NR==2{printf \"%.1f,%.1f,%.0f%%\", $3/1000,$2/1000,$3*100/$2 }'")
    mem = mem.split(',')

    # Clear Canvas
    draw.rectangle((0,0,128,32), outline=0, fill=0)

    # Resize and merge icon to Canvas
    icon = img_mem.resize([26,26])  
    image.paste(icon,(-2,3))

    draw.text((29, 0), "USED: " + mem[0] + ' GB \n', font=small, fill=255)
    draw.text((29, 11), "TOTAL: " + mem[1] + ' GB \n', font=small, fill=255)
    draw.text((29, 21), "UTILISED: " + mem[2] + ' \n', font=small, fill=255)  

    #image.save(r"./img/examples/memory.png")   

    disp.image(image)
    disp.display()
    time.sleep(DURATION) 


def show_cpu_temp():

    #host_info = hassos_get_info('host/info')

    cpu = shell_cmd("top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'")
    temp =  float(shell_cmd("cat /sys/class/thermal/thermal_zone0/temp")) / 1000.00
    uptime = shell_cmd("uptime | grep -ohe 'up .*' | sed 's/,//g' | awk '{ print $2" "$3 }'")

    # Check temapture unit and convert if required.
    if (TEMP_UNIT == 'C'): 
        temp = "%0.2f °C " % (temp)
    else:
        temp = "%0.2f °F " % (temp * 9.0 / 5.0 + 32)


    # Clear Canvas
    draw.rectangle((0,0,128,32), outline=0, fill=0)

    # Resize and merge icon to Canvas
    icon = img_cpu_64.resize([26,26])  
    image.paste(icon,(-2,3))

    draw.text((29, 0), 'TEMP: ' + temp, font=small, fill=255)
    draw.text((29, 11), 'LOAD: '+ cpu + "% ", font=small, fill=255)  
    draw.text((29, 21), uptime.upper(), font=small, fill=255)

    #image.save(r"./img/examples/cpu.png")
    
    disp.image(image)
    disp.display()
    time.sleep(DURATION)


def show_network():
    #host_info = hassos_get_info('host/info')
    #hostname = host_info['data']['hostname'].upper()

    #network_info = hassos_get_info('network/info')
    #ipv4 = network_info['data']['interfaces'][0]['ipv4']['address'][0].split("/")[0]

    hostname = shell_cmd("hostname | cut -d\' \' -f1")
    ipv4 = shell_cmd("hostname -I | cut -d\' \' -f1")
    #mac = shell_cmd("cat /sys/class/net/eth0/address")

    # Clear Canvas
    draw.rectangle((0,0,128,32), outline=0, fill=0)

    # Resize and merge icon to Canvas
    icon = img_network.resize([13,13])
    image.paste(icon,(-2,0))

    draw.text((18, 0), hostname, font=medium, fill=255)
    draw.text((0, 18), "IP4 " + ipv4, font=medium, fill=255)    
    #draw.text((29, 21), "MAC " + mac.upper(), font=small, fill=255)    

    #image.save(r"./img/examples/network.png")

    disp.image(image)
    disp.display()
    time.sleep(DURATION)

def get_text_center(text, font, center_point):
    w, h = draw.textsize(text, font=font)

    return (center_point -(w/2))


def show_splash():

    os_info = hassos_get_info('os/info')    
    os_version = os_info['data']['version']
    os_upgrade = os_info['data']['update_available']  
    if (os_upgrade == True):
        os_version = os_version + "*"

    core_info = hassos_get_info('core/info')
    core_version = core_info['data']['version']  
    core_upgrade = os_info['data']['update_available']
    if (core_upgrade == True):
        core_version =  core_version + "*"


    # Draw a padded black filled box with style.border width.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Get HA Logo and Resize
    logo = img_ha_logo.resize([26,26])
    logo = ImageOps.invert(logo)  
    
    # Merge HA Logo with Canvas.
    image.paste(logo,(-2,3))

    draw.line([(34, 16),(123,16)], fill=255, width=1)

    ln1 = "Home Assistant"
    ln1_x = get_text_center(ln1, p_bold, 78)
    draw.text((ln1_x, 4), ln1, font=p_bold, fill=255)

    # Write Test, Eventually will get from HA API.
    ln2 = 'OS '+ os_version + ' - ' + core_version
    ln2_x = get_text_center(ln2, small, 78)
    draw.text((ln2_x, 20), ln2, font=small, fill=255)


    # Display Image to OLED
    #image.save(r"./img/examples/splash.png")
    disp.image(image)
    disp.display() 
    time.sleep(DURATION)


def show_scroller():
    hostname = shell_cmd("hostname | cut -d\' \' -f1")
    scroller = Scroller('Welcome to ' + hostname, height/2 - 4, width, height/4, large)
    
    while True:
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        scroller.render()
        disp.image(image)
        disp.display()

        if not scroller.move_for_next_frame(renderTimeBreak()):
            break

def hassos_get_info(type):
    info = shell_cmd('curl -sSL -H "Authorization: Bearer $SUPERVISOR_TOKEN" http://supervisor/' + type)
    return json.loads(info)


def shell_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode("utf-8")

def clear_display():
    disp.fill(0)
    disp.display()

def reset_clock():
    return time.time() + DURATION

def renderTimeBreak():
    return time.time() < timer

class Scroller:
    def __init__(self, text, offset = 12, startpos = width, amplitude = 0, font = large, velocity = -2, draw_obj = draw, width = width):
        self.text = text
        self.draw = draw_obj
        self.amplitude = amplitude
        self.offset = offset
        self.velocity = velocity
        self.width = width
        self.startpos = startpos
        self.pos = startpos
        self.font = font
        self.maxwidth, unused = self.draw.textsize(self.text, font=self.font)

    def render(self):
        # Enumerate characters and draw them offset vertically based on a sine wave.
        x = self.pos
        
        for i, c in enumerate(self.text):
            # Stop drawing if off the right side of screen.
            if x > self.width:
                break

            # Calculate width but skip drawing if off the left side of screen.
            if x < -10:
                char_width, char_height = self.draw.textsize(c, font=self.font)
                x += char_width
                continue

            # Calculate offset from sine wave.
            y = self.offset + math.floor(self.amplitude * math.sin(x / float(self.width) * 2.0 * math.pi))

            # Draw text.
            self.draw.text((x, y), c, font=self.font, fill=255)

            # Increment x position based on chacacter width.
            char_width, char_height = self.draw.textsize(c, font=self.font)
            x += char_width

    def move_for_next_frame(self, allow_startover):
        self.pos += self.velocity
        # Start over if text has scrolled completely off left side of screen.
        if self.has_completed():
            if allow_startover:
                self.start_over()
                return True
            else:
                return False
        return True

    def start_over(self):
        self.pos = self.startpos

    def has_completed(self):
        return self.pos < -self.maxwidth

timer = reset_clock()

if __name__ == "__main__":
    start()
