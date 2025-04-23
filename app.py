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

    abort(404, description="Company not found")

# POST a new trucking company
@app.route('/companies', methods=['POST'])
def add_company():
    # Read JSON from request body
    # Validate required fields
    # Add the new company to the JSON data
    # Save the updated data back to the file

    # Read JSON from Request body
    data = request.get_json()
    row = ""

    # Determine if an image is sent or not, or just the raw row data
    if 'row' not in data: 
        row = data
    else:
        row = data['row']
        if 'file' in data and data['file']: # runs if file is uploaded
            # Reads, Validates, and saves logo file
            convertBase64ToImage(data['file'], row['Logo'])

    # Read and validate existing data
    jsonData = openFile(file_path, 'r')
    checkJSONHeaders(jsonData)

    # Requires all fields given
    if not row['Company']:
        abort(400, description="Company Name required")

    if not row['HomePage']:
        abort(400, description="Company HomePage required")

    if not row['Hub']['Hubs']:
        abort(400, description="Company Hub required")

    if not row['Logo']:
        abort(400, description="Company logo required")

    if not row['Revenue']:
        abort(400, description="Company Revenue required")

    if not row['Services']:
        abort(400, description="Company Services required")

    # Prevents duplicate entries keyed on company name
    for company in jsonData['Mainline']['Table']['Row']:
        if company['Company'] == row['Company']:
            abort(400, description="Company already exists")

    # append new row to json
    jsonData['Mainline']['Table']['Row'].append(row)

    # save new JSON to file
    try:
        with open(file_path, 'w') as file:
            json.dump(jsonData, file, indent=4)
    except Exception:
        abort(500, description="JSON file missing")

    # return successful response
    return jsonify({"success": "Data Successfully added"})

# Front-end for POST /companies
@app.route('/add-company')
def add():
    return render_template("add.html")

# PUT to update an existing company
@app.route('/companies/<string:name>', methods=['PUT'])
def update_company(name):
    # Read update data from request
    # Find and update the specified company
    # Save the updated data back to the file

    data = openFile(file_path, 'r')
    checkJSONHeaders(data)

    for i, rows in enumerate(data['Mainline']['Table']['Row']):
        if rows['Company'] == name:
            body = request.get_json()
            entry = data['Mainline']['Table']['Row'][i]

            # Check each legal entry and if applicable update
            if 'Company' in body:
                entry['Company'] = body['Company']

            if 'HomePage' in body:
                entry['HomePage'] = body['HomePage']

            if 'Hubs' in body and 'Hub' in body['Hubs']:
                entry['Hubs']['Hub'] = body['Hubs']['Hub']

            if 'Logo' in body:
                entry['Logo'] = body['Logo']

            if 'Revenue' in body:
                entry['Revenue'] = body['Revenue']

            if 'Services' in body:
                entry['Services'] = body['Services']

            # Save modified JSON back to file
            try:
                with open(file_path, 'w') as file:
                    json.dump(data, file, indent=4)
            except Exception:
                abort(500, description="JSON file missing")

            return jsonify({"success": "Successfully updated " + entry['Company']})

    abort(404, description="Company not found")

# DELETE a trucking company
@app.route('/companies/<string:name>', methods=['DELETE'])
def delete_company(name):
    # Locate and delete the specified company
    # Save the updated data back to the file

    data = openFile(file_path, 'r')
    checkJSONHeaders(data)
    rows = data['Mainline']['Table']['Row']

    for i, company in enumerate(rows):
        if company['Company'] == name:
            del rows[i]

            try:
                with open(file_path, 'w') as file:
                    json.dump(data, file, indent=4)
            except Exception:
                abort(500, "JSON file missing - id: d1")

            return jsonify({"success": "Successfully deleted " + name})

    abort(404, description="Company not found")

# Error handlers (optional to implement in their section)
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': error.description if hasattr(error, 'description') else 'Resource not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': error.description if hasattr(error, 'description') else 'Bad request'}), 400

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': error.description if hasattr(error, 'description') else 'Internal server error'}), 500



