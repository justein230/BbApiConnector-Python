from bottle import route, run, template, request
import requests
import json
from configparser import ConfigParser

config_file_name = 'app_secrets.ini'
config = ConfigParser()
config.read(config_file_name)

@route('/')
def index():
    print_string = f'''
        Welcome to the Blackbaud SKY API Authorization Code Generator!
        <br><br>
        Please go to this URL: <a href="https://oauth2.sky.blackbaud.com/authorization?client_id={config['app_secrets']['app_id']}&response_type=code&redirect_uri={config['other']['redirect_uri']}">https://oauth2.sky.blackbaud.com/authorization?client_id={config['app_secrets']['app_id']}&response_type=code&redirect_uri={config['other']['redirect_uri']}</a>
    '''

    return print_string

@route('/callback')
def callback():
    auth_code = request.query.code
    get_access_refresh_tokens(auth_code)
    return template('Your code is {{auth_code}}', auth_code=auth_code)

def get_access_refresh_tokens(auth_code):
    token_uri = f'https://oauth2.sky.blackbaud.com/token'
    params = {
        'grant_type': 'authorization_code',
        'redirect_uri': config['other']['redirect_uri'],
        'code': auth_code,
        'client_id': config['app_secrets']['app_id'],
        'client_secret': config['app_secrets']['app_secret']
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    codes = requests.post(token_uri, data=params, headers=headers)
    print(codes.request.headers)
    print(codes.text)

run(host='localhost', port=13631, debug=True)