import os
from dotenv import load_dotenv

# 1. Load the .env file
# override=True ensures that if you have windows system variables with the same name,
# the .env file values will take priority during this test.
load_dotenv(override=True)


def verify_credentials():
    print("--- Environment Variable Diagnostic ---")

    # List of keys we expect to find
    keys = ["DATABASE_URL", "TWILIO_SID", "TWILIO_TOKEN", "CRON_SECRET"]

    all_found = True
    for key in keys:
        value = os.getenv(key)
        if value:
            # We obscure the value for security, but show enough to confirm it's not a placeholder
            display_value = value[:10] + "..." if len(value) > 10 else value
            print(f"✅ {key}: Found ({display_value})")
        else:
            print(f"❌ {key}: NOT FOUND")
            all_found = False

    if all_found:
        print("\n🎉 Success! Your .env file is being read correctly.")

        # Specific check for the 'YOUR_HOST' error you saw earlier
        db_url = os.getenv("DATABASE_URL", "")
        if "YOUR_HOST" in db_url or "hostname" in db_url:
            print("⚠️ WARNING: DATABASE_URL still contains placeholder text!")
    else:
        print("\n\a ERROR: One or more variables are missing.")
        print(f"Current Working Directory: {os.getcwd()}")
        if not os.path.exists(".env"):
            print("🚨 PHYSICAL FILE MISSING: No .env file found in this folder.")


if __name__ == "__main__":
    verify_credentials()