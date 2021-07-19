# -------------------------------------------
# Name: AUTOMATION UNFOLLOW
# Portfolio: https://tovinhkhang.netlify.app
# -------------------------------------------

# IMPORT
import requests
import json
import argparse
import tqdm
import time
from base64 import b64encode
from datetime import datetime

# INPUT ARG
ap = argparse.ArgumentParser();
ap.add_argument('-t', '--token', required=True);
ap.add_argument('-m', '--my-username', required=True);
ap.add_argument('-f', '--file');
ap.add_argument('-mf','--max-followers');
args = ap.parse_args();

# RESPONE AUTH
HEADERS = {"Authorization": "Basic " + b64encode(str(args.my_username + ":" + args.token).encode('utf-8')).decode('utf-8')}
res = requests.get("https://api.github.com/user", headers=HEADERS);
if(res.status_code != 200):
    print("Failure to Authenticate! Please check PersonalAccessToken and Username!");
    exit(1);
else:
    print("Authentication Succeeded!");
	
# SESSION HEADER
sesh = requests.session();
sesh.headers.update(HEADERS);

# OUTPUT JSON FILE WITH USERS DATA FOLLOWING
if not args.file:
    target = args.my_username;
    res = sesh.get("https://api.github.com/users/" + target + "/following");
    linkArray = requests.utils.parse_header_links(res.headers['Link'].rstrip('>').replace('>,<', ',<'));
    url = linkArray[1]['url'];
    lastPage = url.split('=')[-1];
    followerArray = [];
    maxFollowers = args.max_followers;
    print('Grabbing People to unfollow\nThis may take a while... there are ' + str(lastPage) + ' pages to go through.');
    for page in tqdm.tqdm(range(1, int(lastPage)), ncols=35, smoothing=True, bar_format='[PROGRESS] {n_fmt}/{total_fmt} | {bar}'):
        res = sesh.get('https://api.github.com/users/' + target + "/following?limit=100&page=" + str(page)).json();
        for user in res:
            followerArray.append(user['login']);
        if(maxFollowers != None):
            if(len(followerArray) >= int(maxFollowers)):
                break;
    outputJsonFile = str(datetime.now().strftime('%m-%d-%Y')) + "-Total-" + str(len(followerArray)) + ".json";
    with open(outputJsonFile, 'w+') as f:
        json.dump(followerArray, f, indent=4);
else:
    outputJsonFile = args.file;

# READ JSON FILE TO STARTING UNFOLLOW
with open(outputJsonFile, 'r+') as f:
    data = json.load(f);
    print("Starting to Unfollow Users...");
    for user in tqdm.tqdm(data, ncols=35, smoothing=True, bar_format='[PROGRESS] {n_fmt}/{total_fmt} | {bar}'):
        while(True):
            time.sleep(2);
            res = sesh.delete('https://api.github.com/user/following/' + user);
            if(res.status_code != 204):
                print("Rate-limited, please wait until it finish!");
                time.sleep(60);
            else:
                break;
# ------
#  END
# ------
