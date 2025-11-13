import requests, re
import pandas as pd
from playwright.sync_api import sync_playwright
import pdfplumber
from io import BytesIO

def extract_pdf_text(url):
    r = requests.get(url)
    with pdfplumber.open(BytesIO(r.content)) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

def solve_quiz(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")

            text = page.inner_text("body")
            links = [a.get_attribute("href") for a in page.query_selector_all("a") if a.get_attribute("href")]

            data_link = next((l for l in links if l.lower().endswith(('.csv', '.pdf'))), None)
            submit_url = next((l for l in links if "submit" in l), None)

            if data_link and data_link.endswith(".csv"):
                df = pd.read_csv(data_link)
                if "value" in df.columns:
                    answer = int(df["value"].sum())
                else:
                    numeric_cols = df.select_dtypes(include='number').columns
                    answer = int(df[numeric_cols[0]].sum()) if len(numeric_cols) else None
            elif data_link and data_link.endswith(".pdf"):
                pdf_text = extract_pdf_text(data_link)
                numbers = [int(x) for x in re.findall(r"\d+", pdf_text)]
                answer = sum(numbers)
            else:
                match = re.search(r"(\d+)", text)
                answer = int(match.group(1)) if match else 0

            browser.close()
            return {"answer": answer, "submit_url": submit_url}
    except Exception as e:
        return {"error": str(e)}
