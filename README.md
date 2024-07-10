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

The chatbot demonstrates a 99% accuracy rate, validated through testing with 100 predefined dialogues stored in `backend_app/test_classification.py`.

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

