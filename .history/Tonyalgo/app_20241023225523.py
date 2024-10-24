from flask import Flask, request, jsonify
import tonyalgo  # Ensure this matches the name of your script file
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # This line enables CORS for your Flask app

@app.route('/run-script', methods=['POST'])
def run_script():
    # Get parameters from the request if needed
    api_key= "067dd15b9d0807e3990e984320fc7a0b"
    result = tonyalgo.main(api_key)
     # Modify your_script to accept parameters as needed
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)