import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import _VectorizerMixin
from sklearn.feature_selection._base import SelectorMixin
from sklearn.pipeline import Pipeline

def merge_category(x):
    if x == "Human Trafficking (A), Commercial Sex Acts":
        return "Human Trafficking"
    elif x == "Human Trafficking (B), Involuntary Servitude":
        return "Human Trafficking"
    elif x == "Human Trafficking, Commercial Sex Acts":
        return "Human Trafficking"
    elif x == "Weapons Offence":
        return "Weapons Offense"
    elif x == "Drug Violation":
        return "Drug Offense"
    elif x == "Motor Vehicle Theft?":
        return "Motor Vehicle Theft"
    elif x == "Suspicious Occ":
        return "Suspicious"
    elif x == "Rape":
        return "Sex Offense"
    else:
        return x


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
    # step 1: dropping irrelavent columns and null values
    incident_df.drop(columns=['incident_date','incident_time','incident_year','report_datetime','row_id','incident_id','incident_number', 
                         'report_type_description','filed_online','incident_code','incident_subcategory',
                         'incident_description','resolution','cad_number','intersection','cnn','analysis_neighborhood',
                         'supervisor_district','point',':@computed_region_jwn9_ihcz',':@computed_region_26cr_cadq',
                         ':@computed_region_qgnn_b9vv',':@computed_region_nqbw_i6c3',':@computed_region_h4ep_8xdi',
                         ':@computed_region_n4xg_c4py',':@computed_region_jg9y_a9du'], inplace=True)
    incident_df.dropna(inplace=True)

    # step 2: create new columns
    incident_df['incident_month']=pd.to_datetime(incident_df["incident_datetime"]).dt.month
    incident_df['incident_year']=pd.to_datetime(incident_df["incident_datetime"]).dt.year
    incident_df['incident_hour']=pd.to_datetime(incident_df["incident_datetime"]).dt.hour
    #incident_df['incident_dayofweek']=pd.to_datetime(incident_df["incident_datetime"]).dt.dayofweek

    # step 3: merging labels
    incident_df['incident_category']=incident_df['incident_category'].apply(merge_category)

    
    # step 4: onehot encoding using column Transformer Settings

    t = [('ohe-cat', OneHotEncoder(sparse=False, handle_unknown='ignore'), ['incident_day_of_week', 'report_type_code','police_district']),
         ('do_nothing', SimpleImputer(strategy='most_frequent'), ['incident_datetime', 'incident_category', 'latitude', 'longitude', 'incident_month', 'incident_year', 'incident_hour']), 
         ]
    pre_processor = ColumnTransformer(transformers=t, remainder='drop')
    incident_df_processed = pre_processor.fit_transform(X=incident_df)
    # Get column names
    columns = get_ct_feature_names(pre_processor)
    incident_df_processed = pd.DataFrame(incident_df_processed, columns=columns)

    # step 5: change column types and names

    numeric_columns = incident_df_processed.columns.drop(['incident_datetime','incident_category'])
    incident_df_processed[numeric_columns] = incident_df_processed[numeric_columns].apply(pd.to_numeric)
    incident_df_processed['incident_datetime'] = incident_df_processed['incident_datetime'].apply(pd.to_datetime)
    incident_df_processed.rename(columns={"police_district_Out of SF": "police_district_OutOfSF"},inplace=True)

    return incident_df_processed