from constants import system_prompt, examples
import uuid
import re
import csv
from constants import (
    INITIAL, 
    RETURN_POLICY_Q1, 
    RETURN_POLICY_Q2, 
    RETURN_POLICY_Q3, 
    ORDER_STATUS_WITHOUT_ID, 
    ORDER_STATUS_INCLUDE_ID, 
    REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO, 
    REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO, 
    UNKNOWN
)

def classify_message(clientOpenAi, user_message):
    completion_response = clientOpenAi.chat.completions.create(
                            temperature=0,
                            max_tokens=64,
                            top_p=1,
                            frequency_penalty=0,
                            presence_penalty=0,
                            model="gpt-4o",
                            messages=[
                                {
                                    "role": "system", 
                                    "content": system_prompt
                                },
                                 *examples,
                                {
                                    "role": "user", 
                                    "content": user_message
                                }
                            ],
                            )
    states_array = completion_response.choices[0].message.content.strip().split(' ')
    return states_array

def handle_order_status_include_id_classification(orders_table, classification):
    order_status_include_id_pattern = re.compile(rf"{ORDER_STATUS_INCLUDE_ID}_(.*)")
    pattern_order_id_match = order_status_include_id_pattern.match(classification)
    if pattern_order_id_match:
        order_id = pattern_order_id_match.group(1)
        # Make a query to the database to get the order status
        item_response = get_order_by_id(orders_table, order_id)
        if 'Item' in item_response:
            order = item_response['Item']
            return f"Thank you for providing your order ID {order_id}. The status of your order is: {order['orderStatus']}.\n"
        else:
            return f"Thank you for providing your order ID {order_id}. Unfortunately, we could not find any order with that ID.\n"
    else:
        return "Error parsing ID. Please try again.\n"

def handle_request_human_include_info_classification(classification):
    request_human_include_info_pattern = re.compile(rf"{REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_(.*?)_(.*?)_(.*)")
    pattern_contact_info_match = request_human_include_info_pattern.match(classification)
    if pattern_contact_info_match:
        name, email, phone = pattern_contact_info_match.groups()
        name = name.replace('-', ' ')
        # Save the contact information to csv file
        with open('contact_info.csv', mode='a', newline='') as contact_info_file:
            contact_info_writer = csv.writer(contact_info_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            contact_info_writer.writerow([name, email, phone])
        return f"Thank you for providing your contact information: Name - {name}, Email - {email}, Phone - {phone}. A human representative will contact you shortly.\n"
    else:
        return "Error parsing contact information. Please try again.\n"

def create_order(orders_table, order_status):
    unique_id = str(uuid.uuid4())
    orders_table.put_item(
            Item={
                'id': unique_id,
                'orderStatus': order_status
            }
        )
    return unique_id

def get_order_by_id(orders_table, order_id):
    response = orders_table.get_item(
        Key={
            'id': order_id
        }
    )
    return response

def fetch_orders(orders_table, limit, last_key=None):
    scan_kwargs = {
        'Limit': limit
    }

    if last_key:
        scan_kwargs['ExclusiveStartKey'] = {'id': last_key}

    response = orders_table.scan(**scan_kwargs)
    items = response.get('Items', [])
    last_evaluated_key = response.get('LastEvaluatedKey')

    return items, last_evaluated_key

def update_order_status(orders_table, order_id, order_status):
    response = orders_table.update_item(
        Key={
            'id': order_id
        },
        UpdateExpression='SET orderStatus = :val1',
        ExpressionAttributeValues={
            ':val1': order_status
        },
        ConditionExpression='attribute_exists(id)',
        ReturnValues="ALL_NEW"
    )
    return response

def delete_order_by_id(orders_table, order_id):
    response = orders_table.delete_item(
        Key={
            'id': order_id
        },
        ReturnValues='ALL_OLD'
    )
    return response