import os

BOT_TOKEN = None  # token
admins = []  # Your id

if os.getenv("API_KEY") is None:
    print(BOT_TOKEN)
    raise Exception("None API_KEY")

if not os.getenv("ADMINS") is None:
    admins = os.getenv("ADMINS").split(";")[::-1][1:]

BOT_TOKEN = os.getenv("API_KEY")
