| Query | Expected Classification | Actual Classification | Result |
|-------|-------------------------|-----------------------|--------|
| Hi, can you tell me if there are items that cannot be returned? | INITIAL, RETURN_POLICY_Q2 | RETURN_POLICY_Q2 | Failed |
| Hi, can you connect me with a representative? | INITIAL, REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO | REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO | Failed |
| Hello, which items cannot be returned? | INITIAL, RETURN_POLICY_Q2 | RETURN_POLICY_Q2 | Failed |
| Hi, my order ID is 98765. What is the status? | INITIAL, ORDER_STATUS_INCLUDE_ID_98765 | ORDER_STATUS_INCLUDE_ID_98765 | Failed |
| Hi, how will I get my refund processed? | INITIAL, RETURN_POLICY_Q3 | RETURN_POLICY_Q3 | Failed |
| Hi, what is the status of my order ID 54321? | INITIAL, ORDER_STATUS_INCLUDE_ID_54321 | ORDER_STATUS_INCLUDE_ID_54321 | Failed |
| Hi, I need to talk to a person and check order status 54321. | INITIAL, ORDER_STATUS_INCLUDE_ID_54321, REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO | ORDER_STATUS_INCLUDE_ID_54321, REQUEST_HUMAN_WITHOUT_ALL_CONTACT_INFO | Failed |
| Hi, can you tell me which items cannot be returned and status of order 54321? | INITIAL, RETURN_POLICY_Q2, ORDER_STATUS_INCLUDE_ID_54321 | RETURN_POLICY_Q2, ORDER_STATUS_INCLUDE_ID_54321 | Failed |
| Hi, I want to know how refunds are processed, my order status ID 12345, and I need to speak to a human... | INITIAL, RETURN_POLICY_Q3, ORDER_STATUS_INCLUDE_ID_12345, REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO | RETURN_POLICY_Q3, ORDER_STATUS_INCLUDE_ID_12345, REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO | Failed |
| Hi, I want to know the status of my order ID 67890, speak to a human, and how refunds are processed... | INITIAL, RETURN_POLICY_Q3, ORDER_STATUS_INCLUDE_ID_67890, REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO | ORDER_STATUS_INCLUDE_ID_67890, RETURN_POLICY_Q3, REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO | Failed |
| Hi, I need to know the status of my order ID 90123, how will I receive my refund, and also speak with a representative... | INITIAL, RETURN_POLICY_Q3, ORDER_STATUS_INCLUDE_ID_90123, REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO | ORDER_STATUS_INCLUDE_ID_90123, RETURN_POLICY_Q3, REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO | Failed |
| Hello, can you tell me the return policy, status of my order ID 01234, and items that cannot be returned? | INITIAL, RETURN_POLICY_Q1, RETURN_POLICY_Q2, ORDER_STATUS_INCLUDE_ID_01234 | INITIAL, RETURN_POLICY_Q1, ORDER_STATUS_INCLUDE_ID_01234, RETURN_POLICY_Q2 | Failed |
| Hi, what is the status of my order ID 57913, the return policy, and connect me with a human representative? | INITIAL, RETURN_POLICY_Q1, ORDER_STATUS_INCLUDE_ID_57913, REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO | RETURN_POLICY_Q1, ORDER_STATUS_INCLUDE_ID_57913, REQUEST_HUMAN_INCLUDE_ALL_CONTACT_INFO | Failed |
