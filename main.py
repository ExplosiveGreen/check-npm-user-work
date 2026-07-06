import requests
import json
from datetime import datetime, timedelta

def total_months(dt_str):
    target_date = datetime.strptime(dt_str.replace("Z", ""), "%Y-%m-%dT%H:%M:%S.%f")
    current_date = datetime.now()

    total_months = (current_date.year - target_date.year) * 12 + (current_date.month - target_date.month)

    if current_date.day < target_date.day:
        total_months -= 1

    return total_months

def diffrence_in_packages():
    current_date = datetime.now()
    prev_date = datetime.now() - timedelta(days=1)
    with open(f'logs/{current_date.date()}.json',"r") as fp:
        current_json = json.load(fp)
    with open(f'logs/{prev_date.date()}.json',"r") as fp:
        prev_json = json.load(fp)
    return [x for x in current_json if x not in prev_json]
    
data = requests.get("https://registry.npmjs.org/-/v1/search?text=maintainer:t3dotgg")
packages = json.loads(data.text)
updated_past_month = filter(lambda package: total_months(package["package"]["date"]) < 2 , packages["objects"])
with open(f'logs/{datetime.now().date()}.json',"w+") as fp:
    json.dump([(package["package"]["name"], package["package"]['links']) for package in updated_past_month], fp)
new_packages = diffrence_in_packages()
if new_packages:
    print("send message")