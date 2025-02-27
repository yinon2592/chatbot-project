import boto3
from utils import handle_create_order, delete_order_by_id, classify_message
from constants import (INITIAL, ORDER_STATUS_WITHOUT_ID, ORDER_STATUS_INCLUDE_ID,
                       REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO, REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO,
                       RETURN_POLICY_Q1, RETURN_POLICY_Q2, RETURN_POLICY_Q3, UNKNOWN,
                       INITIAL_MSG, ORDER_STATUS_WITHOUT_ID_MSG, REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO_MSG,
                          RETURN_POLICY_Q1_MSG, RETURN_POLICY_Q2_MSG, RETURN_POLICY_Q3_MSG, UNKNOWN_MSG)
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
clientOpenAi = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name=os.getenv("AWS_DEFAULT_REGION"))
orders_table = dynamodb.Table('Orders')

# Create test orders
test_order_ids = []
test_order_ids.append(handle_create_order(orders_table, "Pending"))
test_order_ids.append(handle_create_order(orders_table, "Delivered"))
test_order_ids.append(handle_create_order(orders_table, "Cancelled"))

# Define test queries with expected classifications
test_queries = [
    {"query": "current user message: Hello", 
     "expected_classification": [INITIAL]},

    {"query": "current user message: Hi there", 
     "expected_classification": [INITIAL]},

    {"query": "current user message: Hey", 
     "expected_classification": [INITIAL]},

    {"query": "current user message: What is the return policy?", 
     "expected_classification": [RETURN_POLICY_Q1]},

    {"query": "current user message: Tell me the return policy for items bought at your store.", 
     "expected_classification": [RETURN_POLICY_Q1]},

    {"query": "current user message: Can I return an item?", 
     "expected_classification": [RETURN_POLICY_Q1]},

    {"query": "current user message: What items can't be returned?", 
     "expected_classification": [RETURN_POLICY_Q2]},

    {"query": "current user message: Are there items that cannot be returned?", 
     "expected_classification": [RETURN_POLICY_Q2]},

    {"query": "current user message: Which items are non-returnable?", 
     "expected_classification": [RETURN_POLICY_Q2]},

    {"query": "current user message: How will I get my refund?", 
     "expected_classification": [RETURN_POLICY_Q3]},

    {"query": "current user message: How is the refund processed?", 
     "expected_classification": [RETURN_POLICY_Q3]},

    {"query": "current user message: What method is used for refunds?", 
     "expected_classification": [RETURN_POLICY_Q3]},

    {"query": "current user message: What is the status of my order?", 
     "expected_classification": [ORDER_STATUS_WITHOUT_ID]},

    {"query": "current user message: Can you tell me the status of my order?", 
     "expected_classification": [ORDER_STATUS_WITHOUT_ID]},

    {"query": "current user message: I need to know my order status", 
     "expected_classification": [ORDER_STATUS_WITHOUT_ID]},

    {"query": f"current user message: My order ID is {test_order_ids[0]}. What's the status?", 
     "expected_classification": [f"{ORDER_STATUS_INCLUDE_ID}_{test_order_ids[0]}"]},

    {"query": f"current user message: Order ID {test_order_ids[1]} status?", 
     "expected_classification": [f"{ORDER_STATUS_INCLUDE_ID}_{test_order_ids[1]}"]},

    {"query": f"current user message: Check status for order ID {test_order_ids[2]}", 
     "expected_classification": [f"{ORDER_STATUS_INCLUDE_ID}_{test_order_ids[2]}"]},

    {"query": "current user message: I need to speak to a human.", 
     "expected_classification": [REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO]},

    {"query": "current user message: Connect me with a representative.", 
     "expected_classification": [REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO]},

    {"query": "How do I talk to a human?", 
     "expected_classification": [REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO]},

    {"query": "current user message: I am Jane Doe, jane@example.com, 987-654-3210. I need help.", 
     "expected_classification": [f"{REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_Jane-Doe_jane@example.com_987-654-3210"]},

    {"query": "current user message: My name is John Smith, my email is john.smith@example.com, and my phone number is 555-555-5555.", 
     "expected_classification": [f"{REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_John-Smith_john.smith@example.com_555-555-5555"]},

    {"query": "current user message: John Doe, john@example.com, 123-456-7890. Need to talk.", 
     "expected_classification": [f"{REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_John-Doe_john@example.com_123-456-7890"]},

    {"query": f"current user message: What is the return policy and my order ID is {test_order_ids[0]}?", 
     "expected_classification": [RETURN_POLICY_Q1, f"{ORDER_STATUS_INCLUDE_ID}_{test_order_ids[0]}"]},

    {"query": f"current user message: I need help with return policy and check order status {test_order_ids[1]}.", 
     "expected_classification": [RETURN_POLICY_Q1, f"{ORDER_STATUS_INCLUDE_ID}_{test_order_ids[1]}"]},

    {"query": f"current user message: What items can't be returned and order status {test_order_ids[2]}?", 
     "expected_classification": [RETURN_POLICY_Q2, f"{ORDER_STATUS_INCLUDE_ID}_{test_order_ids[2]}"]},

    {"query": "current user message: Hello, what is the return policy for items bought at your store?", 
     "expected_classification": [INITIAL, RETURN_POLICY_Q1]},

    {"query": "current user message: Hi, can you tell me if there are items that cannot be returned?", 
     "expected_classification": [INITIAL, RETURN_POLICY_Q2]},

    {"query": "current user message: Hey, how will I get my refund?", 
     "expected_classification": [INITIAL, RETURN_POLICY_Q3]},

    {"query": f"current user message: Check status for order ID {test_order_ids[0]} and what is the return policy?", 
     "expected_classification": [RETURN_POLICY_Q1, f"{ORDER_STATUS_INCLUDE_ID}_{test_order_ids[0]}"]},

    {"query": "current user message: I need the return policy and my order ID is 54321.", 
     "expected_classification": [RETURN_POLICY_Q1, f"{ORDER_STATUS_INCLUDE_ID}_54321"]},

    {"query": "current user message: How do I talk to a human and order status 98765?", 
     "expected_classification": [f"{ORDER_STATUS_INCLUDE_ID}_98765", REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO]}, # This test case failed (got opposite order of expected_classification)

    {"query": "current user message: My order ID is invalid_order_id. What's the status?", 
     "expected_classification": [f"{ORDER_STATUS_INCLUDE_ID}_invalid_order_id"]},

    {"query": "current user message: I need to cancel my order ID 12345", 
     "expected_classification": [UNKNOWN]},

    {"query": "current user message: Return policy for electronic items", 
     "expected_classification": [RETURN_POLICY_Q1]},

    {"query": "current user message: Can you assist me with returns and also provide status for order ID 54321?", 
     "expected_classification": [RETURN_POLICY_Q1, f"{ORDER_STATUS_INCLUDE_ID}_54321"]},

    {"query": "current user message: Hello, can you tell me how to get a refund?", 
     "expected_classification": [INITIAL, RETURN_POLICY_Q3]},

    {"query": "current user message: I need a human representative and my order status is 12345.", 
     "expected_classification": [f"{ORDER_STATUS_INCLUDE_ID}_12345", REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO]},

    {"query": "current user message: Can I talk to a person and know the return policy?", 
     "expected_classification": [RETURN_POLICY_Q1, REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO]},

    {"query": "current user message: What is the status of my order with ID 98765?", 
     "expected_classification": [f"{ORDER_STATUS_INCLUDE_ID}_98765"]},

    {"query": "current user message: Hi, can you connect me with a representative?", 
     "expected_classification": [INITIAL, REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO]},

    {"query": "current user message: Hey, I need to know the status of my order 54321.", 
     "expected_classification": [INITIAL, f"{ORDER_STATUS_INCLUDE_ID}_54321"]},

    {"query": "current user message: Hi, what is your return policy for items bought?", 
     "expected_classification": [INITIAL, RETURN_POLICY_Q1]},

    {"query": "current user message: Hello, which items cannot be returned?", 
     "expected_classification": [INITIAL, RETURN_POLICY_Q2]},

    {"query": "current user message: Hey, how will I get my refund processed?", 
     "expected_classification": [INITIAL, RETURN_POLICY_Q3]},

    {"query": "current user message: I need to talk to a person and check order status 54321.", 
     "expected_classification": [f"{ORDER_STATUS_INCLUDE_ID}_54321", REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO]},

    {"query": "current user message: Can you tell me the return policy and the status of order ID 12345?", 
     "expected_classification": [RETURN_POLICY_Q1, f"{ORDER_STATUS_INCLUDE_ID}_12345"]},

    {"query": "current user message: What are the non-returnable items and order ID status 98765?", 
     "expected_classification": [RETURN_POLICY_Q2, f"{ORDER_STATUS_INCLUDE_ID}_98765"]},

    {"query": "current user message: How do I get my refund and order status 54321?", 
     "expected_classification": [RETURN_POLICY_Q3, f"{ORDER_STATUS_INCLUDE_ID}_54321"]},

    {"query": "current user message: Hi, my order ID is 98765. What is the status?", 
     "expected_classification": [INITIAL, f"{ORDER_STATUS_INCLUDE_ID}_98765"]},

    {"query": "current user message: Hey, what is your return policy and status of order 54321?", 
     "expected_classification": [INITIAL, RETURN_POLICY_Q1, f"{ORDER_STATUS_INCLUDE_ID}_54321"]},

    {"query": "current user message: I need the status of order ID 98765 and the return policy.", 
     "expected_classification": [RETURN_POLICY_Q1, f"{ORDER_STATUS_INCLUDE_ID}_98765"]},

    {"query": "current user message: What are the items that cannot be returned and order status of 12345?", 
     "expected_classification": [RETURN_POLICY_Q2, f"{ORDER_STATUS_INCLUDE_ID}_12345"]},

    {"query": "current user message: How will I get my refund and order status of 54321?", 
     "expected_classification": [RETURN_POLICY_Q3, f"{ORDER_STATUS_INCLUDE_ID}_54321"]},

    {"query": "current user message: Can you tell me the status of my order with ID 98765?", 
     "expected_classification": [f"{ORDER_STATUS_INCLUDE_ID}_98765"]},

    {"query": "current user message: Hello, can you tell me if there are items that cannot be returned?", 
     "expected_classification": [INITIAL, RETURN_POLICY_Q2]},

    {"query": "current user message: Hi, how will I get my refund processed?", 
     "expected_classification": [INITIAL, RETURN_POLICY_Q3]},

    {"query": "current user message: Hey, I need to talk to a person and order status 12345.", 
     "expected_classification": [INITIAL, f"{ORDER_STATUS_INCLUDE_ID}_12345", REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO]},

    {"query": "current user message: Can you tell me the return policy and status of my order with ID 54321?", 
     "expected_classification": [RETURN_POLICY_Q1, f"{ORDER_STATUS_INCLUDE_ID}_54321"]},

    {"query": "current user message: What items cannot be returned and order status 98765?", 
     "expected_classification": [RETURN_POLICY_Q2, f"{ORDER_STATUS_INCLUDE_ID}_98765"]},

    {"query": "current user message: How do I get my refund processed and order status 54321?", 
     "expected_classification": [RETURN_POLICY_Q3, f"{ORDER_STATUS_INCLUDE_ID}_54321"]},

    {"query": "current user message: Hi, I need to know the status of my order ID 98765 and the return policy.", 
     "expected_classification": [INITIAL, RETURN_POLICY_Q1, f"{ORDER_STATUS_INCLUDE_ID}_98765"]},

    {"query": "current user message: Hey, what are the items that cannot be returned and order status 12345?", 
     "expected_classification": [INITIAL, RETURN_POLICY_Q2, f"{ORDER_STATUS_INCLUDE_ID}_12345"]},

    {"query": "current user message: Can you tell me how I will get my refund and order status of 54321?", 
     "expected_classification": [RETURN_POLICY_Q3, f"{ORDER_STATUS_INCLUDE_ID}_54321"]},

    {"query": "current user message: Hello, my order ID is 98765. What is the status?", 
     "expected_classification": [INITIAL, f"{ORDER_STATUS_INCLUDE_ID}_98765"]},

    {"query": "current user message: Hi, what is the status of my order ID 54321?", 
     "expected_classification": [INITIAL, f"{ORDER_STATUS_INCLUDE_ID}_54321"]},

    {"query": "current user message: Hey, can you tell me the return policy for items bought at your store?", 
     "expected_classification": [INITIAL, RETURN_POLICY_Q1]},

    {"query": "current user message: Can you tell me which items cannot be returned and order status 12345?", 
     "expected_classification": [RETURN_POLICY_Q2, f"{ORDER_STATUS_INCLUDE_ID}_12345"]},

    {"query": "current user message: How will I receive my refund and order status 98765?", 
     "expected_classification": [RETURN_POLICY_Q3, f"{ORDER_STATUS_INCLUDE_ID}_98765"]},

    {"query": "current user message: Hi, I need to talk to a person and check order status 54321.", 
     "expected_classification": [INITIAL, f"{ORDER_STATUS_INCLUDE_ID}_54321", REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO]},

    {"query": "current user message: Hey, what is your return policy and status of order 12345?", 
     "expected_classification": [INITIAL, RETURN_POLICY_Q1, f"{ORDER_STATUS_INCLUDE_ID}_12345"]},

    {"query": "current user message: Can you assist me with returns and order status 98765?", 
     "expected_classification": [RETURN_POLICY_Q1, f"{ORDER_STATUS_INCLUDE_ID}_98765"]},

    {"query": "current user message: Hi, can you tell me which items cannot be returned and status of order 54321?", 
     "expected_classification": [INITIAL, RETURN_POLICY_Q2, f"{ORDER_STATUS_INCLUDE_ID}_54321"]},

    {"query": "current user message: Hey, how will I get my refund processed and order status 12345?", 
     "expected_classification": [INITIAL, RETURN_POLICY_Q3, f"{ORDER_STATUS_INCLUDE_ID}_12345"]},

    {"query": "current user message: What is the return policy and status of order ID 98765?", 
     "expected_classification": [RETURN_POLICY_Q1, f"{ORDER_STATUS_INCLUDE_ID}_98765"]},

    {"query": "current user message: Can you tell me the items that cannot be returned and status of order 54321?", 
     "expected_classification": [RETURN_POLICY_Q2, f"{ORDER_STATUS_INCLUDE_ID}_54321"]},

    {"query": "current user message: How will I receive my refund and status of order ID 12345?", 
     "expected_classification": [RETURN_POLICY_Q3, f"{ORDER_STATUS_INCLUDE_ID}_12345"]},

    {"query": "current user message: I need to know the return policy, my order ID status 98765, and also talk to a human. My name is Carol Smith, my email is carol.smith@example.com, and my phone number is 333-444-5555.",
     "expected_classification": [RETURN_POLICY_Q1, f"{ORDER_STATUS_INCLUDE_ID}_98765", f"{REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_Carol-Smith_carol.smith@example.com_333-444-5555"]},

    {"query": "current user message: Check the status of order ID 54321, inform me about items that can't be returned, and let me speak with a representative. My name is Dave Brown, my email is dave.brown@example.com, and my phone number is 222-333-4444.",
     "expected_classification": [RETURN_POLICY_Q2, f"{ORDER_STATUS_INCLUDE_ID}_54321", f"{REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_Dave-Brown_dave.brown@example.com_222-333-4444"]},

    {"query": "current user message: Hi, I want to know how refunds are processed, my order status ID 12345, and I need to speak to a human. My name is Emily White, my email is emily.white@example.com, and my phone number is 555-666-7777.",
     "expected_classification": [INITIAL, RETURN_POLICY_Q3, f"{ORDER_STATUS_INCLUDE_ID}_12345", f"{REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_Emily-White_emily.white@example.com_555-666-7777"]},

    {"query": "current user message: Can you tell me the items that cannot be returned, the return policy, and the status of my order ID 67890?",
     "expected_classification": [RETURN_POLICY_Q1, RETURN_POLICY_Q2, f"{ORDER_STATUS_INCLUDE_ID}_67890"]},

    {"query": "current user message: What is the return policy, status of my order ID 98765, and I want to talk to a person? My name is Frank Green, my email is frank.green@example.com, and my phone number is 888-999-0000.",
     "expected_classification": [RETURN_POLICY_Q1, f"{ORDER_STATUS_INCLUDE_ID}_98765", f"{REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_Frank-Green_frank.green@example.com_888-999-0000"]},

    {"query": "current user message: Hello, I need the return policy, the status of my order ID 54321, and to speak with a human. My name is Grace Black, my email is grace.black@example.com, and my phone number is 777-888-9999.",
     "expected_classification": [INITIAL, RETURN_POLICY_Q1, f"{ORDER_STATUS_INCLUDE_ID}_54321", f"{REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_Grace-Black_grace.black@example.com_777-888-9999"]},

    {"query": "current user message: What items are non-returnable, how will I receive my refund, and the status of my order ID 23456?",
     "expected_classification": [RETURN_POLICY_Q2, RETURN_POLICY_Q3, f"{ORDER_STATUS_INCLUDE_ID}_23456"]},

    {"query": "current user message: I want to know the return policy, the items that cannot be returned, and the status of my order ID 34567.",
     "expected_classification": [RETURN_POLICY_Q1, RETURN_POLICY_Q2, f"{ORDER_STATUS_INCLUDE_ID}_34567"]},

    {"query": "current user message: How are refunds processed, what is the return policy, and the status of my order ID 45678?",
     "expected_classification": [RETURN_POLICY_Q1, RETURN_POLICY_Q3, f"{ORDER_STATUS_INCLUDE_ID}_45678"]},

    {"query": "current user message: Please tell me the return policy, status of order ID 56789, and items that cannot be returned.",
     "expected_classification": [RETURN_POLICY_Q1, RETURN_POLICY_Q2, f"{ORDER_STATUS_INCLUDE_ID}_56789"]},

    {"query": "current user message: What is the return policy, items that cannot be returned, and I need to talk to a person. My name is Helen Brown, my email is helen.brown@example.com, and my phone number is 123-456-7890.",
     "expected_classification": [RETURN_POLICY_Q1, RETURN_POLICY_Q2, f"{REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_Helen-Brown_helen.brown@example.com_123-456-7890"]},

    {"query": "current user message: Hi, I want to know the status of my order ID 67890, speak to a human, and how refunds are processed. My name is Ian Blue, my email is ian.blue@example.com, and my phone number is 234-567-8901.",
     "expected_classification": [INITIAL, RETURN_POLICY_Q3, f"{ORDER_STATUS_INCLUDE_ID}_67890", f"{REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_Ian-Blue_ian.blue@example.com_234-567-8901"]},

    {"query": "current user message: Can you tell me the status of my order ID 78901, the return policy, and connect me with a representative. My name is Jack White, my email is jack.white@example.com, and my phone number is 345-678-9012.",
     "expected_classification": [RETURN_POLICY_Q1, f"{ORDER_STATUS_INCLUDE_ID}_78901", f"{REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_Jack-White_jack.white@example.com_345-678-9012"]},

    {"query": "current user message: Check the status of order ID 89012, inform me about the return policy, and let me speak with a representative. My name is Kate Green, my email is kate.green@example.com, and my phone number is 456-789-0123.",
     "expected_classification": [RETURN_POLICY_Q1, f"{ORDER_STATUS_INCLUDE_ID}_89012", f"{REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_Kate-Green_kate.green@example.com_456-789-0123"]},

    {"query": "current user message: Hi, I need to know the status of my order ID 90123, how will I receive my refund, and also speak with a representative. My name is Laura Brown, my email is laura.brown@example.com, and my phone number is 567-890-1234.",
     "expected_classification": [INITIAL, RETURN_POLICY_Q3, f"{ORDER_STATUS_INCLUDE_ID}_90123", f"{REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_Laura-Brown_laura.brown@example.com_567-890-1234"]},

    {"query": "current user message: Hello, can you tell me the return policy, status of my order ID 01234, and items that cannot be returned?",
     "expected_classification": [INITIAL, RETURN_POLICY_Q1, RETURN_POLICY_Q2, f"{ORDER_STATUS_INCLUDE_ID}_01234"]},

    {"query": "current user message: I need to know the return policy, the status of my order ID 13579, and also speak with a representative. My name is Mike Black, my email is mike.black@example.com, and my phone number is 678-901-2345.",
     "expected_classification": [RETURN_POLICY_Q1, f"{ORDER_STATUS_INCLUDE_ID}_13579", f"{REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_Mike-Black_mike.black@example.com_678-901-2345"]},

    {"query": "current user message: Please inform me about items that can't be returned, the return policy, and the status of my order ID 24680.",
     "expected_classification": [RETURN_POLICY_Q1, RETURN_POLICY_Q2, f"{ORDER_STATUS_INCLUDE_ID}_24680"]},

    {"query": "current user message: I want to know the return policy, the status of my order ID 35791, and speak to a human. My name is Nancy White, my email is nancy.white@example.com, and my phone number is 789-012-3456.",
     "expected_classification": [RETURN_POLICY_Q1, f"{ORDER_STATUS_INCLUDE_ID}_35791", f"{REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_Nancy-White_nancy.white@example.com_789-012-3456"]},

    {"query": "current user message: Can you check the status of my order ID 46802, tell me the return policy, and inform me about items that can't be returned?",
     "expected_classification": [RETURN_POLICY_Q1, RETURN_POLICY_Q2, f"{ORDER_STATUS_INCLUDE_ID}_46802"]},

    {"query": "current user message: Hi, what is the status of my order ID 57913, the return policy, and connect me with a human representative? My name is Oliver Brown, my email is oliver.brown@example.com, and my phone number is 890-123-4567.",
     "expected_classification": [INITIAL, RETURN_POLICY_Q1, f"{ORDER_STATUS_INCLUDE_ID}_57913", f"{REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_Oliver-Brown_oliver.brown@example.com_890-123-4567"]},

    {"query": "current user message: I need the return policy, the items that cannot be returned, and the status of my order ID 69024.",
     "expected_classification": [RETURN_POLICY_Q1, RETURN_POLICY_Q2, f"{ORDER_STATUS_INCLUDE_ID}_69024"]},

    {"query": "current user message: Please tell me the status of my order ID 70135, the return policy, and how refunds are processed.",
     "expected_classification": [RETURN_POLICY_Q1, RETURN_POLICY_Q3, f"{ORDER_STATUS_INCLUDE_ID}_70135"]}
]

