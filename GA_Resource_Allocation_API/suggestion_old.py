import tensorflow.keras as K
import pandas as pd

def tierSuggestion(config):
    try:
        json_file = open('model.json', 'r')
        model_json = json_file.read()
        json_file.close()
        model = K.models.model_from_json(model_json)
        model.load_weights("model.h5")

        if type(config) == dict:
            df = pd.DataFrame(config)
        else:
            df = config

        predictValuePre = model.predict(df)
        predictValue = round(predictValuePre[0][0])-1
        OutPutList=["St1.Nano","Mt2.GP","Lt3.Large","Lt4.Xlarge","Mt5.Prem"]
        return OutPutList[predictValue] 
    except:
        return "Out of the range"
    
    
    