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
    
def convertLogToJson(result):
    try:
        send_data_arr = []
        resultList = list(result)
        TIERTYPE = ["St1.Nano","Mt2.GP","Lt3.Large","Lt4.Xlarge","Mt5.Prem"]
        RAM = [0.5,1.0,2.0,4.0,8.0]
        VCPUS = [2,2,2,2,2]
        NETWORKBANDWIDTH = [5,5,5,5,5]
        for value in resultList:
            send_data = {}
            send_data['tierType'] = TIERTYPE[value[1]]
            send_data['NetworkBandwidth'] = NETWORKBANDWIDTH[value[1]]
            send_data['RAM'] = RAM[value[1]]
            send_data['vCPUs'] = VCPUS[value[1]]
            send_data['IP_address']  = value[2]
            send_data_arr.append(send_data)
        return send_data_arr
    except KeyError:
        print('Execution Time: convert Log To Json --> KeyError')   

def addDataToTheDataLog(mydb, tierType, IP_address):
    sql = "INSERT INTO data_log (tierType, IP_address) VALUES (%s, %s)"
    val = (tierType, str(IP_address))
    mycursor.execute(sql, val)
    mydb.commit()
    return True
    
    
