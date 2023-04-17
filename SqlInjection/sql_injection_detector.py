import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys


session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"})


def get_all_forms(url):
    content = session.get(url).content
    soup = BeautifulSoup(content, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    details = {}
    action = form.attrs.get("action").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []

    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})

    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details


def contains_sql_error(content):
    errors = [
        "You have an error in your SQL syntax",
        "Warning: mysql_fetch_array()",
        "Warning: mysql_fetch_assoc()",
        "Warning: mysql_num_rows()",
        "Warning: mysql_result()",
        "Warning: pg_exec()",
        "Warning: pg_query()",
        "Warning: oci_execute()",
        "Warning: odbc_exec()",
    ]
    for error in errors:
        if error in content:
            return True
    return False


def detect_sql_injection(url):
    response = session.get(f"{url}'")
    if contains_sql_error(response.content.decode("utf-8", errors="ignore")):
        print(f"[!] SQL Injection vulnerability detected in URL: {url}")
        return

    for form in get_all_forms(url):
        form_details = get_form_details(form)
        data = {input_dict["name"]: input_dict["value"] for input_dict in form_details["inputs"] if input_dict["name"]}

        # Convert relative URL to absolute URL
        action_url = urljoin(url, form_details["action"])

        response = session.request(form_details["method"], action_url, data=data)
        if contains_sql_error(response.content.decode("utf-8", errors="ignore")):
            print(f"[!] SQL Injection vulnerability detected in form: \n{form.prettify()}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 sql_injection_detector.py <url>")
        sys.exit(1)
    url = sys.argv[1]
    detect_sql_injection(url)
