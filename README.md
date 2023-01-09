# ID2223Project
KTH Course ID2223 Project Authors: Khalid El Yaacoub, Xinyu Liang

## Objectives

In this project, we built a serverless ML system that classifies the incident category based on its time and location.
The dataset we selected is [Police Department Incident Reports: 2018 to Present data](https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-2018-to-Present/wg3w-h783) from [San Francisco goverment Open Data Platform](https://data.sfgov.org/browse), which includes incident reports filed as of year 2018 and is updated regularly on a daily interval. Up to when we trained the model the dataset contains around 680K entries and 26 columns, with each row being an incident record. The columns have information on incident time, id, category, decription, resolution, location and so on, a detailed explanation can be found on the link above. 

The dataset API is free to use with an [instruction manual](https://dev.socrata.com/foundry/data.sfgov.org/wg3w-h783). A free [App Token](https://data.sfgov.org/profile/edit/developer_settings) has to be registered and a [sodapy](https://github.com/xmunoz/sodapy) package needs to be installed. All the historical data is available by setting `limit=800000` which is a value larger than the current data size.

## Methodology

We downloaded the newest data from the data source on Jan 8th, 2023. It contained data up to 2023-01-05.

### Data Preprocessing

We preprocessed the raw data in [preprocessor_pipeline.py](https://github.com/Hope-Liang/ID2223Project/blob/main/preprocessor_pipeline.py), which starts at dropping irrelavent columns and rows containing null values. We did this because we found that only around 1-2 percent of the rows have missing values, and the information in many columns doesn't have any predictive power.

Then we extracted the year, month and hour information from the incident_datetime column, and we merged the 49 categories into 13 categories based on our understanding of the data. Lastly we one-hot encoded the incident_day_of_week, report_type_code and police_district.

The features we used to predict the incident categories are: incident year (eg. 2018), month (1-12), hour (0-23), day of week (e.g. Monday), report type code, police district, longitude, latitude, and the column to be predicted is incident category (having 13 categories).

### Feature Pipeline

We wrote the feature pipeline in [incident-feature-pipeline.py](https://github.com/Hope-Liang/ID2223Project/blob/main/incident-feature-pipeline.py), which first downloads the data from the data source, then preprocess it with the preprocessor, and lastly uploads it to [Hopsworks](https://www.hopsworks.ai) feature store. The feature store has more than 500K data entries.

### Training Pipeline

We the trained a XGBoost model with [incident-training-pipeline.py](https://github.com/Hope-Liang/ID2223Project/blob/main/incident-training-pipeline.py), which reads the data from the feature store and creates a feature view. The train-test-split-ratio is set to be 80%-20%, and 


### Inference Pipeline



## Deliverables

### Predictions on Latest Data Monitor UI



### Interactive UI


