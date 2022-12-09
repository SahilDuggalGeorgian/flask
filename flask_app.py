from flask import Flask, request, render_template
from flask_pymongo import PyMongo
import urllib.request, json

app = Flask(__name__)

app.config[
    "MONGO_URI"
] = "mongodb+srv://Sahil123:Sahil123@cluster0.o8ni1b2.mongodb.net/myFirstDb?retryWrites=true&w=majority"

# Setup Mongodb
mongodb_client = PyMongo(app)
db = mongodb_client.db


@app.route("/")
def index():
    db.days.drop()
    url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/barrie?unitGroup=us&key=CD9QP9TXZ7RC7ZC8PRVCGJFUA&contentType=json"
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    days = dict["days"]
    db.days.insert_many(days)
    return render_template("index.html")


@app.route("/piechart")
def piechart():
    days1 = [["Date", "Temperature"]]
    cursor = db.days.find({})
    for document in cursor:
        days1.append([document["datetime"], document["tempmax"]])
    return render_template("pie-chart.html", data=days1)


if __name__ == "__main__":
    app.run()
