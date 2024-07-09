# State strings
INITIAL = 'INITIAL'
RETURN_POLICY_Q1 = 'RETURN_POLICY_Q1'
RETURN_POLICY_Q2 = 'RETURN_POLICY_Q2'
RETURN_POLICY_Q3 = 'RETURN_POLICY_Q3'
ORDER_STATUS_WITHOUT_ID = 'ORDER_STATUS_WITHOUT_ID'
ORDER_STATUS_INCLUDE_ID = 'ORDER_STATUS_INCLUDE_ID'
REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO = 'REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO'
REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO = 'REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO'
UNKNOWN = 'UNKNOWN'

# Response messages
INITIAL_MSG = "Hello!\n"
RETURN_POLICY_Q1_MSG = """You can return most items within 30 days of purchase for a full refund or exchange.
Items must be in their original condition, with all tags and packaging intact.
Please bring your receipt or proof of purchase when returning items.\n"""
RETURN_POLICY_Q2_MSG = """Yes, certain items such as clearance merchandise, perishable goods, and personal care items are non-returnable.
Please check the product description or ask a store associate for more details.\n"""
RETURN_POLICY_Q3_MSG = """Refunds will be issued to the original form of payment.
If you paid by credit card, the refund will be credited to your card.
If you paid by cash or check, you will receive a cash refund.\n"""
ORDER_STATUS_WITHOUT_ID_MSG = "Please provide your order ID to check the status.\n"
REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO_MSG = "Please provide your full name, email, and phone number to connect you with a human representative.\n"
UNKNOWN_MSG = "I'm sorry, I didn't understand that. Please ask a question related to the order status, return policy, or request to talk to a human representative.\n"

# Define the system prompt
system_prompt = f"""
You are a customer support assistant that classifies user intents into multiple categories. You can identify if a user is asking for the status of an order, requesting a human representative, or inquiring about return policies. Follow these rules:

1. **Initial State:** 
    - {INITIAL}: When the user just starts to talk or greet.

2. **Return Policies:** 
    - {RETURN_POLICY_Q1}: When a user asks about the return policy for items purchased at the store.
    - {RETURN_POLICY_Q2}: When a user asks if there are any items that cannot be returned under the return policy.
    - {RETURN_POLICY_Q3}: When a user asks how they will receive their refund.

3. **Order Status:** 
    - {ORDER_STATUS_WITHOUT_ID}: When a user asks for the status of an order but does not provide the order ID.
    - {ORDER_STATUS_INCLUDE_ID}_<order_id>: When a user asks for the status of an order and provides the order ID.
    
4. **Request Human Representative:** 
    - {REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO}: When a user requests to interact with a human but does not provide all contact information.
    - {REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_<full_name>_<email>_<phone_number>: When a user requests to interact with a human and provides full name, email, and phone number.
    
5. **Unknown:** 
    - {UNKNOWN}: When the user's intent does not match any of the above categories.

Recognize and classify the user's intent into one or more of the following categories:
[
'{INITIAL}',
'{RETURN_POLICY_Q1}',
'{RETURN_POLICY_Q2}',
'{RETURN_POLICY_Q3}',
'{ORDER_STATUS_WITHOUT_ID}',
'{ORDER_STATUS_INCLUDE_ID}<order_id>',
'{REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO}',
'{REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}<full_name><email><phone_number>',
'{UNKNOWN}'
].
Ensure that if multiple categories are identified, they are listed in the order specified above.
"""

# Define examples for the classifier
examples = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": INITIAL},
    
    {"role": "user", "content": "What is the status of my order?"},
    {"role": "assistant", "content": ORDER_STATUS_WITHOUT_ID},
    
    {"role": "user", "content": "My order id is 12345. Can you tell me the status?"},
    {"role": "assistant", "content": f"{ORDER_STATUS_INCLUDE_ID}_12345"},
    
    {"role": "user", "content": "I want to talk to a person."},
    {"role": "assistant", "content": REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO},
    
    {"role": "user", "content": "My name is John Doe, my email is john@example.com, and my phone number is 123-456-7890."},
    {"role": "assistant", "content": f"{REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_John-Doe_john@example.com_123-456-7890"},
    
    {"role": "user", "content": "What is the return policy for items purchased at your store?"},
    {"role": "assistant", "content": RETURN_POLICY_Q1},
    
    {"role": "user", "content": "Are there any items that cannot be returned under this policy?"},
    {"role": "assistant", "content": RETURN_POLICY_Q2},
    
    {"role": "user", "content": "How will I receive my refund?"},
    {"role": "assistant", "content": RETURN_POLICY_Q3},

    {"role": "user", "content": "Hey, How will I receive my refund?"},
    {"role": "assistant", "content": f"{INITIAL} {RETURN_POLICY_Q3}"},
    
    {"role": "user", "content": "Can you help me with something else?"},
    {"role": "assistant", "content": UNKNOWN},

    # Examples with multiple categories
    {"role": "user", "content": "Hello, I want to know the return policy and also check the status of my order. My order id is 12345."},
    {"role": "assistant", "content": f"{INITIAL} {RETURN_POLICY_Q1} {ORDER_STATUS_INCLUDE_ID}_12345"},
    
    {"role": "user", "content": "I need to talk to a person about returning an item. My name is Jane Doe, my email is jane@example.com, and my phone number is 987-654-3210."},
    {"role": "assistant", "content": f"{RETURN_POLICY_Q1} {REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_Jane-Doe_jane@example.com_987-654-3210"},
    
    {"role": "user", "content": "Hi, I have a question about your return policy and I also need the status of my order. My order ID is 54321."},
    {"role": "assistant", "content": f"{INITIAL} {RETURN_POLICY_Q1} {ORDER_STATUS_INCLUDE_ID}_54321"},
    
    {"role": "user", "content": "Can you tell me the return policy for items and also help me talk to a person? My name is John Smith, my email is john.smith@example.com, and my phone number is 555-555-5555."},
    {"role": "assistant", "content": f"{RETURN_POLICY_Q1} {REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_John-Smith_john.smith@example.com_555-555-5555"},

    {"role": "user", "content": "I need to know the status of my order ID 12345, speak with a representative, and understand the return policy. My name is Jane Doe, my email is jane.doe@example.com, and my phone number is 987-654-3210."},
    {"role": "assistant", "content": f"{RETURN_POLICY_Q1} {ORDER_STATUS_INCLUDE_ID}_12345 {REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_Jane-Doe_jane.doe@example.com_987-654-3210"},

    {"role": "user", "content": "I want to talk to a human, understand the return policy, and check the status of my order ID 67890. My name is Bob Brown, my email is bob.brown@example.com, and my phone number is 111-222-3333."},
    {"role": "assistant", "content": f"{RETURN_POLICY_Q1} {ORDER_STATUS_INCLUDE_ID}_67890 {REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_Bob-Brown_bob.brown@example.com_111-222-3333"},

    {"role": "user", "content": "Hey, can you check the status of my order ID 98765, connect me to a human representative, and inform me about the items that cannot be returned? My name is Alice Green, my email is alice.green@example.com, and my phone number is 444-555-6666."},
    {"role": "assistant", "content": f"{INITIAL} {RETURN_POLICY_Q2} {ORDER_STATUS_INCLUDE_ID}_98765 {REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO}_Alice-Green_alice.green@example.com_444-555-6666"}
]