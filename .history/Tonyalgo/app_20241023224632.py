from flask import Flask, request, jsonify
import tonyalgo  # Ensure this matches the name of your script file

app = Flask(__name__)

@app.route('/run-script', methods=['POST'])
def run_script():
    # Get parameters from the request if needed
    data = request.json
    # You can modify the script to accept parameters here
    result = your_script.main(api_key='067dd15b9d0807e3990e984320fc7a0b')  # Modify your_script to accept parameters as needed
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
