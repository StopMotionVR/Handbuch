// process.env.DEBUG = 'node-ssdp*';

var os = require('os');
var exec = require('child_process').exec;
var request = require('request');

var parseString = require('xml2js').parseString;

var request = require('request');

var Client = require('node-ssdp').Client;
var wifi = require('node-wifi')

module.exports = function(userConfig) {

  this.defaultConfig = {
    maxMSearch : 10,
    cameraSchema : 'urn:schemas-sony-com:service:ScalarWebAPI:1',
		API_URL : null,
		ssid : null,
		psk : null
  };
  this.mClient = null;
  this.searchTimer = null;
  this.timerCounter = 0;

  this.config = Object.assign({}, this.defaultConfig, userConfig);

  this.sendRPCNoArgs = function(m, v, p) {
    p = p || [];
    return new Promise(function(resolve, reject) {
      v = v || "1.0";
      var c = { "method": m, "params": p, "id": 1, "version": v };
      request({
        method : "POST",
        uri  : this.config.API_URL + "/camera",
        json : true,
        body : c
      }, function(error, res, body) {
        if(error) return reject(error);
        else return resolve(body);
      });
    }.bind(this));
  };

  this.connectWifi = function() {
    return new Promise(function(resolve, reject) {
			console.log('Conntecting Wifi: ' + this.config.ssid + ' : ' + this.config.psk + '...')
			wifi.connect({ ssid : this.config.ssid, password : this.config.psk }, function(err) {
				if (err) {
					console.error(err)
					return reject(err)
				}
				console.log('Connected!')
				return resolve()
			});
    });
  };

  this.disconnectWifi = function() {
    return new Promise(function(resolve, reject) {
      if(os.platform() == 'win32') {
        exec('netsh wlan disconnect', resolve);
      } else {
        exec('nmcli device disconnect iface wlan0', resolve);
      }
    });
  };

  this.discoverCamera = function() {
    return new Promise(function(resolve, reject) {
      console.log('Starting Camera Discovery');

      this.timerCounter = 0;

      this.mClient = new Client();

      this.mClient.on('response', function (headers, statusCode, rinfo) {
        clearInterval(this.searchTimer);

        this.config.DEVICE_DEC = headers.LOCATION;

        console.log('Found Device!');
        console.log('Device Description at: ', this.config.DEVICE_DEC);

        resolve();
      }.bind(this));

      this.sendMSearch(reject);
      this.searchTimer = setInterval(function() { this.sendMSearch(reject); }.bind(this), 2000);
    }.bind(this));
  };

  this.sendMSearch = function(reject) {
    if(this.timerCounter == this.config.maxMSearch) {
      clearInterval(this.searchTimer);
      console.log('Maximum M-Search trys reached, stopping camera discovery now.');
      return reject('Maximum M-Search trys reached, stopping camera discovery now.');
    }
    console.log('Sending M-Search no. ' + (this.timerCounter + 1));
    this.mClient.search(this.config.cameraSchema);
    this.timerCounter ++;
  };

  this.parseDeviceDec = function() {
    return new Promise(function(resolve, reject) {
      console.log('Requesting Device Description');
      request.get(this.config.DEVICE_DEC, function (error1, response, deviceDecXML) {
        if(error1) {
          console.error(error1);
          return reject(error1);
        }

        parseString(deviceDecXML, function (error2, r) {
          if(error2) {
            console.error(error2);
            return reject(error2);
          }

          var device = r.root.device[0];

          this.config.CAMERA_NAME = device.friendlyName[0];
          this.config.API_URL = device['av:X_ScalarWebAPI_DeviceInfo'][0]['av:X_ScalarWebAPI_ServiceList'][0]['av:X_ScalarWebAPI_Service'][2]['av:X_ScalarWebAPI_ActionList_URL'][0];

          console.log("Device Info:");
          console.log("-----------------------");
          console.log("Device Name: ", this.config.CAMERA_NAME);
          console.log("API Endpoint: ", this.config.API_URL);
          console.log("-----------------------");

          resolve();

        }.bind(this));
      }.bind(this));
    }.bind(this));
  };

  this.initShooting = function() {
    return this.sendRPCNoArgs("startRecMode");
  };

  this.getSupportedCameraFunction = function(iso) {
    return this.sendRPCNoArgs("getSupportedCameraFunction");
  };

  this.setFNumber = function(f) {
    return this.sendRPCNoArgs("setFNumber", null, [f]);
  };

  this.setShutterSpeed = function(s) {
    return this.sendRPCNoArgs("setShutterSpeed", null, [s]);
  };

  this.setISO = function(iso) {
    return this.sendRPCNoArgs("setIsoSpeedRate", null, [iso]);
  };

  this.takePhoto = function() {
    return this.sendRPCNoArgs("actTakePicture");
  };

};
