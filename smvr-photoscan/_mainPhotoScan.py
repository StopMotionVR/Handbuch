import PhotoScan
import sys
import os
import time

import pseudoGlobals
from stalkerThread import *
from listeningThread import *
from stateMachine import *
from reconstructionKit import *
from newClass import *

PhotoScan.app.console.clear()
PhotoScan.app.update()


testThread = StalkerThread(1, "Stalker")
testThread.start()

try:
	while True:
		time.sleep(0.5)
		PhotoScan.app.update()
		if pseudoGlobals.shouldStartReconstruction:
			pseudoGlobals.shouldStartReconstruction = False
			if startReconstruction():
				print('Reconstruction successful!')
			else:
				if pseudoGlobals.shouldInterruptReconstruction:
					print('Just as I said... Like a sir.')
					pseudoGlobals.shouldInterruptReconstruction = False
				else:
					print('Reconstruction failed!')
				PhotoScan.app.document.clear()
			
	
except NameError as e:
	print('Unknown exception')
	print(type(e))
	print(e)
finally:
	print('FINALLY')
	#sys.exit(0)
	#os.kill()