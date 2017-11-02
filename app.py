#! /usr/bin/env python3

import flask
import subprocess
import time

app = flask.Flask("cowsay magnificent")

@app.route('/cowsay_alpha')
def fun1():
    def inner():
        proc = subprocess.Popen(
            ['./cowsay-fun.sh'],
            stdout=subprocess.PIPE,
            shell=True
        )

        for line in iter(proc.stdout.readline,''):
            yield line.rstrip().decode('utf-8') + '<br/>\n'
            time.sleep(0.1)
    
    return flask.Response(inner(), mimetype='text/html')

@app.route('/cowsay_beta')
def fun2():
    def inner():
        proc = subprocess.Popen(
            ['./cowsay-vader.sh'],
            stdout=subprocess.PIPE,
            shell=True
        )

        for line in iter(proc.stdout.readline,''):
            yield line.rstrip().decode('utf-8') + '<br/>\n'
            time.sleep(0.1)
    
    return flask.Response(inner(), mimetype='text/html')


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
