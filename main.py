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

def package_key(pkg):
    return (
        pkg["package"]["name"],
        pkg["package"]["version"]
    )

def diff_packages(current, previous):
    previous_keys = {package_key(pkg) for pkg in previous}

    return [
        pkg for pkg in current
        if package_key(pkg) not in previous_keys
    ]    

data = requests.get("https://registry.npmjs.org/-/v1/search?text=maintainer:t3dotgg")
packages = json.loads(data.text)
created_past_month, updated_past_month = (
    list(filter(lambda package: total_months(package["package"]["date"]) < 2 , packages["objects"])),
    list(filter(lambda package: total_months(package["updated"]) < 2 , packages["objects"]))
)
with open(f'logs/updated_{datetime.now().date()}.json',"w+") as fp:
    json.dump(list(updated_past_month), fp)
with open(f'logs/created_{datetime.now().date()}.json',"w+") as fp:
    json.dump(list(created_past_month), fp)

prev_date = datetime.now() - timedelta(days=1)
with open(f'logs/created_{prev_date.date()}.json',"r") as fp:
    prev_created_json = json.load(fp)
with open(f'logs/updated_{prev_date.date()}.json',"r") as fp:
    prev_updated_json = json.load(fp)

new_created_packages = diff_packages(created_past_month, prev_created_json)
new_updated_packages = diff_packages(updated_past_month, prev_updated_json)

events = [
    json.dumps({
        'name': pkg['package']['name'],
        'version': pkg['package']['version'],
        'date': pkg['package']['date'],
        'links': pkg['package']['links'],
        'type': "CREATED"
    })
    for pkg in new_created_packages
] + [
    json.dumps({
        'name': pkg['package']['name'],
        'version': pkg['package']['version'],
        'date': pkg['updated'],
        'links': pkg['package']['links'],
        'type': "UPDATED"
    })
    for pkg in new_updated_packages
]

with open(f'logs/events_{datetime.now().date()}.jsonl', "w+") as fp :
    fp.write('\n'.join(events))

# if new_packages:
#     print("send message")