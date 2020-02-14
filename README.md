# Blackbaud SKY API Key Generator/Manager
This code is used by me to securely authenticate to the Blackbaud SKY API for local applications. I'm hoping it can be useful for others as well!

# Components
I found it helpful for me to split the functionality into two files: one for when you have no refresh token, and then one for when you do have one.
- For the authorization code generator, a simple HTTP server is needed in order to receive the code from Blackbaud. I used the Bottle framework, since it is easy to use and lightweight. It relies only on standard Python libraries!
- For the API connector program, I create a Session object and use a config file for storing all the secrets, keys, tokens and other supporting information.

## Prerequisites
- Clone my repository to your local machine, and create a Python virtual environment. Then, when the virtual environment is activated, run `pip install bottle`. This will install all the libraries from pip that you need to run the auth code generator (`bb_auth.py` in resources).
- Paste your Application ID and Application Secret into the placeholders in `app_secrets.ini`. These will be used for authorization and authentication throughout the process. Also, paste your Blackbaud API Subscription Key in the placeholder in `app_secrets.ini`.
- Choose a URL to use for testing auth codes and set it in `test_api_endpoint` field in `app_secrets.ini`. I arbitrarily picked the `Role list` endpoint in the School API for my purposes, but you can pick any endpoint you wish.
- If you are an environment admin, make sure that you have connected your application to the environment from which you want to pull data. If you are not an environment admin, ask your administrator to connect your SKY API application. Instructions on how to do this are [here](https://developer.blackbaud.com/skyapi/docs/createapp). Just to clarify, steps 1 and 2 of this guide are to be performed by you (the application creator), and steps 3 and 4 are to be completed by an environment admin.
- Port 13631 is used on the local machine to run the web server. Make sure that [here](https://developer.blackbaud.com/apps/), in your application settings, under Redirect URIs, that you have `http://localhost:13631/callback` as an option.

## Obtain Authorization Code to Get Tokens
1. Once the prerequisite steps are completed, run the authorization code generator component (`bb_auth.py`).
2. When the application is running, go to `http://localhost:13631`. Here, you will find the link that you need to go to in order to authorize your application with your credentials.
3. Sign in with your Blackbaud ID, then click "Authorize". You should be taken to a screen with your authorization code. If you look at the console of the application, you will see a very long access token and a much shorter refresh token. Copy these values and paste them in `app_secrets.ini`.
4. Once you have copied these values into the config file, you can terminate the bb_auth application.


## Install the BbApiConnector library using the .whl file
1. Find the .whl file under Releases in GitHub and download the file.
2. Either using the virtual enviornment created earlier for bb_auth, or a new virtual environment, install the .whl file by running the following command: `pip install <filename>.whl`.

## Set Up a Session for Use in Python Programs
1. When all placeholders in the `app_secrets.ini` file are filled (which they should be at this point), you are ready to start authenticating with the SKY API!
2. In your program, add `from BbApiConnector import BbApiConnector` to the top of your program.
3. Create a BbApiConnector object and pass in the config file path, like so: `api_conn = BbApiConnector('app_secrets.ini')`
4. In order to use the API, use the pre-authorized Session object created with this script. add the line `bb_session = api_conn.get_session()` near the top of your file.
5. You are done! In order to use the API, use bb_session like you would the normal requests library. No headers need to be specified. An example request is located below:
```python
params = {
    'base_role_ids': '1'
}
req = bb_session.get("https://api.sky.blackbaud.com/school/v1/users/extended", params=params)
```

Happy API'ing! Please feel free to report any issues with the code in the Issues section, or contribute yourself with a Pull Requests. Note that this is a personal project of mine, and I will only review Issues and Pull Requests when time allows.
