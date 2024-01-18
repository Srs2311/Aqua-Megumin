import datetime
import json

def refresh_events():
    with open ("./json/events.json","r") as events_json:
        events = json.load(events_json)
        event_names = []
        for event in events:
            event_names.append(event["name"])
        return events,event_names


def add_countdown(bot,message):
    events,event_names =  refresh_events()
    countdownInfo = str(message.text).replace("/addCountdown ","")
    countdownInfo = countdownInfo.split("|")
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
            bot.send_message(message.chat.id,f"Added countdown: {countdown_json["name"]}")
    
def countdown(bot,message):
    events,event_names =  refresh_events()
    countdown_name = str(message.text).replace("/countdown ","")
    for event in events:
        if countdown_name.lower() in event["name"].lower():
            td = datetime.datetime(int(event["year"]),int(event["month"]),int(event["day"]),int(event["hour"]),int(event["minute"]),int(event["seconds"])) - datetime.datetime.now()
            hms = str(datetime.timedelta(seconds=td.seconds))
            hms = hms.split(":")
            bot.send_message(message.chat.id,f"{event["name"]} in {td.days} days {hms[0]} hours {hms[1]} minutes {hms[2]} seconds")
