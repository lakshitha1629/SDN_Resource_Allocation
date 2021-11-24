from flask import Flask, request, redirect, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import suggestion_old
import traffic
import mysql.connector
import base64
import json
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)
mydb = mysql.connector.connect(
    host="database-1.ckbdn0ey3gu5.us-east-2.rds.amazonaws.com",
    user="admin",
    password="admin123",
    database="sdnDB"
)

class Test(Resource):
    def get(self):
        return 'Welcome to, SDN API!'
    
    def post(self):
        try:
            value = request.get_json()
            if(value):
                return {'Post Values': value}, 201
            
            return {"error":"Invalid format."}
            
        except Exception as error:
            return {'error': error}

class GetSuggestion(Resource):
    def get(self):
        return {"error":"Invalid Method."}
    
    def post(self):
        try:
            data = request.get_json()
            # print(data)
            Output = suggestion_old.tierSuggestion(data)
            return {'OutputValue': Output}, 201

        except Exception as error:
            return {'error': error}

class GetAllList(Resource):
    def get(self):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM data_log")
        myresult = mycursor.fetchall()
        dataList = suggestion_old.convertLogToJson(myresult)
        return jsonify(dataList)

class CreateTier(Resource):
    def get(self):
        return {"error":"Invalid Method."}
    
    def post(self):
        try:
            tierType = request.get_json()
            print(tierType)
            IP_address = "192.168.20.10"
            # print(data)
            Output = suggestion_old.addDataToTheDataLog(mydb, int(tierType), IP_address)
            return {Output}, 201

        except Exception as error:
            return {'error': error}

class GetTraffic(Resource):
    def get(self):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM data_log")
        myresult = mycursor.fetchall()
        data = traffic.sendData(myresult)
        return {'IP_Address': data}, 201

class GetFutureTraffic(Resource):
    def get(self):
        return {"error":"Invalid Method."}
    
    def post(self):
        try:
            futureTraffic = request.get_json()
            with open("./file/"+str(futureTraffic['year'])+".png", "rb") as img_file:
                my_string = base64.b64encode(img_file.read())
                return {'Img': "data:image/png;base64,"+str(my_string.decode('utf-8'))}, 201

        except Exception as error:
            return {'error': error}

class GetPredictTraffic(Resource):
    def get(self):
        f = open('data.json')
        data = json.load(f)
        return jsonify(data)


api.add_resource(Test,'/')
api.add_resource(GetSuggestion,'/api/getSuggestion')
api.add_resource(GetAllList,'/api/getAllList')
api.add_resource(CreateTier,'/api/createTier')
api.add_resource(GetTraffic,'/api/getTraffic')
api.add_resource(GetFutureTraffic,'/api/getFutureTraffic')
api.add_resource(GetPredictTraffic,'/api/getPredictTraffic')

if __name__ == '__main__':
    app.run(debug=True)