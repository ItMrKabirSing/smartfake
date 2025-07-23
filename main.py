# Copyright @ISmartCoder
# Updates Channel https://t.me/TheSmartDev
from flask import Flask, jsonify, request, render_template
import json
import random
import os
import pycountry

app = Flask(__name__)

@app.route('/', methods=['GET'])
def status():
    return render_template('status.html')

@app.route('/api/address', methods=['GET'])
def get_address():
    country_code = request.args.get('code', '').upper()
    if not country_code:
        return jsonify({
            "error": "Country code is required",
            "api_owner": "@ISmartCoder",
            "api_updates": "t.me/TheSmartDev"
        }), 400
    
    file_path = os.path.join('data', f"{country_code.lower()}.json")
    try:
        with open(file_path, 'r') as file:
            addresses = json.load(file)
        
        if not addresses:
            return jsonify({
                "error": "No addresses found for this country code",
                "api_owner": "@ISmartCoder",
                "api_updates": "t.me/TheSmartDev"
            }), 404
        
        random_address = random.choice(addresses)
        random_address["api_owner"] = "@ISmartCoder"
        random_address["api_updates"] = "t.me/TheSmartDev"
        return jsonify(random_address)
    
    except FileNotFoundError:
        return jsonify({
            "error": "Country code not found",
            "api_owner": "@ISmartCoder",
            "api_updates": "t.me/TheSmartDev"
        }), 404
    except Exception as e:
        return jsonify({
            "error": str(e),
            "api_owner": "@ISmartCoder",
            "api_updates": "t.me/TheSmartDev"
        }), 500

@app.route('/api/countries', methods=['GET'])
def get_countries():
    try:
        data_dir = 'data'
        countries = []
        
        # Check if data directory exists
        if not os.path.exists(data_dir):
            return jsonify({
                "error": "Data directory not found",
                "api_owner": "@ISmartCoder",
                "api_updates": "t.me/TheSmartDev"
            }), 404

        # Iterate through .json files in data directory
        for filename in os.listdir(data_dir):
            if filename.endswith('.json'):
                country_code = filename.split('.')[0].upper()
                # Get country name from pycountry
                country = pycountry.countries.get(alpha_2=country_code)
                country_name = country.name if country else "Unknown"
                
                countries.append({
                    "country_code": country_code,
                    "country_name": country_name
                })
        
        if not countries:
            return jsonify({
                "error": "No countries found",
                "api_owner": "@ISmartCoder",
                "api_updates": "t.me/TheSmartDev"
            }), 404

        return jsonify({
            "countries": sorted(countries, key=lambda x: x["country_name"]),
            "api_owner": "@ISmartCoder",
            "api_updates": "t.me/TheSmartDev"
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "api_owner": "@ISmartCoder",
            "api_updates": "t.me/TheSmartDev"
        }), 500

@app.errorhandler(404)
def page_not_found(e):
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Error</title>
        <style>
            body {
                background-color: #ffffff;
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                color: #333;
            }
            .error-message {
                text-align: center;
                font-size: 24px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="error-message">Error: Wrong Endpoint</div>
    </body>
    </html>
    ''', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
