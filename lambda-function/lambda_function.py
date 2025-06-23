import json
import requests
import os

"""
Lambda Function for State-Based Call Routing in Amazon Connect

Purpose:
- Extracts the caller's phone number from the Amazon Connect event.
- Validates and determines location using the Numverify API.
- Maps the detected state to a customer service team for call routing.
"""

NUMVERIFY_API_KEY = os.getenv('NUMVERIFY_API_KEY')

# State to CS team mapping
STATE_TEAM_MAP = {
    'Telangana': 'TG',
    'Andhra Pradesh': 'AP',
    'Tamil Nadu': 'TN',
    'Maharashtra': 'MH'
}

DEFAULT_CS_TEAM = 'Default'

def lambda_handler(event, context):
    # Extract customer's phone number
    phone_number = event.get('Details', {}).get('ContactData', {}).get('Attributes', {}).get('number')
    if not phone_number:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing customer phone number.")
        }

    # Validate phone number format (basic check, can be improved)
    if not phone_number.startswith("+91") or len(phone_number) < 10:
        return {
            'statusCode': 400,
            'body': json.dumps("Invalid phone number format.")
        }

    # Call numverify API
    url = (
        f"http://apilayer.net/api/validate"
        f"?access_key={NUMVERIFY_API_KEY}"
        f"&number={phone_number[3:]}"  # Remove +91 country code
        f"&country_code=IN"
        f"&format=1"
    )
    try:
        response = requests.get(url)
        data = response.json()

        if not data.get('valid'):
            return {
                'statusCode': 400,
                'body': json.dumps("Invalid phone number.")
            }

        region = data.get('location', '').strip()

        # Assign to default CS team if region is not in the predefined list
        cs_team = STATE_TEAM_MAP.get(region, DEFAULT_CS_TEAM)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'cs_team': cs_team,
                'location': region
            })
        }

    except requests.exceptions.RequestException as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Request error: {str(e)}")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
