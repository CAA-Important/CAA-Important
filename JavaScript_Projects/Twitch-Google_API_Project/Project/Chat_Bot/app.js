var tmi = require('tmi.js');

var options ={
  options: {
    debug: true
  },
  connection: {
    cluster: "aws",
    reconnect: true
  },
  identity: {
    username: "",
    password: "oauth:"
  },
  channels: []
};

var client = new tmi.client(options);
client.connect();

client.on('chat', function(channel, user, message, self){
  client.action("", message);
});

client.on('connected', function(address, port) {
  client.action("", "Hello World!");
});
