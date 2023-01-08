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
    # Convert to pandas DataFrame
    incident_df = pd.DataFrame.from_records(results)
    incident_df.drop(columns=['incident_date','report_datetime','row_id','incident_id','incident_number', 
                         'report_type_description','filed_online','incident_code','incident_subcategory',
                         'incident_description','resolution','cad_number','intersection','cnn','analysis_neighborhood',
                         'supervisor_district','point',':@computed_region_jwn9_ihcz',':@computed_region_26cr_cadq',
                         ':@computed_region_qgnn_b9vv',':@computed_region_nqbw_i6c3',':@computed_region_h4ep_8xdi',
                         ':@computed_region_n4xg_c4py',':@computed_region_jg9y_a9du'], inplace=True)
    incident_df.dropna(inplace=True)

    incident_fg = fs.get_or_create_feature_group(
        name="incident_modal",
        version=1,
        primary_key=['incident_datetime','incident_time','incident_year','incident_day_of_week','report_type_code','incident_category','police_district','latitude','longitude'], 
        description="Incident dataset")
    incident_fg.insert(incident_df, write_options={"wait_for_job" : False})

if __name__ == "__main__":
    if LOCAL == True :
        g()
    else:
        with stub.run():
            f()
