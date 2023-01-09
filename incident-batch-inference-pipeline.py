import os
import modal
    
LOCAL=True

if LOCAL == False:
   stub = modal.Stub()
   hopsworks_image = modal.Image.debian_slim().pip_install(["hopsworks","joblib","seaborn","sklearn","dataframe-image"])
   @stub.function(image=hopsworks_image, schedule=modal.Period(days=1), secret=modal.Secret.from_name("HOPSWORKS_API_KEY"))
   def f():
       g()

def g():
    import pandas as pd
    import hopsworks
    import joblib
    import datetime
    import xgboost as xgb
    from PIL import Image
    from datetime import datetime
    import dataframe_image as dfi
    from sklearn.metrics import confusion_matrix
    from matplotlib import pyplot
    import seaborn as sns
    import requests

    project = hopsworks.login()
    fs = project.get_feature_store()
    
    mr = project.get_model_registry()
    model = mr.get_model("incident_modal", version=1)
    model_dir = model.download()
    model = joblib.load(model_dir + "/incident_model.pkl")
    
    feature_view = fs.get_feature_view(name="incident_modal", version=1)
    batch_data = feature_view.get_batch_data()
    batch_data.drop(columns=['incident_datetime'], inplace=True)
    
    y_pred = model.predict(batch_data)
    # print(y_pred)
    incident = y_pred[y_pred.size-1]
    incident_url = "https://raw.githubusercontent.com/Hope-Liang/ID2223Project/main/images/" + incident + ".png"
    print("Incident predicted: " + incident)
    img = Image.open(requests.get(incident_url, stream=True).raw)            
    img.save("./latest_incident.png")
    dataset_api = project.get_dataset_api()    
    dataset_api.upload("./latest_incident.png", "Resources/images", overwrite=True)
    
    iris_fg = fs.get_feature_group(name="incident_modal", version=1)
    df = iris_fg.read()
    # print(df["variety"])
    label = df.iloc[-1]["incident_category"]
    label_url = "https://raw.githubusercontent.com/Hope-Liang/ID2223Project/main/images/" + label + ".png"
    print("Incident actual: " + label)
    img = Image.open(requests.get(label_url, stream=True).raw)            
    img.save("./actual_incident.png")
    dataset_api.upload("./actual_incident.png", "Resources/images", overwrite=True)
    
    monitor_fg = fs.get_or_create_feature_group(name="incident_predictions",
                                                version=1,
                                                primary_key=["datetime"],
                                                description="SF Incident Category Prediction/Outcome Monitoring"
                                                )
    
    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    data = {
        'prediction': [incident],
        'label': [label],
        'datetime': [now],
       }
    monitor_df = pd.DataFrame(data)
    monitor_fg.insert(monitor_df, write_options={"wait_for_job" : False})
    
    history_df = monitor_fg.read()
    # Add our prediction to the history, as the history_df won't have it - 
    # the insertion was done asynchronously, so it will take ~1 min to land on App
    history_df = pd.concat([history_df, monitor_df])


    df_recent = history_df.tail(5)
    dfi.export(df_recent, './df_recent.png', table_conversion = 'matplotlib')
    dataset_api.upload("./df_recent.png", "Resources/images", overwrite=True)
    
    predictions = history_df[['prediction']]
    labels = history_df[['label']]

    # Only create the confusion matrix when our iris_predictions feature group has examples of all 13 different
    print("Number of different incident categories predictions to date: " + str(predictions.value_counts().count()))
    if predictions.value_counts().count() == 13:
        results = confusion_matrix(labels, predictions)
    
        df_cm = pd.DataFrame(results, ['True Assault', 'True Drug Offense', 'True Financial Offense', 'True Malicious Mischief', 'True Missing Person',
        'True Non-Criminal', 'True Other', 'True Other Offenses', 'True Suspicious', 'True Theft and Robbery', 'True Traffic and Vehicle Offense',
        'True Warrant', 'True Weapons Offense'],
                         ['Pred Assault', 'Pred Drug Offense', 'Pred Financial Offense','Pred Malicious Mischief', 'Pred Missing Person',
        'Pred Non-Criminal', 'Pred Other', 'Pred Other Offenses', 'Pred Suspicious', 'Pred Theft and Robbery', 'Pred Traffic and Vehicle Offense',
        'Pred Warrant', 'Pred Weapons Offense'])
    
        cm = sns.heatmap(df_cm, annot=True, fmt="d")
        fig = cm.get_figure()
        fig.savefig("./confusion_matrix.png")
        dataset_api.upload("./confusion_matrix.png", "Resources/images", overwrite=True)
    else:
        print("You need 13 different incident category predictions to create the confusion matrix.")
        print("Run the batch inference pipeline more times until you get 13 different incident category predictions") 


if __name__ == "__main__":
    if LOCAL == True :
        g()
    else:
        with stub.run():
            f()

