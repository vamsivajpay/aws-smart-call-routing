# Amazon Connect Contact Flows

This directory includes two Amazon Connect contact flows, each exported as a `.json` file:

- **main-contact-flow.json**: The core flow managing all incoming contacts.
- **customer-flow.json**: A supplementary flow for handling specific customer interactions.

## Instructions

1. Sign in to your Amazon Connect instance.
2. Navigate to **Contact Flows** and select **Import Flow**.
3. Upload both `.json` files.
4. Confirm that all required resources (queues, prompts, Lambda functions) referenced in the flows are present in your instance.

## Important Notes

- These contact flows are designed to work together; import both for full functionality.
- If referenced queues or other resources do not exist, you must create them manually.
