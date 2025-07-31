from flask import Flask, request, jsonify

app = Flask(__name__)
last_result = {"result": ''}


@app.route('/reverse', methods=['GET'])
def reverse():
    input_text = request.args.get('text')
    if not input_text:
        return jsonify({"error": "Missing 'text' query parameter"}), 400

    reversed_words = ' '.join(reversed(input_text.strip().split()))
    last_result["result"] = reversed_words
    return jsonify({"result": reversed_words})


@app.route('/restore', methods=['GET'])
def restore():
    if last_result["result"] is None:
        return jsonify({"error": "No previous result found"}), 404

    return jsonify({"result": last_result["result"]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
