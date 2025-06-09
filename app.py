from flask import Flask, request, jsonify
from Nl2Sql import database_question

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")
    result = database_question(question)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')