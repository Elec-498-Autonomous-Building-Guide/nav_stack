import json

# Fake backend

def getRoomsList():
    # Temp until integration with Roomba
    with open("Rooms.json","r") as open_file:
        data = json.load(open_file)
    return data;

def listByFloor(floor):
    data = getRoomsList()
    rooms = []
    for i in data["Rooms"]:
        f = str(i['floor'])
        if f == floor:
             rooms.append(str(i["room"]))
    return rooms

def getObstackeList():
    with open("obstacles.json","r") as f:
        data = json.load(f)
    return data["Obstacles"];

def sendRoom(room):
    pass
