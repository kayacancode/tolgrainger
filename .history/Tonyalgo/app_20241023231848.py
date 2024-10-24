from flask import Flask, request, jsonify
import tonyalgo  # Ensure this matches the name of your script file
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app, resources={r"/run-script": {"origins": "http://localhost:3000"}})  # Adjust if needed

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        # Get parameters from the request if needed
        api_key= "067dd15b9d0807e3990e984320fc7a0b"
        result = tonyalgo.main(api_key)
        # Modify your_script to accept parameters as needed
        print("Response from the script:", result) 
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return HTTP 500 error code if an error occurs

if __name__ == '__main__':
    app.run(debug=True)
