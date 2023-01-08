import os
import modal
    
LOCAL=True

if LOCAL == False:
   stub = modal.Stub()
   image = modal.Image.debian_slim().pip_install(["hopsworks","joblib","seaborn","sklearn","dataframe-image","sodapy"]) 

   @stub.function(image=image, schedule=modal.Period(days=1), secret=modal.Secret.from_name("HOPSWORKS_API_KEY"))
   def f():
       g()

def g():
    import hopsworks
    import pandas as pd
    from sodapy import Socrata

    project = hopsworks.login()
    fs = project.get_feature_store()

    client = Socrata("data.sfgov.org", "gZmg4iarmENBTk1Vzsb94bnse", username="xinyulia@kth.se", password="Xw990504")
    results = client.get("wg3w-h783", limit=800000)
    incident_df = pd.DataFrame.from_records(results) # Convert to pandas DataFrame
    
    from preprocessor_pipeline import preprocessing_incident
    incident_df_preprocessed = preprocessing_incident(incident_df)

    incident_fg = fs.get_or_create_feature_group(
        name="incident_modal",
        version=1,
        primary_key=['incident_day_of_week_Friday', 'incident_day_of_week_Monday',
       'incident_day_of_week_Saturday', 'incident_day_of_week_Sunday',
       'incident_day_of_week_Thursday', 'incident_day_of_week_Tuesday',
       'incident_day_of_week_Wednesday', 'report_type_code_II',
       'report_type_code_IS', 'report_type_code_VI', 'report_type_code_VS',
       'police_district_Bayview', 'police_district_Central',
       'police_district_Ingleside', 'police_district_Mission',
       'police_district_Northern', 'police_district_OutOfSF',
       'police_district_Park', 'police_district_Richmond',
       'police_district_Southern', 'police_district_Taraval',
       'police_district_Tenderloin', 'incident_datetime',
       'latitude', 'longitude', 'incident_month', 'incident_year',
       'incident_hour'], 
        description="Incident dataset")
    incident_fg.insert(incident_df_preprocessed, write_options={"wait_for_job" : False})

if __name__ == "__main__":
    if LOCAL == True :
        g()
    else:
        with stub.run():
            f()
