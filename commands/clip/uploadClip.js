const spawn = require('child_process').spawn
const path = require("path");
const lastCommanded = {}

uploadClip = (username, title) => {
    let now = new Date()
    if (!lastCommanded[username] || now - lastCommanded[username] > 20000) {
        lastCommanded[username] = now
        let sp = null;
        if (title) {
            sp = spawn('python3.10', [path.join(__dirname, 'upload_clip.py'), '-u', username, '-t', title]);
        } else {
            sp = spawn('python3.10', [path.join(__dirname, 'upload_clip.py'), '-u', username]);
        }
        sp.stdout.on('data', function (data) {
            console.log('stdout: ' + data.toString());
        });
        sp.stderr.on('data', function (data) {
            console.error('stderr: ' + data.toString());
        });
    } else {
      console.log('Clip Command is Cool-Time: ' + now - lastCommanded[username]);
    }
}

module.exports = uploadClip