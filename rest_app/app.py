"""
Flask Reverse API

This Flask application provides two endpoints:
- `/reverse`: Accepts a `text` query parameter, reverses the order of words, and caches the result.
- `/restore`: Returns the most recently cached result from `/reverse`.

Endpoints:
    GET /reverse?text=your+text+here
        Args:
            text (str): The text to reverse (words order).
        Returns:
            JSON: {"result": reversed_text} or error message.

    GET /restore
        Returns:
            JSON: {"result": cached_text} or error message if no cache exists.

Example usage:
    curl 'http://localhost:8000/reverse?text=hello+world'
    # {"result": "world hello"}

    curl 'http://localhost:8000/restore'
    # {"result": "world hello"}
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

cache: dict = {
    "result": None
}


@app.route('/reverse', methods=['GET'])
def reverse():
    input_text: str | None = request.args.get('text')

    if not input_text:
        return jsonify({"error": "Missing 'text' query parameter"}), 400

    cache['result'] = ' '.join(reversed(input_text.strip().split()))
    
    return jsonify({"result": cache['result']})


@app.route('/restore', methods=['GET'])
def restore():
    if cache['result'] is None:
        return jsonify({"error": "No previous result found"}), 404

    return jsonify({"result": cache['result']})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
