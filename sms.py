import vonage
import Base
import Flashscore
import datetime

for league in Base.leagues:
    games = Flashscore.getUpcomingFlashscore(league, f"{datetime.datetime.today().day}-{datetime.datetime.today().month}")


def sendsms(text):
    client = vonage.Client(key="c48d7fab", secret="9LmDvpoLTqCNNVl7")
    sms = vonage.Sms(client)

    responseData = sms.send_message(
        {
            "from": "Vonage APIs",
            "to": "48884364610",
            "text": f"{text}"
        }
    )

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
