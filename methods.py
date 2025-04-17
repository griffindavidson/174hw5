from flask import jsonify, abort
import json, base64, os

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

def convertBase64ToImage(base64_str, filename):
    if base64_str.startswith('data:image'):
        # Split out the header if included
        header, base64_str = base64_str.split(',', 1)

    try:
        # Decode the base64 string
        image_data = base64.b64decode(base64_str)

        # Save to file (you can change the directory as needed)
        with open(filename, 'wb') as f:
            f.write(image_data)

    except Exception as e:
        print("Failed to decode and save image:", e)
        return jsonify({"Error": "Failed to save image"}), abort(500)

        