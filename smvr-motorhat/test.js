var MotorHat = require('./index.js');
var motor = new MotorHat();

motor.on('ready', function() {
	console.log('Weee ready');
	motor.step(100, 100, motor.FORWARD, motor.SINGLE)
})
