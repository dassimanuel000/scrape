const { PythonShell } = require('python-shell');

let options = {
    pythonPath: 'python3.10',
    args: ['28','08'] //An argument which can be accessed in the script using sys.argv[1]
};

let pyshell = new PythonShell('3posteurHeadless.py', options);
    
pyshell.on('message', function (message) {
    console.log(message);
});

pyshell.end(function (err, code, signal) {
    if (err) throw err;
    console.log('The exit code was: ' + code);
    console.log('The exit signal was: ' + signal);
    console.log('finished');
});