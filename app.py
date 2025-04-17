from flask import Flask, request, jsonify, abort, send_file, render_template
from methods import openFile, checkJSONHeaders
import os


app = Flask(__name__)

basedir = os.path.dirname(__file__)
file_path = os.path.join(basedir, 'truckinglist.json')

# Root route with helpful description
@app.route('/')
def index():
    return send_file('static/html/index.html')

# GET all trucking companies
@app.route('/companies', methods=['GET'])
def get_all_companies():
    # Load JSON file from disk
    # Extract and return all companies as JSON
    json = openFile(file_path, 'r')
    checkJSONHeaders(json)
    return json

# GET a specific company by name
@app.route('/companies/<string:name>', methods=['GET'])
def get_company(name):
    # Load JSON and return data for the company if it exists
    # If not found, return 404 error

    json = openFile(file_path, 'r')
    checkJSONHeaders(json)

    companies = json['Mainline']['Table']['Row']

    for company in companies:
        if company['Company'] == name or \
           os.path.splitext(company['Logo'])[0] == name:

           # overwrites copy, not actual JSON file
            json['Mainline']['Table']['Row'] = [company]
            
            return json

    abort(404)

# POST a new trucking company
@app.route('/companies', methods=['POST'])
def add_company():
    # Read JSON from request body
    # Validate required fields
    # Add the new company to the JSON data
    # Save the updated data back to the file
    pass

@app.route('/add-company')
def add():
    return render_template("add.html")

# PUT to update an existing company
@app.route('/companies/<string:name>', methods=['PUT'])
def update_company(name):
    # Read update data from request
    # Find and update the specified company
    # Save the updated data back to the file
    pass

# DELETE a trucking company
@app.route('/companies/<string:name>', methods=['DELETE'])
def delete_company(name):
    # Locate and delete the specified company
    # Save the updated data back to the file
    pass

# Error handlers (optional to implement in their section)
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500



