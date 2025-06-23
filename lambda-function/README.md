# Lambda Function: State-Based Call Routing for Amazon Connect

This repository contains an AWS Lambda function designed for integration with Amazon Connect. The function dynamically routes incoming customer calls to specific customer service teams based on the caller’s phone number state.

## Features

- Extracts the caller’s phone number from the Amazon Connect event.
- Uses the [Numverify API](https://numverify.com/) to validate the number and determine its state/location.
- Maps the detected state to a specific customer service (CS) team.
- Returns the mapped CS team and location to Amazon Connect for call routing.

## Usage

1. **Set up your Numverify API key** as an environment variable:
   ```
   NUMVERIFY_API_KEY=your_api_key
   ```
2. **Deploy the `lambda_state_routing.py` function** to AWS Lambda.
3. **Configure your Amazon Connect contact flow** to invoke this Lambda function using the "Invoke Lambda Function" block.

## Example Event

```json
{
  "Details": {
    "ContactData": {
      "Attributes": {
        "number": "+919876543210"
      }
    }
  }
}
```

## Response Structure

- **Success (valid number):**
  ```json
  {
    "statusCode": 200,
    "body": "{\"cs_team\": \"TG\", \"location\": \"Telangana\"}"
  }
  ```
- **Failure (missing or invalid number):**
  ```json
  {
    "statusCode": 400,
    "body": "\"Missing customer phone number.\""
  }
  ```

## Customization

- Add or update state-to-team mappings in the `STATE_TEAM_MAP` dictionary in the Python file.

## License

MIT
