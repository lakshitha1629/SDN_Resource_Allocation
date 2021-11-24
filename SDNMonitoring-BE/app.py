from flask import Flask, request, redirect, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import monitor
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

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

class GetMonitorDetails(Resource):
    def get(self):
        dataList = monitor.main()
        return jsonify(dataList)


api.add_resource(Test,'/')
api.add_resource(GetMonitorDetails,'/api/getMonitorDetails')

if __name__ == '__main__':
    app.run(debug=True)