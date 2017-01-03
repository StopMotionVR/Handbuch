import pseudoGlobals;
from sendDefs import *

def setState(newState):
	if pseudoGlobals.currentState != newState:
		pseudoGlobals.currentState = newState
		pseudoGlobals.currentStateRegistered = False
		print('Switching state to "'+pseudoGlobals.currentState+'"')
		sendStatus()

def sendStatus():
	print('Sending new status: '+pseudoGlobals.currentState)
	body = {
		'mid': pseudoGlobals.moduleUniqueID,
		'status': pseudoGlobals.currentState
	}
	sendPost('status', body)