contexted_conversations = [
    # helo msseage twice
    {"query": f""""
        user: hello
        assistant: {INITIAL_MSG}
        current user message: hello
        """,
        "expected_classification": [INITIAL]},

    {"query": f""""
        user: hey
        assistant: {INITIAL_MSG}
        current user message: what is the return policy?
        """,
        "expected_classification": [RETURN_POLICY_Q1]},

    {"query": f""""
        user: hey
        assistant: {INITIAL_MSG}
        current user message: what items can't be returned?
        """,
        "expected_classification": [RETURN_POLICY_Q2]},

    {"query": f""""
        user: hi
        assistant: {INITIAL_MSG}
        current user message: how will I get my refund?
        """,
        "expected_classification": [RETURN_POLICY_Q3]},

    {"query": f""""
        user: hello
        assistant: {INITIAL_MSG}
        current user message: can you tell me the status of my order?
        """,
        "expected_classification": [ORDER_STATUS_WITHOUT_ID]},
    
    {"query": f""""
        user: hello
        assistant: {INITIAL_MSG}
        user: what is the status of my order?
        assistant: please provide your order ID
        current user message: {test_order_ids[0]}
        """,
        "expected_classification": [f"{ORDER_STATUS_INCLUDE_ID}_{test_order_ids[0]}"]},
    
    {"query": f""""
        user: hey
        assistant: {INITIAL_MSG}
        current user message: I need to speak to a human.
        """,
        "expected_classification": [REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO]},

    {"query": f""""
        user: hello
        assistant: {INITIAL_MSG}
        current user message: I am Jane Doe, my email is jane_doe@example.com and my phone number is 123-456-7890. I need help.
        """,
        "expected_classification": [f"{REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_Jane-Doe_jane_doe@example.com_123-456-7890"]},
    
    {"query": f""""
        user: hello
        assistant: {INITIAL_MSG}
        current user message: I need to cancel my order ID 12345
        """,
        "expected_classification": [UNKNOWN]},
    
    {"query": f""""
        user: hello
        assistant: {INITIAL_MSG}
        current user message: I want to know the return policy and also check the status of my order. My order id is {test_order_ids[0]}.
        """,
        "expected_classification": [RETURN_POLICY_Q1, f"{ORDER_STATUS_INCLUDE_ID}_{test_order_ids[0]}"]},
]

test_queries.extend(contexted_conversations)

# Function to test classification accuracy
def test_classification_accuracy():
    correct_count = 0

    for test in test_queries:
        user_message = test["query"]
        expected_classification = test["expected_classification"]
        
        # Get the actual classification from the classify_message function
        actual_classification = classify_message(clientOpenAi, user_message)
        
        if actual_classification == expected_classification:
            correct_count += 1
        else:
            print(f"Test failed for query: '{user_message}'")
            print(f"Expected: {expected_classification}, but got: {actual_classification}")

    accuracy = (correct_count / len(test_queries)) * 100
    print(f"Classification Accuracy: {accuracy}%")

    # Cleanup: Delete test orders
    for order_id in test_order_ids:
        delete_order_by_id(orders_table, order_id)

# Run the test
test_classification_accuracy()

# this test got 99% accuracy (1 out of total 100 test cases failed)