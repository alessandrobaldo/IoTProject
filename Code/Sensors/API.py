from flask import Flask, redirect
from iHealth import iHealth
import apiconfig as cfg

app = Flask(__name__)
client_id = cfg.CLIENT_ID
client_secret = cfg.CLIENT_SECRET
callback = cfg.CALLBACK_URI
api = iHealth(client_id, client_secret, callback)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/authorize')
def authorize():
    r = api.authorize()
    return redirect(r.url)

@app.route('/callback')
def callback():
    r = api.callback()
    return r

@app.route('/api_bp')
def api_bp():
    r = api.get_blood_pressure()
    return r

@app.route('/api_weight')
def api_weight():
    r = api.get_weight()
    return r

@app.route('/api_blood_oxygen')
def api_blood_oxygen():
    r = api.get_blood_oxygen()
    return r

if __name__ == '__main__':

    app.route('/authorize')
    app.route('/callback')
    app.route('/api_blood_oxygen')