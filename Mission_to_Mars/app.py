from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_news = mongo.db.mars_news.find_one()

    # Return template and data
    return render_template("index.html", mars_news=mars_news)


@app.route("/scrape")
def scrape():
    mars_news = mongo.db.mars_news
    mars = scrape_mars.scrape()
    mars_news.update({}, mars, upsert=True)
    # Redirect back to homepage
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
