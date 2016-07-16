#!/usr/bin/python

# Persistence-of-vision (POV) example for Adafruit Dot Star RGB LED strip.
# Loads image, displays column-at-a-time on LEDs at very high speed,
# suitable for naked-eye illusions.
# See strandtest.py for a much simpler example script.
# See image-paint.py for a slightly simpler light painting example.

import Image
# from dotstar import Adafruit_DotStar
from colorcycletemplate import ColorCycleTemplate



# print "Displaying..."
# while True:                            # Loop forever

# 	for x in range(width):         # For each column of image...
# 		strip.show(column[x])  # Write raw data to strip

class POV(ColorCycleTemplate):
	def init(self, strip, numLEDs):
		self.filename  = "earth.png" # Image file to load
		# self.rOffset = 2
		# self.gOffset = 3
		# self.bOffset = 1
		# self.rOffset = 0
		# self.gOffset = 1
		# self.bOffset = 2
		self.rOffset = 3
		self.gOffset = 2
		self.bOffset = 1
		
		print "Loading..."
		self.img       = Image.open(self.filename).convert("RGB")
		self.pixels    = self.img.load()
		self.width     = self.img.size[0]
		self.height    = self.img.size[1]
		self.numLEDs = self.height
		print "%dx%d pixels" % self.img.size

		# Calculate gamma correction table, makes mid-range colors look 'right':
		self.gamma = bytearray(256)
		for i in range(256):
			self.gamma[i] = int(pow(float(i) / 255.0, 2.7) * 255.0  *0.2+ 0.5) 

		# Allocate list of bytearrays, one for each column of image.
		# Each pixel REQUIRES 4 bytes (0xFF, B, G, R).
		print "Allocating..."
		self.column = [0 for x in range(self.width)]
		for x in range(self.width):
			self.column[x] = bytearray(self.height * 4)

		# Convert entire RGB image into column-wise BGR bytearray list.
		# The image-paint.py example proceeds in R/G/B order because it's counting
		# on the library to do any necessary conversion.  Because we're preparing
		# data directly for the strip, it's necessary to work in its native order.
		print "Converting..."
		for x in range(self.width):          # For each column of image...
			for y in range(self.height): # For each pixel in column...
				value             = self.pixels[x, y]    # Read pixel in image
				y4                = y * 4           # Position in raw buffer
				self.column[x][y4]     = 0xFF            # Pixel start marker
				self.column[x][y4 + self.rOffset] = self.gamma[value[0]] # Gamma-corrected R
				self.column[x][y4 + self.gOffset] = self.gamma[value[1]] # Gamma-corrected G
				self.column[x][y4 + self.bOffset] = self.gamma[value[2]] # Gamma-corrected B
	def update(self, strip, numLEDs, numStepsPerCycle, currentStep, currentCycle):
		# One cycle = One thrip through the color wheel, 0..254
		# Few cycles = quick transition, lots of cycles = slow transition
		# Note: For a smooth transition between cycles, numStepsPerCycle must be a multiple of 7
		# startIndex = currentStep % 7 # Each segment is 7 dots long: 2 blank, and 5 filled
		# colorIndex = strip.wheel(int(round(255/numStepsPerCycle * currentStep, 0)))
		# for pixel in range(numLEDs):
		#     # Two LEDs out of 7 are blank. At each step, the blank ones move one pixel ahead.
		#     if ((pixel+startIndex) % 7 == 0) or ((pixel+startIndex) % 7 == 1): strip.setPixelRGB(pixel, 0)
		#     else: strip.setPixelRGB(pixel, colorIndex)
		# for x in range(self.width):          # For each column of image...
		x = currentStep%self.width	
		# for y in range(self.height): # For each pixel in column...
		# 	y4                = y * 3           # Position in raw buffer
		# 	value1 = self.column[x][y4 + self.rOffset]
		# 	value2 = self.column[x][y4 + self.gOffset]
		# 	value3 = self.column[x][y4 + self.bOffset]
		# 	strip.setPixelRGB(y,  strip.combineColor(value1, value2, value3))
		strip.leds = self.column[x]
		return 1

