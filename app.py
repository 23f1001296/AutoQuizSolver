import os, time
from flask import Flask, request, jsonify
from solver import solve_quiz
from utils.submitter import submit_answer

app = Flask(__name__)
SECRET = os.getenv("QUIZ_SECRET")
EMAIL = os.getenv("QUIZ_EMAIL")

@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "running", "message": "AutoQuizSolver ready."})

@app.route("/receive", methods=["POST"])
def receive():
    t0 = time.time()
    try:
        payload = request.get_json(force=True)
    except:
        return jsonify({"error": "Invalid JSON"}), 400

    email = payload.get("email")
    secret = payload.get("secret")
    url = payload.get("url")

    if not all([email, secret, url]):
        return jsonify({"error": "Missing required fields"}), 400
    if secret != SECRET:
        return jsonify({"error": "Invalid secret"}), 403

    result = solve_quiz(url)
    if "error" in result:
        return jsonify(result), 500

    answer, submit_url = result["answer"], result["submit_url"]
    response = submit_answer(submit_url, email, secret, url, answer)
    elapsed = round(time.time() - t0, 2)

    return jsonify({
        "status": "success",
        "answer": answer,
        "submit_response": response,
        "time_taken": f"{elapsed}s"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
