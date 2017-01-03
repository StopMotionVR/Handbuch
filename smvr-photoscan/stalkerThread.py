import pseudoGlobals
import threading
from threading import Thread, Lock
import time
from sendDefs import *

class StalkerThread(threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.daemon = True
		self.threadID = threadID
		self.name = name
	def run(self):
		isLoopRunning = True
		while isLoopRunning:
			try:
				# update progress
				payload = {
					'absolute': pseudoGlobals.currentAbsoluteProgress,
					'relative': pseudoGlobals.currentRelativeProgress,
					'type': 'KNOWN'
				}
				time.sleep(0.4)
			except KeyboardInterrupt:
				isLoopRunning = False