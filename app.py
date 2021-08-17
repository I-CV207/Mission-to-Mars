#We will use Falsk to render a template, redirecting to another URL and creating an URL
from flask import Flask, render_template, redirect, url_for
#We will use Pymongo to interact with our mongo database
from flask_pymongo import PyMongo
#To use the scrapping code, we will convert from jupyter notebook to Python
import scraping

#Set up Flask
app=Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"

mongo = PyMongo(app)

#1. app.config["MONGO_URI"] tells Python that our app will connect to Mongo 
#   using a URI, a uniform resource identifier similar to a URL.

#2. "mongodb://localhost:27017/mars_app" is the URI we'll be using to 
#   connect our app to Mongo. 
#   This URI is saying that the app can reach Mongo through our localhost server, 
#   using port 27017, using a database named "mars_app".

@app.route("/")
def index():
    mars=mongo.db.mars.find_one()
    return render_template("index.html",mars=mars)

#1. This route, @app.route("/"), tells Flask what to display 
#   when we're looking at the home page, index.html     

#2. mars = mongo.db.mars.find_one() uses PyMongo to find the "mars" collection in our database.

#3. return render_template("index.html" tells Flask to return an HTML template using an index.html file. 

#4. mars=mars) tells Python to use the "mars" collection in MongoDB.
#   This function is what links our visual representation of our work, our web app, to the code that powers it.

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
# We're inserting data, so first we'll need to add an empty JSON object 
# with {} in place of the query_parameter. Next, we'll use the data we 
# have stored in mars_data. Finally, the option we'll include is upsert=True. 
# This indicates to Mongo to create a new document if one doesn't already 
# exist, and new data will always be saved (even if we haven't already 
# created a document for it).

   return redirect('/', code=302)
# Finally, we will add a redirect after successfully scraping the data: 
# return redirect('/', code=302). This will navigate our page back to / where 
# we can see the updated content. 
if __name__=="main":
    app.run()  