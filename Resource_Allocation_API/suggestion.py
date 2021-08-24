import pandas as pd
import json

def getTierOutput(USERTYPE,PROCESSORSPEED,CPU,RAM,NETWORK):
    try:
        data = {'UserType': [1, 2, 4, 3, 1], 'ProcessorSpeed': [1, 2, 2, 3, 4], 'vCPUs': [1, 2, 3, 4, 5], 'RAM': [1, 2, 3, 3, 4], 'NetworkBandwidth': [1, 2, 3, 3, 3], 'Output': [1, 2, 3, 4, 5]}
        df = pd.DataFrame.from_dict(data)
        OutputDF = (df['UserType'] == USERTYPE) & (df['ProcessorSpeed'] == PROCESSORSPEED) & (df['vCPUs'] == CPU) & (df['RAM'] == RAM) & (df['NetworkBandwidth'] == NETWORK)
        indexList = [i for i, x in enumerate(OutputDF) if x]
        
        if(len(indexList)>0):
            for a in indexList:
                #print(df['Output'][a])
                suggestion = df['Output'][a]
                Output = tierSuggestion(suggestion)
        else:
            suggestion = 0
            Output = tierSuggestion(suggestion)
            print("Out of list")
    
        return Output
    
    except KeyError:
        print('KeyError {}'.format(KeyError))


def tierSuggestion(suggestion):
    switcher = {
        1: "St1.Nano",
        2: "Mt2.GP",
        3: "Lt3.Large",
        4: "Lt4.Xlarge",
        5: "Mt5.Prem",
    }
    
    return switcher.get(suggestion, "Out of the range")