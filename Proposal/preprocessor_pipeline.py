import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import _VectorizerMixin
from sklearn.feature_selection._base import SelectorMixin
from sklearn.pipeline import Pipeline


def get_feature_out(estimator, feature_in):
    if hasattr(estimator, 'get_feature_names'):
        if isinstance(estimator, _VectorizerMixin):
            # handling all vectorizers
            return [f'vec_{f}' \
                    for f in estimator.get_feature_names()]
        else:
            return estimator.get_feature_names(feature_in)
    elif isinstance(estimator, SelectorMixin):
        return np.array(feature_in)[estimator.get_support()]
    else:
        return feature_in


def get_ct_feature_names(ct):
    # handles all estimators, pipelines inside ColumnTransfomer
    # doesn't work when remainder =='passthrough'
    # which requires the input column names.
    output_features = []

    for name, estimator, features in ct.transformers_:
        if name != 'remainder':
            if isinstance(estimator, Pipeline):
                current_features = features
                for step in estimator:
                    current_features = get_feature_out(step, current_features)
                features_out = current_features
            else:
                features_out = get_feature_out(estimator, features)
            output_features.extend(features_out)
        elif estimator == 'passthrough':
            output_features.extend(ct._feature_names_in[features])

    return output_features

def preprocessing_incident(incident_df):

    # change data type of all columns from string
    # extract hour, month, year from datetime and remove datetime
    incident_df['incident_month']=pd.to_datetime(incident_df["incident_datetime"]).dt.month
    incident_df['incident_year']=pd.to_datetime(incident_df["incident_datetime"]).dt.year
    incident_df['incident_hour']=pd.to_datetime(incident_df["incident_datetime"]).dt.hour
    #incident_df['incident_dayofweek']=pd.to_datetime(incident_df["incident_datetime"]).dt.dayofweek
    incident_df=incident_df.astype({'latitude': 'float64', 'longitude': 'float64'})
    incident_df.drop(columns=['incident_datetime'], inplace=True)
    
    # column Transformer Settings

    t = [('ohe-cat', OneHotEncoder(sparse=False, handle_unknown='ignore'), ['incident_day_of_week', 'report_type_code','police_district']),
         ('do_nothing', SimpleImputer(strategy='most_frequent'), ['incident_category', 'latitude', 'longitude', 'incident_month', 'incident_year', 'incident_hour']), 
         ]
    pre_processor = ColumnTransformer(transformers=t, remainder='drop')
    incident_df_processed = pre_processor.fit_transform(X=incident_df)

    # Get column names
    columns = get_ct_feature_names(pre_processor)
    incident_df_processed = pd.DataFrame(incident_df_processed, columns=columns)

    return incident_df_processed