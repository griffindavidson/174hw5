from flask import Flask, request, jsonify, abort, send_file, render_template, request # type: ignore
from methods import openFile, checkJSONHeaders, convertBase64ToImage
import os
import json
import base64

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
        if company['Company'] == name:

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

    # TODO: thoroughly validate fields, and
    #   allow fields to be empty

    # Read JSON from Request body
    data = request.get_json()
    row = ""
    fileBase64 = ""

    # Determine if an image is sent or not, or just the raw row data
    if 'row' not in data: 
        row = data
    else:
        row = data['row']
        # Reads, Validates, and saves logo file
        if 'file' in data and data['file']: # runs if file is uploaded
            fileBase64 = data['file']
            convertBase64ToImage(fileBase64, row['Logo'])

    # Read and validate existing data
    jsonData = openFile(file_path, 'r')
    checkJSONHeaders(jsonData)

    # Requires at least company name given
    if not row['Company']:
        abort(400, description="Company Name required")

    # Prevents duplicate entries
    for company in jsonData['Mainline']['Table']['Row']:
        if company['Company'] == row['Company']:
            abort(400, description="Company already exists")

    # append new row to json
    jsonData['Mainline']['Table']['Row'].append(row)

    # save new JSON to file
    try:
        with open(file_path, 'w') as file:
            json.dump(jsonData, file, indent=4)
    except Exception as e:
        abort(500)

    # return successful response
    return jsonify({"success": "Data Successfully added"})

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
    return jsonify({'error': error.description if hasattr(error, 'description') else 'Bad request'}), 400

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500



