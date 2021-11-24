from flask import Flask, request, redirect, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import suggestion_old
import mysql.connector
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

api.add_resource(Test,'/')
api.add_resource(GetSuggestion,'/api/getSuggestion')
api.add_resource(GetAllList,'/api/getAllList')
api.add_resource(CreateTier,'/api/createTier')

if __name__ == '__main__':
    app.run(debug=True)