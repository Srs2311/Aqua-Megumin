import datetime
import json

def refresh_events():
    with open ("./json/events.json","r") as events_json:
        events = json.load(events_json)
        event_names = []
        for event in events:
            event_names.append(event["name"])
        return events,event_names


def add_countdown(message):
    events,event_names =  refresh_events()
    if "/addCountDown" in message:
        countdownInfo = str(message).replace("/addCountDown ","")
    elif "/addCountdown" in message:
        countdownInfo = str(message).replace("/addCountdown ","")
    elif "/addcountdown" in message:
        countdownInfo = str(message).replace("/addcountdown ","")
    elif "/add_countdown" in message:
        countdownInfo = str(message).replace("/add_countdown ","")
    
    countdownInfo = countdownInfo.split("|")
    print(countdownInfo)
    mdy = countdownInfo[1].strip().split("/")
    
    countdown_json = {}
    countdown_json["name"] = countdownInfo[0]
    if countdown_json["name"] not in event_names:
        countdown_json["year"] = mdy[2]
        countdown_json["month"] = mdy[0]
        countdown_json["day"] = mdy[1]
    
        if len(countdownInfo) > 2:
            hms = countdownInfo[2].split(":")
            if len(hms) == 3:
                countdown_json["hour"] = hms[0]
                countdown_json["minute"] = hms[1]
                countdown_json["seconds"] =hms[2]
            elif len(hms) == 2:
                countdown_json["hour"] = hms[0]
                countdown_json["minute"] = hms[1]
                countdown_json["seconds"] = 0
            elif len(hms) == 1:
                countdown_json["hour"] = hms[0]
                countdown_json["minute"] = 0
                countdown_json["seconds"] = 0
        else:
            countdown_json["hour"] = 0
            countdown_json["minute"] = 0
            countdown_json["seconds"] = 0
        events.append(countdown_json)
        with open("./json/events.json","w") as events_file:
            events_file.write(json.dumps(events))
            response = f"Added countdown: {countdown_json["name"]}"
    return(response)
    
def countdown(message):
    events,event_names =  refresh_events()
    countdown_name = str(message).replace("/countdown ","")
    for event in events:
        if countdown_name.lower() in event["name"].lower():
            td = datetime.datetime(int(event["year"]),int(event["month"]),int(event["day"]),int(event["hour"]),int(event["minute"]),int(event["seconds"])) - datetime.datetime.now()
            hms = str(datetime.timedelta(seconds=td.seconds))
            hms = hms.split(":")
            response = f"{event["name"]} in {td.days} days {hms[0]} hours {hms[1]} minutes {hms[2]} seconds"
    if response:
        return response
    else:
        return("Could not find countdown")