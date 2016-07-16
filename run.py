import imagepov

numLEDs = 128
pov = imagepov.POV(numLEDs=numLEDs, pauseValue=0, numStepsPerCycle = 255, numCycles = -1, globalBrightness=1)
pov.start()