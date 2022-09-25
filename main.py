from flask import Flask
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


#data: 1 = level start, 2 = level win, 3 = level lose
def dataUpdatation(data_details,level, data):

    print("Update with level "+level+" and data "+data)

    myquery = { "_id": level }
    newvalues = { "$set": {} }

    if data == '1':
        newvalues["$set"]["startLevCount"] = data_details["startLevCount"]+1
    elif data == '2':
        newvalues["$set"]["winLevCount"] = data_details["winLevCount"]+1
    else:
        newvalues["$set"]["loseLevCount"] = data_details["loseLevCount"]+1

    user_collection.update_one(myquery, newvalues)


def dataInsertion(data_details,level, data):

    print("First Insert with level "+level+" and data "+data)

    data_details["_id"] = level

    if data == '1':
        data_details["startLevCount"] = 1
        data_details["winLevCount"] = 0
        data_details["loseLevCount"] = 0
    elif data == '2':
        data_details["startLevCount"] = 0
        data_details["winLevCount"] = 1
        data_details["loseLevCount"] = 0
    else:
        data_details["startLevCount"] = 0
        data_details["winLevCount"] = 0
        data_details["loseLevCount"] = 1

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