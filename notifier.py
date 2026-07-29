import json
import requests

secrets = "config/secrets.json"

webhook_bazos = ""
webhook_error = ""
webhook_sbazar = ""

with open(secrets) as file:
    content = json.load(file)
    content = content["webhooks"]
    webhook_bazos = content["bazos"]
    webhook_sbazar = content["sbazar"]
    webhook_error = content["error"]


def send_discord_message(message, site):
    webhook = ""

    if site == "bazos":
        webhook = webhook_bazos
    elif site == "sbazar":
        webhook =  webhook_sbazar

    elif site == "error":
        webhook = webhook_error
    else:
        webhook = webhook_error
        message =  f"site: {site} or message: {message} is invalid"

    payload = {
            "content": message
            }

    response = requests.post(webhook, json=payload)

    if response.status_code == 204:
        return True

    else:
        print(f"sending msg failed {response.status_code}, {response.text}")
        return False

if __name__ == "__main__":
    send_discord_message("test", "bazos")
