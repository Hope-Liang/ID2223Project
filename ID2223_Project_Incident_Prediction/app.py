import gradio as gr
import numpy as np
from PIL import Image
import requests

import hopsworks
import joblib

project = hopsworks.login()
fs = project.get_feature_store()

mr = project.get_model_registry()
model = mr.get_model("incident_modal", version=1)
model_dir = model.download()
model = joblib.load(model_dir + "/incident_model.pkl")


def incident(dayofweek, reportcode, district, latitude, longitude, month, year, hour):
    input_list = []
    if dayofweek == 'Friday':
        input_list.append(1.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
    elif dayofweek == 'Monday':
        input_list.append(0.0)
        input_list.append(1.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
    elif dayofweek == 'Saturday':
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(1.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
    elif dayofweek == 'Sunday':
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(1.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
    elif dayofweek == 'Thursday':
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(1.0)
        input_list.append(0.0)
        input_list.append(0.0)
    elif dayofweek == 'Tuesday':
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(1.0)
        input_list.append(0.0)
    elif dayofweek == 'Wednesday':
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(1.0)
    else:
        print("ERROR!")
        exit()
    
    if reportcode == "II":
        input_list.append(1.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
    elif reportcode == "IS":
        input_list.append(0.0)
        input_list.append(1.0)
        input_list.append(0.0)
        input_list.append(0.0)
    elif reportcode == "VI":
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(1.0)
        input_list.append(0.0)
    elif reportcode == "VS":
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(1.0)      
    else:
        print("ERROR!")
        exit()

    if district == 'Bayview':
        input_list.append(1.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
    elif district == 'Central':
        input_list.append(0.0)
        input_list.append(1.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
    elif district == 'Ingleside':
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(1.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
    elif district == 'Mission':
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(1.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
    elif district == 'Northern':
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(1.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0) 
    elif district == 'OutofSF':
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(1.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0) 
    elif district == 'Park':
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(1.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
    elif district == 'Richmond':
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(1.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
    elif district == 'Southern':
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(1.0)
        input_list.append(0.0)
        input_list.append(0.0) 
    elif district == 'Traval':
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(1.0)
        input_list.append(0.0) 
    elif district == 'Tenderloin':
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(0.0)
        input_list.append(1.0) 
    else:
        print("ERROR!")
        exit()  

    input_list.append(latitude)
    input_list.append(longitude)
    input_list.append(month)
    input_list.append(year)
    input_list.append(hour)

    incident = model.predict(np.asarray(input_list).reshape(1, -1))
    incident_url = "https://raw.githubusercontent.com/Hope-Liang/ID2223Project/main/images/" + incident[0] + ".png"
    img = Image.open(requests.get(incident_url, stream=True).raw)
    
    return img

demo = gr.Interface(
    fn=incident,
    title="Incident Predictive Analytics",
    description="Experiment with incident features/attributes to predict what kind of incident category took place.",
    allow_flagging="never",
    inputs=[
        gr.inputs.Textbox(default="Saturday", label="Incident Day of Week (Saturday, Sunday etc...)"),
        gr.inputs.Textbox(default="II", label="Report Type Code (II, IS, VI, VS)"),
        gr.inputs.Textbox(default="Northern", label="Police District (Northern, Bayview, Southern, Mission, Ingleside, Tenderloin, Taraval, Central, Richmond, Park, OutofSF)"),
        gr.inputs.Number(default=37.711111, label="latitude"),
        gr.inputs.Number(default=-122.422222, label="longitude"),
        gr.inputs.Number(default=1, label="Incident Month (1-12)"),
        gr.inputs.Number(default=2023, label="Incident Year (e.g 2019)"),
        gr.inputs.Number(default=1, label="Incident Hour (0-23)"),
    ],
    outputs=gr.Image(type="pil"))

demo.launch()