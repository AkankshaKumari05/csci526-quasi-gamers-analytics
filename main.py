from operator import le
from flask import Flask, jsonify, redirect, url_for
import pandas as pd
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

@app.route('/home')
def homepage():
    return redirect(url_for('static', filename='home.html'))

@app.route('/update/<string:count>')
def updateNumberOfUser(count):
    return "You bet its done"+count

@app.route('/getuserNumberStartGame/<string:count>')
def userNumberStartGame(count):
    df = pd.read_csv("data.csv", sep=" ", header=None, 
                 names=["Features", "Value"])
    if count == "1"  :
        print (df['Value'][0])
    else:
        print("wrong")
  
    
    getDB()
    print(df['Features'])
    return "Updated"
   
def getDB():
    try:
        connection = mysql.connector.connect(host='104.154.96.134',
                                            database='quasi-gamers',
                                            user='root',
                                            password='9DI/NTiD&-2UU10f')
        if connection.is_connected():
            print("Connected to MySQL Server version ")
            cursor = connection.cursor()
            print("You're connected to database: ")
            closeDB(connection, cursor)
    except Error as e:
        print("Error while connecting to MySQL", e)

def closeDB(connection, cursor):
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
if __name__ == "__main__":
    app.run()