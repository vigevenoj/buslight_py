# buslight_py
Upcoming Trimet arrivals trigger color-coded lighting changes. Python3 flavor

# Installation
1. Clone this repository
1. pip install -r requirements.txt

# Getting started
1. Get a TriMet developer key at https://developer.trimet.org/appid/registration/
1. Set up Philips Hue python integration via phue
1. Set up configuration file in ./trimet.yaml
  * TriMet API key
  * TriMet stop IDs
1. Run the script, python buslight.py

The script will output what color it is changing to as well as how long until the 
next arrival to *any* of the configured stops, and will then schedule the next 
time it will make a request to TriMet for arrivals data. 

Script does not terminate by itself, so it will keep running until stopped.


For a ruby version, see
https://github.com/vigevenoj/scripts/blob/master/bus_light.rb
