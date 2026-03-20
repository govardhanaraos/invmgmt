import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_TOKEN"))

try:
    # This just fetches account info to verify the SID/Token are valid
    account = client.api.accounts(os.getenv("TWILIO_SID")).fetch()
    print(f"✅ Success! Connected to: {account.friendly_name}")
except Exception as e:
    print(f"❌ Error: {e}")