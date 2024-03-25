const tmi = require('tmi.js');
const {User, Makgora} = require('./commands/makgora/main');
const uploadClip = require('./commands/clip/uploadClip');

// Define configuration options
const opts = {
  identity: {
    username: "",
    password: ""
  },
  channels: [
    
  ]
};

// Create a client with our options
const client = new tmi.client(opts);

// Register our event handlers (defined below)
client.on('message', onMessageHandler);
client.on('connected', onConnectedHandler);

// Connect to Twitch:
client.connect();
// const makgora = new Makgora();

// Called every time a message comes in
function onMessageHandler (target, context, msg, self) {
  try{
    if (self) { return; } // Ignore messages from the bot
    // Remove whitespace from chat message
    const msgList = msg.trim().split(' ');
    const commandName = msgList[0];
    // If the command is known, let's execute it
    if (commandName === '!dice') {
      const num = rollDice();
      client.say(target, `You rolled a ${num}`);
      console.log(`* Executed ${commandName} command`);
    } else if (commandName === '!클립') {
      uploadClip(target.replace('#', ''), msg.replace(commandName, '').trim())
    }
    else if (commandName === '!막고라신청'){
      const user = new User(context['user-id'], context['username'], context['display-name']);
      client.say(target, makgora.push(target, user, msgList));
    }else if (commandName === '!막고라삭제'){
      try{
        if(context['badges-raw'] !== null && (context['badges-raw'].indexOf('broadcaster') >= 0 || context['badges-raw'].indexOf('moderator') >= 0 || context['display-name'] === '야구보놔')){
          client.say(target, makgora.delete(target, msgList[1]));
        }
      }catch(error){
        return;
      }
    }else if (commandName === '!막고라취소'){
      client.say(target, makgora.deleteMe(target, context['user-id']));
    }else if (commandName === '!막고라'){
      client.say(target, makgora.getListString(target));
    }else if (commandName === '!막고라순서'){
      client.say(target, `${context['display-name']}님은 ${makgora.indexOf(target, context['user-id'])}번째 순서입니다.`);
    }else if (commandName === '!master'){
      client.say(target, makgora.getMasterListString(target));
    }else if (commandName === '!insert'){
      if(context['badges-raw'] !== null && (context['badges-raw'].indexOf('broadcaster') >= 0 || context['badges-raw'].indexOf('moderator') >= 0)){
        const user = new User(context['user-id'], context['username'], context['display-name']);
        client.say(target, makgora.insert(target, user, msgList[1], msgList));
      }
    }
  }catch(error){
    console.log(error);
  }
}

// Function called when the "dice" command is issued
function rollDice () {
  const sides = 6;
  return Math.floor(Math.random() * sides) + 1;
}

// Called every time the bot connects to Twitch chat
function onConnectedHandler (addr, port) {
  console.log(`* Connected to ${addr}:${port}`);
}
