from flask import Flask, request, redirect
from flask_restful import Resource, Api
from flask_cors import CORS
import os
import re
import suggestion

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

class GetSuggestion(Resource):
    def get(self):
        return {"error":"Invalid Method."}

    def post(self):
        try:
            value = request.get_json()
            if(value):
                Output = suggestion.getTierOutput(value['UserType'],value['ProcessorSpeed'],value['vCPUs'],value['RAM'],value['NetworkBandwidth'])

                return {'Output Values': Output}, 201
            
            return {"error":"Invalid format."}
            
        except Exception as error:
            return {'error': error}

api.add_resource(Test,'/')
api.add_resource(GetSuggestion,'/getSuggestion')

if __name__ == '__main__':
    app.run(debug=True)
