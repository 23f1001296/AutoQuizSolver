import requests
from bs4 import BeautifulSoup
import re

def solve_quiz(url):
    try:
        # Step 1: Fetch the quiz page HTML
        res = requests.get(url, timeout=15)
        if res.status_code != 200:
            return {"error": f"Failed to fetch quiz page: {res.status_code}"}

        html = res.text
        soup = BeautifulSoup(html, "html.parser")

        # Step 2: Extract visible text (for debugging)
        question_text = soup.get_text(separator="\n")
        print("Question snippet:", question_text[:200])  # Optional for debugging

        # Step 3: Dummy solving logic (update later for real quiz)
        answer = 0

        # Step 4: Try to find submit URL (either <form action> or link)
        submit_url = None
        form = soup.find("form")
        if form and form.get("action"):
            submit_url = form["action"]
        else:
            possible = re.findall(r'https?://[^\s"]+/submit', html)
            if possible:
                submit_url = possible[0]

        return {"answer": answer, "submit_url": submit_url}

    except Exception as e:
        return {"error": str(e)}
