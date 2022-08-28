import pandas as pd
from azure.data.tables import TableClient

def get_dasboard_data(table_name):

    
    table_client = TableClient.from_connection_string(conn_str="DefaultEndpointsProtocol=https;AccountName=darkdiggersstorage;AccountKey=p/1FydC6+TuLvWDx8KfUBAO8wMXQQHpU1RLKCxi/4ImQY0AByS5MJFwMCOoHRaH8Y4Pwbfrq3w4i+AStp7oiKw==;EndpointSuffix=core.windows.net", table_name=table_name)
    azure_table = table_client.query_entities("")
    df = pd.DataFrame([_ for _ in azure_table]) 
    
    df.index = df["PredictionDateTime"]
    g = df.groupby(pd.Grouper(freq="M"))
    
    df_preds = g["Prediction"].count().reset_index()
    df_preds["yyyymm"] = df_preds["PredictionDateTime"].dt.strftime('%Y%m')
    preds = list(df_preds["Prediction"])
    preds_labels = list(df_preds["yyyymm"])
    
    df_writeback = g["Writeback"].count().reset_index()
    df_writeback["yyyymm"] = df_writeback["PredictionDateTime"].dt.strftime('%Y%m')
    writeback = list(df_writeback["Writeback"])
    writeback_labels = list(df_writeback["yyyymm"])
    
    total_predictions, total_writebacks = df_preds["Prediction"].sum(), df_writeback["Writeback"].sum()

    df["yyyymm"] = df["PredictionDateTime"].dt.strftime('%Y%m')
    df["Correct_prediction"] = df["Writeback"]==df["Prediction"]
    df_accuracy = df[~df["Writeback"].isna()].groupby("yyyymm")["Correct_prediction"].agg("mean").reset_index()
    accurazy_labels, accurazy =  list(df_accuracy["yyyymm"]), list(round(df_accuracy["Correct_prediction"],2)*100)
    
    total_accurazy = round(round(df[~df["Writeback"].isna()]["Correct_prediction"].mean(),2)*100,0)
    last_call = df["PredictionDateTime"].max().strftime('%Y-%m-%d')
    last_writeback = df.loc[~df["Writeback"].isna(),"PredictionDateTime"].max().strftime('%Y-%m-%d')
    
    return preds_labels, preds, writeback_labels,\
           writeback,total_predictions, total_writebacks, \
           accurazy_labels, accurazy, last_call, last_writeback, \
           total_accurazy 