import json
from operator import ne
from flask import Flask, redirect, url_for
from service import db, user_collection

app = Flask(__name__)

@app.route("/test")
def test():
    return "Service is up duhhhh!!!!!"
    

@app.route('/home')
def homepage():
    return redirect(url_for('static', filename='home.html'))


@app.route('/update/<string:level>/<string:data>')
def update(level, data):
    status, data_details =  checkLevelExits(level)
    if status:
        dataUpdatation(data_details,level, data)
    else:
        dataInsertion(data_details,level, data)
    return "Done"


@app.route('/deathData')
def getDeathData():
    cursor = user_collection.find()
    total_death = {}
    level = []
    levelDeathCount = []
    for next in cursor:
        level.append(int(next["_id"]))
        levelDeathCount.append(next["loseLevCount"])
    total_death["level"] = level
    total_death["deathCount"] = levelDeathCount 

    res = json.dumps(total_death, indent=4)
    return res


@app.route('/startFinishData')
def getStartFinishData():
    cursor = user_collection.find()
    data = {}
    level = []
    levelFinishCount = []
    levelStartCount = []
    for next in cursor:
        level.append(int(next["_id"]))
        levelFinishCount.append(next["winLevCount"])
        levelStartCount.append(next["startLevCount"])
    data["level"] = level
    data["startCount"] = levelStartCount 
    data["finishCount"] = levelFinishCount 
    res = json.dumps(data, indent=4)
    return res

@app.route('/wallBreakUsedData')
def getWallBreakUsedCount():
    cursor = user_collection.find()
    wallBreakUsed = {}
    level = []
    breakUsedCount = []
    for next in cursor:
        if int(next["_id"]) == 3:
            level.append(int(next["_id"]))
            breakUsedCount.append(next["wallBreakUsed"])
    wallBreakUsed["level"] = level
    wallBreakUsed["wallBreakUsed"] = breakUsedCount 
    res = json.dumps(wallBreakUsed, indent=4)
    return res

@app.route('/launchpadUsedData')
def getLaunchpadUsedCount():
    cursor = user_collection.find()
    launchpadUsed = {}
    level = []
    launchpadUsedCount = []
    for next in cursor:
        if int(next["_id"]) in [2, 4, 5]:
            level.append(int(next["_id"]))
            launchpadUsedCount.append(next["launchpadUsed"])
    launchpadUsed["level"] = level
    launchpadUsed["launchpadUsed"] = launchpadUsedCount 
    res = json.dumps(launchpadUsed, indent=4)
    return res

#data: 1 = level start, 2 = level win, 3 = level lose
def dataUpdatation(data_details,level, data):

    print("Update with level "+level+" and data "+data)

    myquery = { "_id": level }
    newvalues = { "$set": {} }

    if data == '1':
        newvalues["$set"]["startLevCount"] = data_details["startLevCount"]+1
    elif data == '2':
        newvalues["$set"]["winLevCount"] = data_details["winLevCount"]+1
    elif data == "3":
        newvalues["$set"]["loseLevCount"] = data_details["loseLevCount"]+1
    elif data == "4":
        newvalues["$set"]["wallBreakUsed"] = data_details["wallBreakUsed"]+1
    elif data == "5":
        newvalues["$set"]["launchpadUsed"] = data_details["launchpadUsed"]+1

    user_collection.update_one(myquery, newvalues)


def dataInsertion(data_details,level, data):

    print("First Insert with level "+level+" and data "+data)

    data_details["_id"] = level

    if data == '1':
        data_details["startLevCount"] = 1
        data_details["winLevCount"] = 0
        data_details["loseLevCount"] = 0
        data_details["wallBreakUsed"] = 0
        data_details["launchpadUsed"] = 0
    elif data == '2':
        data_details["startLevCount"] = 0
        data_details["winLevCount"] = 1
        data_details["loseLevCount"] = 0
        data_details["wallBreakUsed"] = 0
        data_details["launchpadUsed"] = 0
    elif data == "3":
        data_details["startLevCount"] = 0
        data_details["winLevCount"] = 0
        data_details["loseLevCount"] = 1
        data_details["wallBreakUsed"] = 0
        data_details["launchpadUsed"] = 0
    elif data == "4":
        data_details["startLevCount"] = 0
        data_details["winLevCount"] = 0
        data_details["loseLevCount"] = 0
        data_details["wallBreakUsed"] = 1
        data_details["launchpadUsed"] = 0
    elif data == "5":
        data_details["startLevCount"] = 0
        data_details["winLevCount"] = 0
        data_details["loseLevCount"] = 0
        data_details["wallBreakUsed"] = 0
        data_details["launchpadUsed"] = 1

    user_collection.insert_one(data_details)


def checkLevelExits(level):

    cursor = user_collection.find({"_id":level})
    res_details = []

    for next in cursor:
        res_details.append(next)

    if len(res_details) == 0:
        return False, {}

    return True, res_details[0]


if __name__ == "__main__":
    
    app.config['DEBUG'] = True
    app.run()