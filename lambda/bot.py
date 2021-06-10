import telegram
from emoji import emojize

with open(".key", "r") as f:
    API_KEY = f.read().strip()

CHAT_ID = -1001480260749

bot = telegram.Bot(token=API_KEY)


def lambda_handler(event, context):
    sns = event["Records"][0]["Sns"]
    bot.sendMessage(chat_id=CHAT_ID,
                    text=emojize(sns["Message"], use_aliases=True))
