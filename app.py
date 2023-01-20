from flask import Flask


import subprocess


app = Flask(__name__)

is_bot_running = False

def display_log(path):
    return open(path).read().replace("\n", "<br>")

@app.route('/bot_log')
def bot_log():
    site = "<h1>Mensa Mining Bot Log</h1>"

    site += "<div id=\"log\">" + display_log("app/log/botlog.txt") + "</div>"

    return site

@app.route('/init')
def init():
    global is_bot_running
    if not is_bot_running:
        subprocess.Popen(["python", "app/main.py"]) 
    site = "<h1>initiate Bot!</h1>"
    print("initiated Bot")
    is_bot_running = True
    return site

@app.route('/')
def index():
    text = ""
    if is_bot_running:
        text+= "<h1>Bot is running...</h1>"
    else:
        text+= "<h1>Bot is offline.</h1>"
    text+= "<div id=\"content\"> <p>Links to Administration:</p><ul> <li><a href=\"init\">init Bot</a></li><li><a href=\"bot_log\">Bot Log</a></li></ul></div>"
    return text


index()
