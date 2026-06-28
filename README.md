This is a project in progress to help understand how to create automatic data ingestion pipelines. It is hosted on my personal linux server. 

This pipeline ingests daily Texas grid demand from the EIA API and  populates a csv(will populate postgress soon). It also versions the data using DVC and then pushes the artifacts to an AWS S3 Bucket. 
On arrival, the S3 Bucket triggers an AWS Lambda function to observe the daily ingestion metadata and send success/failures health reports to my email via AWS SNS. Everything is triggered automatically every night via cron and shell scripts. 

Phase 2(In Progress) 

Train XGboost model to predict future demand. 90 percent of this will also be automated/

Phase 3(Planned)

FAST API backend and Streamlit for dashboard to display future grid demands. 


### Full Demand Time Series
![Full demand time series](eda_output/1_timeseries.png)

### Hourly Pattern
![Demand by hour of day](eda_output/2_hourly_pattern.png)

### Daily Pattern
![Demand by day of week](eda_output/3_daily_pattern.png)

### Monthly Pattern
![Demand by month](eda_output/4_monthly_pattern.png)

### Demand Distribution
![Demand value distribution](eda_output/5_distribution.png)

### Year-over-Year Comparison
![Year over year monthly averages](eda_output/6_yearly_comparison.png)


