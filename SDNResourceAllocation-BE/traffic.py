import random
import requests
from server import Server
import suggestion_old

def sendData(dataList):
    try:
        data = suggestion_old.convertLogToJson(dataList)
        #instantiating some servers
        s1 = Server(data[0]['vCPUs'],data[0]['RAM'],data[0]['IP_address']) #the total is 50
        s2 = Server(data[1]['vCPUs'],data[1]['RAM'],data[1]['IP_address']) #the total is 30
        s3 = Server(data[2]['vCPUs'],data[2]['RAM'],data[2]['IP_address']) #the total is 20

        total = (s1.RAM + s1.cpuCores) + (s2.RAM + s2.cpuCores) + (s3.RAM + s3.cpuCores)

        #calculating server selection probability for each server
        s1_prob = int(((s1.RAM + s1.cpuCores) / (total))*10)
        s2_prob = int(((s2.RAM + s2.cpuCores) / (total))*10)
        s3_prob = int(((s3.RAM + s3.cpuCores) / (total))*10)

        #server selection process
        for i in range(1,10):
            pos = {'server 1': s1_prob, 'server 2': s2_prob, 'server 3': s3_prob}
            choice = random.choice([x for x in pos for y in range(pos[x])]) #making the random choice

            if(choice == "server 1"):
                r =requests.get(s1.ip)
                return s1.ip
            elif(choice == "server 2"):
                r =requests.get(s2.ip)
                return s2.ip
            else:
                r =requests.get(s3.ip)
                return s3.ip
        
    except KeyError:
        return False
    