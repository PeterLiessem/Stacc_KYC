import pandas as pd
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# Filter data on name
def filter_name(data, name):
    return data.loc[data["name"] == name]

# Filter data on country
def filter_countries(data, country):
    return data.loc[data["countries"] == country]

# Filter data on id
def filter_id(data,id):
    return data.loc[data["id"] == id]

# Format data for respons
def format_data(data):
    data_out = {}
    for i in range(len(data['name'])):

        # Seperate aliases
        ali = ""
        if type(data['aliases'][i]) != float:
            aliases = data['aliases'][i].split(";")
            ali = {k: v for k,v in enumerate(aliases)}

        # Make instance
        data_out[i] = {
        "id": data['id'][i], 
        "schema": data['schema'][i], 
        "name": data['name'][i], 
        "aliases": ali, 
        "birth_date": data['birth_date'][i], 
        "countries": data['countries'][i], 
        "addresses": data['addresses'][i], 
        "identifiers": data['identifiers'][i], 
        "sanctions": data['sanctions'][i], 
        "phones": data['phones'][i], 
        "emails": data['emails'][i], 
        "dataset": data['dataset'][i], 
        "last_seen": data['last_seen'][i], 
        "first_seen": data['first_seen'][i]
        }
    return data_out

# Returns if there is an error
def check_errors(data, args):
    if  args["name"]==None and args["countries"]==None and args["id"]==None:
        return True, {'error': 'No identifiers provided'}, 403 # Bad request
    elif len(data) == 0:
        return True, {'error': 'No matching instances found in database'}, 404 # Not found
    return False, data, 200


class getPep_name(Resource):
    def get(self):
        parser = reqparse.RequestParser() 
        
        # Args
        parser.add_argument('name') 
        parser.add_argument('countries') 
        parser.add_argument('id') 
        args = parser.parse_args()

        # Read data
        data = pd.read_csv('pep.csv')
        
        # Filter data
        data = data if args["name"]      == None  else filter_name(data, args.name)
        data = data if args["countries"] == None  else filter_countries(data, args.countries)
        data = data if args["id"]        == None  else filter_id(data, args.id)

        # Checks for errors
        is_error, data, code = check_errors(data, args)
        if is_error:
            return data, code

        # Clean dict keys
        data = format_data(data.reset_index(drop=True))

        return {'data': data,}, 200  # data, OK
        



# entry point
api.add_resource(getPep_name, '/api/pep')  

if __name__ == '__main__':
    app.run() 