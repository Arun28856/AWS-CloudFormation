import json
import boto3
import os

ses = boto3.client('ses')

def lambda_handler(event, context):
    # Print incoming event for debugging
    print("Received event: " + json.dumps(event, indent=2))

    # Extract SNS message
    for record in event['Records']:
        sns_message = record['Sns']['Message']
        sns_subject = record['Sns'].get('Subject', 'SNS Notification')

        # Send email using SES
        try:
            response = ses.send_email(
                Source=os.environ['SOURCE_EMAIL'],  # Verified email in SES
                Destination={
                    'ToAddresses': [os.environ['DESTINATION_EMAIL']]  # Recipient
                },
                Message={
                    'Subject': {
                        'Data': sns_subject,
                        'Charset': 'UTF-8'
                    },
                    'Body': {
                        'Text': {
                            'Data': sns_message,
                            'Charset': 'UTF-8'
                        }
                    }
                }
            )
            print("Email sent! Message ID:"),
            print(response['MessageId'])
        except Exception as e:
            print("Error sending email:", e)

    return {
        'statusCode': 200,
        'body': json.dumps('Processed SNS message and sent via SES.')
    }
