var PythonShell = require('python-shell')

module.exports = function(userConfig) {

	this.FORWARD = 1
	this.BACKWARD = 2

	this.SINGLE = 1
	this.DOUBLE = 2
	this.INTERLEAVE = 3
	this.MICROSTEP = 4

  this.config = userConfig

	this.on = function(which, f) {
		if(which == 'ready') {
			this.config.readyF = f
			this.config.readyF()
		}
	}

	this.step = function(speed, steps, direction, step_type) {
		var options = {
  		mode: 'text',
			scriptPath: __dirname,
  		args: [speed, steps, direction, step_type]
		}

		PythonShell.run('stepper.py', options, function (err, results) {
			if (err) console.error(err)
			// results is an array consisting of messages collected during execution
			console.log('results: %j', results)
			if(this.config.readyF) this.config.readyF()
		}.bind(this))
	}
}
