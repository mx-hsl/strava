# This is a sample Python script.
# Medium Blog https://medium.com/swlh/using-python-to-connect-to-stravas-api-and-analyse-your-activities-dummies-guide-5f49727aac86

import requests
import json
import ssl
from configparser import ConfigParser
import time
import pandas as pd

config = ConfigParser()
config.read('config.ini')
client_id = eval(config['strava']['client_id'])
client_secret = config['strava']['client_secret']
url_auth = "https://www.strava.com/oauth/authorize"
url_token = "https://www.strava.com/oauth/token"
url_activites = "https://www.strava.com/api/v3/activities"


def auth():
    data = {"client_id": client_id,
            "redirect_uri": "localhost",
            "response_type": "code",
            "approval_prompt": "auto",
            "scope": "activity:read_all"
            }

    r = requests.get(url_auth, data)
    print(r)

def update_tokens():
    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': "refresh_token",
        'f': 'json'
    }

    print("Requesting Token...\n")
    new_strava_tokens = requests.post(url_auth, data=payload, verify=False)
    with open('strava_tokens.json', 'w') as outfile:
        json.dump(new_strava_tokens, outfile)
        print("updated token json file")
    strava_tokens = new_strava_tokens
    return strava_tokens


def first_auth():
    # code must be found out manually with this URL:
    # url = https://www.strava.com/oauth/authorize?client_id=80669&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=profile:read_all,activity:read_all
    code = 'code must be found out manually'
    response = requests.post(
        url=url_token,
        data={
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'grant_type': 'authorization_code'
        }
    )  # Save json response as a variable
    strava_tokens = response.json()  # Save tokens to file
    with open('strava_tokens.json', 'w') as outfile:
        json.dump(strava_tokens, outfile)  # Open JSON file and print the file contents
    # to check it's worked properly
    with open('strava_tokens.json') as check:
        data = json.load(check)
        print(data)


def get_activities():
    # Loop through all activities
    page = 1
    ## Create the dataframe ready for the API call to store your activity data
    activities_df = pd.DataFrame(
        columns=[
            "id",
            "name",
            "kudos_count",
            "start_date_local",
            "type",
            "distance",
            "moving_time",
            "elapsed_time",
            "total_elevation_gain",
            "end_latlng",
            "external_id"
        ]
    )
    while True:

        # get page of activities from Strava
        r = requests.get(url_activites + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(page))
        r = r.json()  # if no results then exit loop
        if (not r):
            break

        # otherwise add new data to dataframe
        for x in range(len(r)):
            activities_df.loc[x + (page - 1) * 200, 'id'] = r[x]['id']
            activities_df.loc[x + (page - 1) * 200, 'name'] = r[x]['name']
            activities_df.loc[x + (page - 1) * 200, 'kudos_count'] = r[x]['kudos_count']
            activities_df.loc[x + (page - 1) * 200, 'start_date_local'] = r[x]['start_date_local']
            activities_df.loc[x + (page - 1) * 200, 'type'] = r[x]['type']
            activities_df.loc[x + (page - 1) * 200, 'distance'] = r[x]['distance']
            activities_df.loc[x + (page - 1) * 200, 'moving_time'] = r[x]['moving_time']
            activities_df.loc[x + (page - 1) * 200, 'elapsed_time'] = r[x]['elapsed_time']
            activities_df.loc[x + (page - 1) * 200, 'total_elevation_gain'] = r[x]['total_elevation_gain']
            activities_df.loc[x + (page - 1) * 200, 'end_latlng'] = r[x]['end_latlng']
            activities_df.loc[x + (page - 1) * 200, 'external_id'] = r[x]['external_id']  # increment page
        page += 1
        activities_df.to_csv('strava_activities.csv')
        print('Strava Activities have been updated')
        return activities_df


if __name__ == '__main__':
    with open('strava_tokens.json') as tokens:
        data = json.load(tokens)

        ## If access_token has expired then use the refresh_token to get the new access_token
        if data['expires_at'] < time.time():
            data = update_tokens()
        refresh_token = data["refresh_token"]
        access_token = data["access_token"]

        activities_df = get_activities()
        print(activities_df)


