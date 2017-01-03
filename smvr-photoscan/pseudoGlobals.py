STATE_INIT			= 'INIT'
STATE_READY			= 'READY'
STATE_STARTED		= 'STARTED'
STATE_FETCHING		= 'FETCHING'
STATE_MATCHING		= 'MATCHING'
STATE_ALIGNMENT		= 'ALIGNMENT'
STATE_DENSE_CLOUD	= 'DENSE_CLOUD'
STATE_MODEL			= 'MODEL'
STATE_UV_MAP		= 'UV_MAP'
STATE_DIFFUSE		= 'DIFFUSE'
STATE_EXPORT		= 'EXPORT'
STATE_FINISHED		= 'FINISHED'
STATE_ERROR			= 'ERROR'

currentState = STATE_INIT
currentStateRegistered = True

shouldInterruptReconstruction = False
shouldStartReconstruction = False

currentAbsoluteStep = 0
currentRelativeProgress = 0.0
currentAbsoluteProgress = 0.0