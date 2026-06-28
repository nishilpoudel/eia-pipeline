This is a project in progress to help me learn about how to create automatic data ingestion pipelines. 

This pipeline automatically ingests daily Texas grid demand from the EIA API and  populates a csv via cron (will populate postgress soon). It also versions the data using DVC and then pushes the artifacts to an AWS S3 Bucket. 
On arrival, the S3 Bucket triggers an AWS Lambda function to observe the daily ingestion metadata and send success/failures to my email via AWS SNS. 
