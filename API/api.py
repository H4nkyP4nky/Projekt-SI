from flask import Flask, jsonify

# flask app's instance
api = Flask(__name__)

# endpoint
@api.route('/')
def home():
    return "API dla sieci szkół" # welcome message

# epi endpoint, json format
@api.route('/api/test', methods=['GET'])
def test():
    # python dictionary to json
    return jsonify({"message": "endpoint"}), 200 # 200 = http status

# local, easy reloading
if __name__ == '__main__':
    api.run(debug=True)
