from flask import Flask, redirect, request, jsonify
from requests_oauthlib import OAuth2Session

app = Flask(__name__)

CLIENT_ID = '1234snd.apps.googleusercontent.com'
CLIENT_SECRET = '1234'
REDIRECT_URI = 'http://localhost:5000/oauth2callback'

# Google OAuth2 endpoints
AUTHORIZATION_BASE_URL = 'https://accounts.google.com/o/oauth2/auth'
TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
SCOPE = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']


@app.route('/')
def home():
    return 'Домашняя страница. <a href="/login">Войти через Google</a>.'


@app.route('/login')
def login():
    google = OAuth2Session(CLIENT_ID, scope=SCOPE, redirect_uri=REDIRECT_URI)
    authorization_url, state = google.authorization_url(AUTHORIZATION_BASE_URL, access_type="offline",
                                                        prompt="select_account")

    return redirect(authorization_url)


@app.route('/oauth2callback')
def callback():
    google = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    google.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=request.url)

    userinfo_response = google.get('https://www.googleapis.com/oauth2/v1/userinfo')
    userinfo = userinfo_response.json()

    return jsonify(userinfo)


if __name__ == '__main__':
    app.run(debug=True)
