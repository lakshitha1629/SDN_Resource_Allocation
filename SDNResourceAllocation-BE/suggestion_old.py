import tensorflow.keras as K
import pandas as pd
import mysql.connector

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
            VALUE=TIERTYPE.index(value[1])
            send_data = {}
            send_data['tierType'] = TIERTYPE[VALUE]
            send_data['NetworkBandwidth'] = NETWORKBANDWIDTH[VALUE]
            send_data['RAM'] = RAM[VALUE]
            send_data['vCPUs'] = VCPUS[VALUE]
            send_data['IP_address']  = value[2]
            send_data_arr.append(send_data)
        return send_data_arr
    except KeyError:
        print('Execution Time: convert Log To Json --> KeyError')   

def addDataToTheDataLog(tierType, IP_address):
    mydb = mysql.connector.connect(
    host="database-1.ckbdn0ey3gu5.us-east-2.rds.amazonaws.com",
    user="admin",
    password="admin123",
    database="sdnDB")
    mycursor = mydb.cursor()
    sql = "INSERT INTO data_log (tierType, IP_address) VALUES (%s, %s)"
    val = (tierType, IP_address)
    mycursor.execute(sql, val)
    mydb.commit()
    return True
    
    
