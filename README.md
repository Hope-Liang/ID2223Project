# ID2223Project
KTH Course ID2223 Project Authors: Khalid El Yaacoub, Xinyu Liang

## Objectives

In this project, we built a serverless ML system that classifies the incident category based on its time and location.
The dataset we selected is [Police Department Incident Reports: 2018 to Present data](https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-2018-to-Present/wg3w-h783) from [San Francisco goverment Open Data Platform](https://data.sfgov.org/browse), which includes incident reports filed as of year 2018 and is updated regularly on a daily interval. Up to when we trained the model the dataset contains around 680K entries and 26 columns, with each row being an incident record. The columns have information on incident time, id, category, decription, resolution, location and so on, a detailed explanation can be found on the link above. 

The dataset API is free to use with an [instruction manual](https://dev.socrata.com/foundry/data.sfgov.org/wg3w-h783). A free [App Token](https://data.sfgov.org/profile/edit/developer_settings) has to be registered and a [sodapy](https://github.com/xmunoz/sodapy) package needs to be installed. All the historical data is available by setting `limit=800000` which is a value larger than the current data size.





## Methodology





## Deliverables