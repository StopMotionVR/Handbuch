var wait = function(ms) {
  return new Promise(function(resolve, reject) {
    setTimeout(resolve, ms);
  });
};

var SonyRemote = require('./index.js');
var remote = new SonyRemote({ ssid : 'DIRECT-yUE0:ILCE-6000', psk : 'password' });

remote
  .connectWifi()
  .then(function(result) {
    console.log(result);
    return wait(2000);
  })
  .then(function() {
    return remote.discoverCamera();
  })
  .then(function() {
    return remote.parseDeviceDec();
  })
  .then(function() {
    console.log('Init Shooting ...');
    return remote.initShooting();
  })
  .then(function(result) {
    console.log(result);
    return wait(3000);
  })
  .then(function() {
    return remote.setFNumber("5.6");
  })
  .then(function(result) {
    console.log(result);
    return remote.setISO("200");
  })
  .then(function(result) {
    console.log(result);
    return remote.setShutterSpeed("1/200");
  })
  .then(function() {
    console.log('Taking Photo No. 1 ...');
    return remote.takePhoto();
  })
  .then(function(result) {
    console.log(result);
    return wait(250);
  })
  .then(function() {
    return remote.setShutterSpeed("1");
  })
  .then(function() {
    console.log('Taking Photo No. 2 ...');
    return remote.takePhoto();
  })
  .then(function(result) {
    console.log(result);
    return wait(250);
  })
  .then(function() {
    return remote.setShutterSpeed("3");
  })
  .then(function() {
    console.log('Taking Photo No. 3 ...');
    return remote.takePhoto();
  })
  .then(function(result) {
    console.log(result);
    console.log('Disconnecting in 2sec ...');
    return wait(2000);
  })
  .then(function() {
    return remote.disconnectWifi();
  })
  .catch(function(error) {
    console.log(error);
  });
