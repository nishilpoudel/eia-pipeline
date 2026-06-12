import boto3
import os
import json
import logging


#Initalize the s3 client 
s3_client = boto3.client('s3')
sns_client = boto3.client('sns')


#Initalize the logger
logger = logging.getLogger()
logger.setLevel("INFO")


def publish_to_sns(topic_arn, message):
    response = sns_client.publish(
        TopicArn = topic_arn,
        Message = message,
        Subject = "Report from S3"
    )


def lambda_handler(event, context):
    topic_arn = os.environ.get("SNS_TOPIC_ARN")
    
    try:
        bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        object_key = event["Records"][0]["s3"]["object"]["key"]
        response = s3_client.get_object(Bucket = bucket_name, Key = object_key)

        data = json.loads(response["Body"].read())

        ingest_date = data['ingest_date']
        rows_added = data['rows_added']
        first_new_timestamp = data['first_new_timestamp']
        last_new_timestamp = data['last_new_timestamp']

        if rows_added > 0:
            body = f"The report for {ingest_date} was a success. Number of rows aded is {rows_added} from the range of {first_new_timestamp} to {last_new_timestamp}."
            publish_to_sns(topic_arn, body)
        else:
            logger.error(f"There were no rows updated")
            body = "No rows were updated. Further troubleshooting is required."
            publish_to_sns(topic_arn, body)


    except Exception as e:
        body = "Error. Further troubleshooting is required."
        publish_to_sns(topic_arn, body)
        logger.error(f"Error uploading meta data {str(e)}")
        raise




