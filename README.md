# ID2223Project
KTH Course ID2223 Project Authors: Khalid El Yaacoub, Xinyu Liang

## Proposal

We plan to 

### Dataset

The dataset we are using can be easily obtained from [San Francisco goverment Open Data Platform](https://data.sfgov.org/browse). To be specific, we are using the [Police Department Incident Reports: 2018 to Present data](https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-2018-to-Present/wg3w-h783), which includes incident reports filed as of year 2018 and is updated regularly on a daily interval.

Up to now the dataset contains around 670K data entries and 26 columns, with each row being a incident record.

The dataset API is free to use with an [instruction manual](https://dev.socrata.com/foundry/data.sfgov.org/wg3w-h783). A free [App Token](https://data.sfgov.org/profile/edit/developer_settings) has to be registered and a [sodapy](https://github.com/xmunoz/sodapy) package needs to be installed. All the historical data is available by setting `limit=800000` which is a value larger than the current data size.


### Methodology