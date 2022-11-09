import json
from enum import Enum

from flask import Flask, redirect, url_for, jsonify
from flask_cors import CORS
from firebase_admin import credentials, firestore, initialize_app

app = Flask(__name__)
CORS(app)

cred = credentials.Certificate("cs526-analytics-firebase-adminsdk.json")
initialize_app(cred)
db = firestore.client()
analytics_ref = db.collection('analytics').document("analytics_data")
leaderboard_collection = db.collection('leaderboard')

NUM_LEVEL = 11


def init():
    init_analytics_ref()
    init_leaderboard_ref()


def init_analytics_ref():
    if not analytics_ref.get().exists:
        analytics_ref.set({})


def init_leaderboard_ref():
    for level in range(NUM_LEVEL + 1):
        leaderboard_ref = leaderboard_collection.document("lv_{}".format(level))
        if not leaderboard_ref.get().exists:
            leaderboard_ref.set({})


class Attributes(Enum):
    startLevCount = 1
    winLevCount = 2
    loseLevCount = 3
    wallBreakUsed = 4
    launchpadUsed = 5
    enemiesRespawned = 6
    playerDistance = 7


class Graphs(Enum):
    death = {"attrs": [Attributes.loseLevCount], "levels": '*'}
    start_finish = {"attrs": [Attributes.startLevCount, Attributes.winLevCount], "levels": '*'}
    wall_breaker_used = {"attrs": [Attributes.wallBreakUsed], "levels": [2, 3, 7]}
    launch_pad_used = {"attrs": [Attributes.launchpadUsed], "levels": [2, 5, 6, 7, 8, 9, 11]}
    enemy_respawned = {"attrs": [Attributes.enemiesRespawned], "levels": '*'}
    player_distance = {"attrs": [Attributes.playerDistance], "levels": '*'}


@app.route("/test")
def test():
    return "Service is up duhhhh!!!!!"


@app.route('/home')
def homepage():
    return redirect(url_for('static', filename='home.html'))


@app.route('/update_leaderboard/<string:username>/<int:level>/<int:time>')
def update_leaderboard(username, level, time):
    if level > NUM_LEVEL:
        return 'invalid level', 418

    leaderboard_ref = leaderboard_collection.document("lv_{}".format(level))
    leaderboard_lv_data = leaderboard_ref.get().to_dict()
    if username not in leaderboard_lv_data or time < leaderboard_lv_data[username]:
        leaderboard_lv_data[username] = time
        leaderboard_ref.update(leaderboard_lv_data)
    return "Done"


@app.route('/leaderboard/<int:level>')
def get_leaderboard(level):
    if level > NUM_LEVEL:
        return 'invalid level', 418
    leaderboard = leaderboard_collection.document("lv_{}".format(level)).get().to_dict()
    sorted_lb = sorted([[k, v] for k, v in leaderboard.items()], key=lambda x: x[1])
    return jsonify({"Items": [{"username": k, "time": v} for k, v in sorted_lb]})


@app.route('/update/<string:level_id>/<string:attr_id>')
def update(level_id, attr_id, attr_val=1):
    init()
    if int(level_id) > NUM_LEVEL:
        return "Error in updating level " + level_id
    level = "level_" + level_id
    analytics_data = analytics_ref.get().to_dict()
    attr_name = Attributes(int(attr_id)).name

    if level not in analytics_data:
        analytics_data[level] = {}

    analytics_data[level][attr_name] = analytics_data[level].get(attr_name, 0) + attr_val
    analytics_ref.update(analytics_data)
    return "Done"


@app.route('/distance/<string:level_id>/<string:attr_val>')
def dist(level_id, attr_val):
    return update(level_id, 7, attr_val)


def get_graph_data(graph):
    init()
    graph_attr = graph.value
    attrs, levels = graph_attr['attrs'], graph_attr['levels']
    arr = [[0 for j in range(NUM_LEVEL + 1)] for i in range(len(attrs))]
    for level, level_data in analytics_ref.get().to_dict().items():
        level_id = int(level.split("_")[-1])
        for i, attr in enumerate(attrs):
            arr[i][level_id] = level_data.get(attr.name, 0)

    if levels == '*':
        levels = [x for x in range(NUM_LEVEL + 1)]

    res = {"level": levels}

    for i, attr in enumerate(attrs):
        res[attr.name] = arr[i] if levels == '*' else [arr[i][x] for x in levels]

    return jsonify(res)


@app.route('/deathData')
def getDeathData():
    return get_graph_data(Graphs.death)


@app.route('/startFinishData')
def getStartFinishData():
    return get_graph_data(Graphs.start_finish)


@app.route('/wallBreakUsedData')
def getWallBreakUsedCount():
    return get_graph_data(Graphs.wall_breaker_used)


@app.route('/launchpadUsedData')
def getLaunchpadUsedCount():
    return get_graph_data(Graphs.launch_pad_used)


@app.route('/enemyRespawnData')
def getEnemyRespawnCount():
    return get_graph_data(Graphs.enemy_respawned)


@app.route('/playerDistanceData')
def getPlayerDistanceCount():
    return get_graph_data(Graphs.player_distance)


if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run()
