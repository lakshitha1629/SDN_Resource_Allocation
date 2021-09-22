import tensorflow.keras as K
import pandas as pd
import resource
import os

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

        i = int(predictValue)
        Number_of_processes = [10000,20000]
        Memory = [10000000,20000000]
        soft, hard = resource.getrlimit(resource.RLIMIT_NPROC)
        print ('Number of processes starts as  :', soft)
        resource.setrlimit(resource.RLIMIT_NPROC, (Number_of_processes[i], hard))
        soft, hard = resource.getrlimit(resource.RLIMIT_NPROC)
        print ('Number of processes limit changed to :', soft)

        soft1, hard1 = resource.getrlimit(resource.RLIMIT_MEMLOCK)
        print ('Memory starts as  :', soft1)
        resource.setrlimit(resource.RLIMIT_MEMLOCK, (Memory[i], hard1))
        soft1, hard1 = resource.getrlimit(resource.RLIMIT_MEMLOCK)
        print ('Memory limit changed to :', soft1)

        OutPutList=["St1.Nano","Mt2.GP","Lt3.Large","Lt4.Xlarge","Mt5.Prem"]
        return OutPutList[predictValue] 
    except:
        return "Out of the range"
    
    
    