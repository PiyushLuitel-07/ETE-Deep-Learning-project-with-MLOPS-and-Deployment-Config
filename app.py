'''
Flask: The main Flask class for creating the web application.
request: To handle HTTP requests in Flask.
jsonify: To create JSON responses.
render_template: For rendering HTML templates.
os: To interact with the operating system, used here for setting environment variables and executing system commands.
CORS and cross_origin: To handle Cross-Origin Resource Sharing (CORS) headers, allowing the application to be accessed from different domains.
decodeImage and PredictionPipeline: These are custom modules from cnnClassifier package for image decoding and prediction.
'''
from flask import Flask, request, jsonify, render_template
import os
from flask_cors import CORS, cross_origin
from cnnClassifier.utils.common import decodeImage
from cnnClassifier.pipeline.predict import PredictionPipeline



'''Sets the LANG and LC_ALL environment variables to en_US.UTF-8. This is often done to ensure consistent encoding across different systems.'''
os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')



'''
app = Flask(__name__): Initializes a Flask application.
CORS(app): Allows CORS for all routes in the Flask application.
'''
app = Flask(__name__)
CORS(app)



'''
Defines a class ClientApp, which is instantiated when the server starts.
It initializes with a filename for the input image (inputImage.jpg) and creates a PredictionPipeline object for image classification.
'''
class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        self.classifier = PredictionPipeline(self.filename)



'''
Home Route ("/", HTTP GET):
Renders an HTML template named index.html. This route is likely to serve a webpage allowing users to interact with the application.
'''
@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')



'''
Train Route ("/train", HTTP GET and POST):
Executes the command python main.py to train the model when a request is received.
Returns a simple success message after training is completed.
'''
@app.route("/train", methods=['GET','POST'])
@cross_origin()
def trainRoute():
    os.system("python main.py")
    return "Training done successfully!"



@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRoute():
    image = request.json['image']
    decodeImage(image, clApp.filename)
    result = clApp.classifier.predict()
    return jsonify(result)


if __name__ == "__main__":
    clApp = ClientApp()
    # app.run(host='0.0.0.0', port=8080) #local host
    # app.run(host='0.0.0.0', port=8080) #for AWS
    app.run(host='0.0.0.0', port=80) #for AZURE



'''
explain this in detail:

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')

ChatGPT
This section of code is defining a route in a Flask web application. Let's break it down:

Decorator:
@app.route("/", methods=['GET']): This is a decorator provided by Flask. It associates the function below it (home()) with a specific URL route ("/" in this case) and HTTP methods (GET in this case). So, when a user navigates to the root URL of the web application (e.g., http://yourdomain.com/), this function will handle the incoming request.
Cross-Origin Resource Sharing (CORS):
@cross_origin(): This is another decorator provided by the flask_cors extension. It allows Cross-Origin Resource Sharing for this route. CORS is a mechanism that enables resources to be shared across different domains, and this decorator ensures that the browser permits requests from other domains to access this route.
Function:
def home():: This is the function associated with the route. It will be executed when a request is made to the specified URL with the specified HTTP method(s).
render_template('index.html'): This function is used to render an HTML template named 'index.html'. Flask looks for templates in a directory named templates in the root directory of the Flask application. So, it expects to find a file named index.html inside a templates directory. Once found, Flask renders this HTML template and sends it as the response to the client's request.
In summary, when a user makes a GET request to the root URL of the Flask web application, this route handler function home() is invoked. It renders an HTML template called index.html and sends it back to the user's browser as the response. This mechanism allows the web application to serve dynamic HTML content to users accessing the root URL.

'''


'''

GET:
Purpose: GET is used to request data from a specified resource.
Data in URL: When you send a GET request, the data is sent via the URL as key-value pairs in the query string. For example, http://example.com/api/resource?param1=value1&param2=value2.
Idempotent: GET requests are considered idempotent, meaning making the same GET request multiple times will have the same effect each time and will not change the server's state.
Caching: GET requests can be cached by browsers and intermediaries like proxy servers because they are generally safe and have no side effects.
Example: Retrieving a list of products from an e-commerce website, fetching a user's profile information.

POST:
Purpose: POST is used to submit data to be processed to a specified resource.
Data in Body: When you send a POST request, the data is sent in the body of the request. This allows for sending larger amounts of data and more complex data structures compared to GET requests.
Non-idempotent: POST requests are not idempotent, meaning making the same POST request multiple times might have different effects each time, especially if it involves modifying server state.
Not Cached: POST requests are generally not cached because they often involve changing the server's state.
Example: Submitting a form on a website, creating a new resource on a server, such as adding a new user to a database.
In the provided Flask code, you can see both GET and POST methods being used in the route definitions:

@app.route("/", methods=['GET']): This route is only accessible via the GET method. It's typically used for serving static content or retrieving data from the server.
@app.route("/train", methods=['GET','POST']): This route is accessible via both GET and POST methods. It's used for both retrieving (GET) and submitting (POST) data. In this case, it's used to trigger model training through a GET or POST request.
@app.route("/predict", methods=['POST']): This route is only accessible via the POST method. It's used for submitting data, in this case, an image for prediction.
These HTTP methods allow the web application to handle different types of requests and perform appropriate actions based on the client's needs.

'''