"""
API entrypoint for task_1.py and task_2.py
"""

from flask import Flask, request, jsonify
import task_1
import task_2

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return "OK", 200


@app.route("/task-1", methods=["GET"])
def get_data():
    """GET endpoint for task_1"""
    try:
        result = task_1.main()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/task-2", methods=["POST"])
def scrape_data():
    """POST endpoint for task_2, requires an URL as a query parameter"""
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL parameter is missing"}), 400
    try:
        result = task_2.main(url)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
