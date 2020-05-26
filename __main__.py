import os
import pickle

from flask import Flask, request, jsonify, render_template
import numpy as np


# First try to load all of your classifiers
clf = {}
ftse = None

with open("app/clf.pkl", "rb") as f:
	ftse = pickle.load(f)

# If the classifier could not be loaded, then exit the program
if ftse is None:
	print("Error loading the classifier")
	exit(1)

# Make a dictionary of clfs
clf["FTSE"] = ftse

# Instantiate your flask app
app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

# The predict endpoint accepts an index, along with an input and returns a prediction on movement
@app.route("/predict", methods = ["GET", "POST"])
def predict():
	if request.method == "POST":
		# If the method is POST, then proceeed with the prediction
		res = {
			"prediction": None,
		}
		
		# Make an object, called content that will store the response 
		content = request.json
		
		# Try to find the input and index parameters
		try:
			# Get the name of the index and the input from the content object
			index = content["index"]
			X_input = np.array([content["input"]])
		
			# Pass the input into the classifier to get a prediction
			pred = clf[index].predict_proba(X_input).tolist()
			# Bind the prediction with the response object
			res["prediction"] = pred

		# Catch the exception where the client did not give nine features in the input
		except ValueError as e:
			res["message"] = "Please enter an input with nine features"
		
		# Catch the exception where the client entered an index that is not the dictionary i.e the index was not trained!
		except KeyError as e:
			res["message"] = "Please enter an index that has been trained"
	
		# No matter what happens, return a resposne the client
		finally:
			return jsonify(res)

	# If you are here, then you didn't use the POST method to make the request
	return "<h1> Use POST and supply index and input as JSON </h1>"

if __name__ == "__main__":
	app.run(debug = True, port = 5000)
