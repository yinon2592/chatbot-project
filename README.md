## General Explanation

The chatbot is built on the OpenAI framework, utilizing a Large Language Model (LLM) to process customer inquiries on an e-commerce platform. It is designed to handle:
- Return policy explanations.
- Order status updates.
- Requests to connect with human representatives.

Inputs are classified into defined states to generate relevant responses.

## States

The chatbot categorizes user inputs into the following states for targeted responses:

- **`INITIAL`**: Default starting state of a conversation.
- **`RETURN_POLICY_Q1`**: For general return policy inquiries.
- **`RETURN_POLICY_Q2`**: For questions about non-returnable items.
- **`RETURN_POLICY_Q3`**: For explaining the refund process.
- **`ORDER_STATUS_WITHOUT_ID`**: For order status inquiries without an order ID.
- **`ORDER_STATUS_INCLUDE_ID`**: For order status inquiries with an order ID.
- **`REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO`**: When a user seeks human assistance without providing full contact details.
- **`REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO`**: When full contact details are provided for human assistance.
- **`UNKNOWN`**: For unclassified inputs, providing general help or requesting clarification.

## Integration with DynamoDB

The chatbot uses a CRUD API with Amazon DynamoDB to manage order data, enhancing interactions by maintaining order IDs and statuses.

## Chatbot Performance Evaluation

### Accuracy

The chatbot demonstrates a 99% accuracy rate as a stateless classifier (with no conversation context), validated through testing with 100 predefined dialogues stored in backend_app/test_classification.py.
Later on, I added context to every query and made the necessary changes to the system definition and added prompts (the last queries and responses).
As a result, the chatbot achieved an 82% accuracy rate as a stateful classifier, validated through 110 predefined dialogues.

| Query | Expected Classification | Actual Classification | Result |
|-------|-------------------------|-----------------------|--------|
| Hi, can you tell me if there are items that cannot be returned? | INITIAL, RETURN_POLICY_Q2 | RETURN_POLICY_Q2 | Failed |
| Hello, can you tell me how to get a refund? | INITIAL, RETURN_POLICY_Q3 | RETURN_POLICY_Q3 | Failed |
| Hi, can you connect me with a representative? | INITIAL, REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO | REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO | Failed |
| Hello, which items cannot be returned? | INITIAL, RETURN_POLICY_Q2 | RETURN_POLICY_Q2 | Failed |
| Hi, my order ID is 98765. What is the status? | INITIAL, ORDER_STATUS_INCLUDE_ID_98765 | ORDER_STATUS_INCLUDE_ID_98765 | Failed |
| Hello, can you tell me if there are items that cannot be returned? | INITIAL, RETURN_POLICY_Q2 | RETURN_POLICY_Q2 | Failed |
| Hi, how will I get my refund processed? | INITIAL, RETURN_POLICY_Q3 | RETURN_POLICY_Q3 | Failed |
| Hi, I need to know the status of my order ID 98765 and the return policy. | INITIAL, RETURN_POLICY_Q1, ORDER_STATUS_INCLUDE_ID_98765 | RETURN_POLICY_Q1, ORDER_STATUS_INCLUDE_ID_98765 | Failed |
| Hello, my order ID is 98765. What is the status? | INITIAL, ORDER_STATUS_INCLUDE_ID_98765 | ORDER_STATUS_INCLUDE_ID_98765 | Failed |
| Hi, what is the status of my order ID 54321? | INITIAL, ORDER_STATUS_INCLUDE_ID_54321 | ORDER_STATUS_INCLUDE_ID_54321 | Failed |
| Hey, can you tell me the return policy for items bought at your store? | INITIAL, RETURN_POLICY_Q1 | RETURN_POLICY_Q1 | Failed |
| Hi, I need to talk to a person and check order status 54321. | INITIAL, ORDER_STATUS_INCLUDE_ID_54321, REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO | REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO, ORDER_STATUS_INCLUDE_ID_54321 | Failed |
| Hi, can you tell me which items cannot be returned and status of order 54321? | INITIAL, RETURN_POLICY_Q2, ORDER_STATUS_INCLUDE_ID_54321 | RETURN_POLICY_Q2, ORDER_STATUS_INCLUDE_ID_54321 | Failed |
| Hi, I want to know how refunds are processed, my order status ID 12345, and I need to speak to a human... | INITIAL, RETURN_POLICY_Q3, ORDER_STATUS_INCLUDE_ID_12345, REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO | RETURN_POLICY_Q3, ORDER_STATUS_INCLUDE_ID_12345, REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO | Failed |
| Hello, I need the return policy, the status of my order ID 54321, and to speak with a human... | INITIAL, RETURN_POLICY_Q1, ORDER_STATUS_INCLUDE_ID_54321, REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO | RETURN_POLICY_Q1, ORDER_STATUS_INCLUDE_ID_54321, REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO | Failed |
| Please tell me the return policy, status of order ID 56789, and items that cannot be returned. | RETURN_POLICY_Q1, RETURN_POLICY_Q2, ORDER_STATUS_INCLUDE_ID_56789 | RETURN_POLICY_Q1, ORDER_STATUS_INCLUDE_ID_56789, RETURN_POLICY_Q2 | Failed |
| Hi, I want to know the status of my order ID 67890, speak to a human, and how refunds are processed... | INITIAL, RETURN_POLICY_Q3, ORDER_STATUS_INCLUDE_ID_67890, REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO | ORDER_STATUS_INCLUDE_ID_67890, REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO, RETURN_POLICY_Q3 | Failed |
| Hi, I need to know the status of my order ID 90123, how will I receive my refund, and also speak with a representative... | INITIAL, RETURN_POLICY_Q3, ORDER_STATUS_INCLUDE_ID_90123, REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO | ORDER_STATUS_INCLUDE_ID_90123, RETURN_POLICY_Q3, REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO | Failed |
| Hello, can you tell me the return policy, status of my order ID 01234, and items that cannot be returned? | INITIAL, RETURN_POLICY_Q1, RETURN_POLICY_Q2, ORDER_STATUS_INCLUDE_ID_01234 | INITIAL, RETURN_POLICY_Q1, ORDER_STATUS_INCLUDE_ID_01234, RETURN_POLICY_Q2 | Failed |
| Hi, what is the status of my order ID 57913, the return policy, and connect me with a human representative? | INITIAL, RETURN_POLICY_Q1, ORDER_STATUS_INCLUDE_ID_57913, REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO | RETURN_POLICY_Q1, ORDER_STATUS_INCLUDE_ID_57913, REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO | Failed |


### Response Relevance

Caching is implemented to enhance performance. The use of WebSockets could further improve real-time interactions.

### User Satisfaction

The design focuses on user convenience and ease of use.

## Setup Instructions

- **Backend**: Run `pip install -r requirements.txt`.
- **Frontend**: Execute `npm install` followed by `npm run build`.

## Application URLs

- **Backend URL**: [https://chatbot-project-1jej.onrender.com/](https://chatbot-project-1jej.onrender.com/)
- **Frontend URL**: [https://chatbot-frontend-kklu.onrender.com/](https://chatbot-frontend-kklu.onrender.com/)

