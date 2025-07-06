from datetime import datetime, timezone
import json
import requests
import math

# Script looks up information in cached tarkov.dev database
# Last updated time is the time since last look up on their website, not using external API methods

profileID = "12400636"

def LookUpInTargetPath(path, json):
    keys = path.split(".")
    current = json

    try:
        for key in keys:
            if isinstance(current, dict):
                current = current[key]
            elif isinstance(current, list):
                try:
                    index = int(key)
                    current = current[index]
                except (ValueError, IndexError):
                    return None
            else:
                return None
        return current
    except (KeyError, TypeError):
        return None

def CalculateTime(time):
    fix_unix = str(time)[:-3]
    
    profile_time = datetime.fromtimestamp(int(fix_unix), tz=timezone.utc)
    current_time = datetime.now(timezone.utc)
    
    time_diff = current_time - profile_time
    
    days = time_diff.days
    hours, remainder = divmod(time_diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if days > 0:
        return f"{days}d,{hours}h" if hours > 0 else f"{days}d"
    elif hours > 0:
        return f"{hours}h,{minutes}m" if minutes > 0 else f"{hours}h"
    elif minutes > 0:
        return f"{minutes}m"
    else:
        return f"{seconds}s"

def LookUpProfileData(profile):
    formatURL = "https://players.tarkov.dev/profile/" + profile + ".json"
    # print(formatURL)
    try:
        response = requests.get(formatURL)
        response.raise_for_status()
        returnJSON = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {formatURL}: {e}")
        return None
    
    nicknameTargetPath = "info.nickname"
    nickname = LookUpInTargetPath(nicknameTargetPath, returnJSON)
    print(nickname)

    timeTargetPath = "updated"
    time = LookUpInTargetPath(timeTargetPath, returnJSON)
    print(f"Last updated at: {CalculateTime(time)}")
    
LookUpProfileData(profileID)
