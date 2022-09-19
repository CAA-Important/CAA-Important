//Get the required packages
var tmi = require('tmi.js');
var path = require('path');
var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
const {Translate} = require('@google-cloud/translate');

//Set the location of the folder containing the HTML and CSS files that will sent to the user and displayed
//Used this to figure out how to send an entire folder for the HTML: https://stackoverflow.com/questions/40509666/sending-whole-folder-content-to-client-with-express
var html_path = path.join(__dirname, 'Project_Interface');
app.use(express.static(html_path));

//Set necessary information for the Google Translate API
//Information for the setup: https://cloud.google.com/translate/docs/reference/libraries#client-libraries-install-nodejs
const projectId = "cobalt-deck-223421";
const translate = new Translate({   projectId: projectId, });

//Create an object to hold the required settings for our Twitch chat bot
//Used this video to help set up the Twitch chat bot: https://www.youtube.com/watch?v=K6N9dSMb7sM
//Once the bot was set up, everything else came from the documentation for Twitch's interface at https://docs.tmijs.org/v1.2.1/Functions.html
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
    password: ""
  },
  channels: [""]
};


var client = null;
//Create a class for the storing of user information
class userInfo {
  constructor(){
  this.user = null;
  this.userClient = null;
  this.language = null;
  }
}

var users = []

//Handle new socket connections to the server
//Information used to handle sockets: https://socket.io/docs/
//Extra socket help: https://socket.io/get-started/chat
io.on('connection', function(socket) {
  //Restrict maximum number of users
  if(users.length >= 10){
    socket.emit('disconnect', 'Too many users.  Sorry.');
    socket.disconnect();
  }
  else{
    //If a user disconnects, remove them from the list of users
      socket.on('disconnect', function() {
        for(i = 0; i < userInfo.length; i++){
          if(users[i].user.id == socket.id){
            users[i].userClient.disconnect();
            users.splice(i, 1);
            break;
          }
        }
      });

      //Handles when a user wants to connect to a different Twitch chat for translating
      socket.on('set_channel', function(channel){
        var i;
        var x;
        for(i = 0; i < users.length; i++){
          //Find the user that has connected and get the object holding their connection to their current Twitch chat
          if(("" + users[i].user.id) == ("" + socket.id)){
            client = users[i].userClient;
            //console.log("found " + users[i].userClient);
            x = i;
          }
        }
        //Disconnect from the current Twitch chat
        if(client != null){
          client.disconnect();
        }

        //Connect to the newly chosen Twitch Chat
        options.channels = [channel];
        client = new tmi.client(options);
        client.connect();
        users[x].userClient = client;

        //Set the Twitch chat connection object to listen for chat messages
        client.on('chat', function(channel, user, message, self){
          var i;
          var theLanguage;
          for(i = 0; i < users.length; i++){
            if(("" + users[i].user.id) == ("" + socket.id)){
              theLanguage = users[i].language;
            }
          }
          if(theLanguage == null){
            theLanguage = "en";
          }
          //When a message is received, translate that message, and then send it to the user
          translate
          .translate(message, theLanguage).then(results => {
            socket.emit('new_message', user.username, results[0]);
          })
          .catch(err => {
            console.error('ERROR:', err);
          });

        });
      });

      //Function to handle when the user wants to change the language the Twitch chat is being translated into.
      socket.on('set_language', function(language){
        var i;
        for(i = 0; i < users.length; i++){
          if(("" + users[i].user.id) == ("" + socket.id)){
            users[i].language = language;
          }
        }
      });

      //All of the functions above set up important information for the socket
      //With all of that information in, put that socket inside of a userInfo object
      //Then append the new user into the list of users
      var newUser = new userInfo;
      newUser.user = socket;
      users.push(newUser);
    }
  });

//Listen for users on port 8080
http.listen(8080, function () {
    var host = 'localhost';
    var port = http.address().port;
    console.log('listening on http://'+host+':'+port+'/');
});
