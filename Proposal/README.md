# ID2223Project
KTH Course ID2223 Project Authors: Khalid El Yaacoub, Xinyu Liang

## Proposal

In this project, we are planning to build a serverless ML system that classifies the incident category with other information in the database such as time, location, resolution.

### Dataset

The dataset we are using can be easily obtained from [San Francisco goverment Open Data Platform](https://data.sfgov.org/browse). To be specific, we are using the [Police Department Incident Reports: 2018 to Present data](https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-2018-to-Present/wg3w-h783), which includes incident reports filed as of year 2018 and is updated regularly on a daily interval.

Up to now the dataset contains around 670K data entries and 26 columns, with each row being a incident record. The columns have information on incident time, id, category, decription, resolution, location and so on.

The dataset API is free to use with an [instruction manual](https://dev.socrata.com/foundry/data.sfgov.org/wg3w-h783). A free [App Token](https://data.sfgov.org/profile/edit/developer_settings) has to be registered and a [sodapy](https://github.com/xmunoz/sodapy) package needs to be installed. All the historical data is available by setting `limit=800000` which is a value larger than the current data size.


### Methodology

We will download the newest data from the data source, make a feature pipeline and use Hopsworks as a feature store. Then we will create a feature view from it with selected features and some other preprocessing work, this feature view will be used to train a XGBoost classifier model.

As the database gets updated daily, we will be able to grab new data entries and test the performance of our model with an inference pipeline.

There will be two interfaces from Hugging-face, one to have an interactive UI interface for users to test the model, and a historical UI interface to visualize the historical performance of the model.


