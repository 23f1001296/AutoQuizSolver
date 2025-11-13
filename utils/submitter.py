import requests

def submit_answer(submit_url, email, secret, quiz_url, answer):
    payload = {
        "email": email,
        "secret": secret,
        "url": quiz_url,
        "answer": answer
    }
    try:
        res = requests.post(submit_url, json=payload, timeout=30)
        return res.json() if res.content else {"error": "No response"}
    except Exception as e:
        return {"error": str(e)}
