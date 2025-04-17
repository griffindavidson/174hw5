from flask import jsonify, abort
import json

def openFile(path, privileges):

    try:
        with open(path, privileges) as file:
            data = json.load(file)
            return data
    except:
        abort(500)

def checkJSONHeaders(jsonData):
    if 'Mainline' not in jsonData or \
        'Table' not in jsonData['Mainline'] or \
        'Header' not in jsonData['Mainline']['Table'] or \
        'Data' not in jsonData['Mainline']['Table']['Header'] or \
        not jsonData['Mainline']['Table']['Header']['Data']:
            abort(500)

    if 'Row' not in jsonData['Mainline']['Table']:
        abort(500)

        