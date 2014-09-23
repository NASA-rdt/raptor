#!/usr/bin/python

#Created for NASA GSFC SSCO internship by Aaron Neely summer 2014

# This script will controll the boot status light on the RAPTOR Edge arm kit
# The light will be blue while booting up and then green while the kit is
# running and ready to go

import raptorStatusLights as lights

lights.status_lights('boot','blue',0)
lights.status_lights('boot','green',1)
