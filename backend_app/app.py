from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os
import boto3
from dotenv import load_dotenv
from flask_cors import CORS
from utils import classify_message, handle_order_status_include_id_classification, handle_request_human_include_info_classification, create_order_handle, get_order_by_id, fetch_orders, update_order_status, delete_order_by_id
from constants import (INITIAL, ORDER_STATUS_WITHOUT_ID, ORDER_STATUS_INCLUDE_ID,
                       REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO, REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO,
                       RETURN_POLICY_Q1, RETURN_POLICY_Q2, RETURN_POLICY_Q3, UNKNOWN,
                       INITIAL_MSG, RETURN_POLICY_Q1_MSG, RETURN_POLICY_Q2_MSG, RETURN_POLICY_Q3_MSG,
                       ORDER_STATUS_WITHOUT_ID_MSG, REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO_MSG, UNKNOWN_MSG)


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Allow only local requests to access the backend
CORS(app, origins=["http://localhost:*", "http://127.0.0.1:*", "https://chatbot-frontend-kklu.onrender.com/"])

# Initialize OpenAI client
clientOpenAi = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

# Connect to DynamoDB
# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name=os.getenv("AWS_DEFAULT_REGION"))
orders_table = dynamodb.Table('Orders')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    classifications = classify_message(clientOpenAi, user_message)
    response = ""
    
    for classification in classifications:
        if classification.startswith(INITIAL):
            response += INITIAL_MSG
        if classification == RETURN_POLICY_Q1:
            response += RETURN_POLICY_Q1_MSG
        if classification == RETURN_POLICY_Q2:
            response += RETURN_POLICY_Q2_MSG
        if classification == RETURN_POLICY_Q3:
            response += RETURN_POLICY_Q3_MSG
        if classification == ORDER_STATUS_WITHOUT_ID:
            response += ORDER_STATUS_WITHOUT_ID_MSG
        if classification.startswith(ORDER_STATUS_INCLUDE_ID):
            response += handle_order_status_include_id_classification(orders_table, classification)
        if classification == REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO:
            response += REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO_MSG
        if classification.startswith(REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO):
            response += handle_request_human_include_info_classification(classification)
        if classification == UNKNOWN and response == "":
            response += UNKNOWN_MSG

    return jsonify({"response": response.strip()})

# CRUD operations for orders

@app.route('/order', methods=['POST'])
def create_order():
    order_status = request.json.get('status')
    unique_id = create_order_handle(orders_table, order_status)
    return jsonify({'id': unique_id})

@app.route('/order/<order_id>', methods=['GET'])
def get_order(order_id):
    response = get_order_by_id(orders_table, order_id)
    return jsonify(response['Item'])  # This will raise KeyError if 'Item' is not in response

@app.route('/orders', methods=['GET'])
def get_orders():
    # Get query parameters for pagination
    limit = int(request.args.get('limit', 10))
    last_key = request.args.get('lastKey')

    items, last_evaluated_key = fetch_orders(orders_table, limit, last_key)

    return jsonify({
        'items': items,
        'lastEvaluatedKey': last_evaluated_key
    })
   
@app.route('/order/<order_id>', methods=['PUT'])
def update_order(order_id):
    order_status = request.json.get('orderStatus')
    response = update_order_status(orders_table, order_id, order_status)
    return jsonify(response['Attributes']) 

@app.route('/order/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    response = delete_order_by_id(orders_table, order_id)
    return jsonify(response['Attributes']) 


if __name__ == '__main__':
    # Get the environment variable
    env = os.getenv('FLASK_ENV', 'production')
    # Set debug mode based on the environment variable
    print("FLASK_ENV = ", env)
    debug = env == 'development'
    app.run(debug=debug)
