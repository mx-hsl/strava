# This is a sample Python script.
import requests
import json
import ssl
from configparser import ConfigParser

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

config = ConfigParser()
config.read('config.ini')
client_id = config['strava']['client_id']
client_secret = config['strava']['client_secret']
refresh_token = config['strava']['refresh_token']
url_auth = "https://www.strava.com/oauth/authorize"
url_token = "https://www.strava.com/oauth/token"


def token_exchange():
    data = {"client_id": client_id,
            "client_secret": client_secret,
            "code": "code",
            "grant_type": "authorization_code"
            }
    r = requests.post(url_token, data)
    print(r)

def token_refresh():
    data = {"client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
            }
    r = requests.post(url_token,
                      data)
    print(r)



def auth():
    data = {"client_id": client_id,
            "redirect_uri": "localhost",
            "response_type": "code",
            "approval_prompt": "auto",
            "scope": "activity:read_all"
            }

    r = requests.get(url_auth, data)
    print(r)

def access_strava():
    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    auth_url = "https://www.strava.com/oauth/token"
    activites_url = "https://www.strava.com/api/v3/activities"

    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': "refresh_token",
        'f': 'json'
    }

    print("Requesting Token...\n")
    res = requests.post(auth_url, data=payload, verify=False)
    access_token = res.json()['access_token']
    print("Access Token = {}\n".format(access_token))

    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': 200, 'page': 1}
    my_dataset = requests.get(activites_url + '?access_token=' + access_token).json()

    print(my_dataset[0]["name"])
    print(my_dataset[0]["map"]["summary_polyline"])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context

    #access_strava()
    #s = requests.session()
    token_exchange()
    #token_refresh()
    #auth()


