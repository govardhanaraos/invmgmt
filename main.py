import os
from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_db, Investment
import calculate_performance as engine
from dotenv import load_dotenv
import os
# This explicitly loads the .env file from the current directory
load_dotenv()

app = FastAPI()

# Security: Set this in your .env file
CRON_SECRET = os.getenv("CRON_SECRET", "my_super_secret_key_123")

# Now this will fetch the real value from .env
DATABASE_URL = os.getenv("DATABASE_URL")

@app.post("/cron/daily-performance-check")
def daily_performance_check(api_key: str, db: Session = Depends(get_db)):
    """
    Endpoint for cron-job.org to trigger daily logic.
    """
    # 1. Security Check
    if api_key != CRON_SECRET:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    # 2. Fetch all investments from Aiven
    investments = db.query(Investment).all()
    if not investments:
        return {"status": "No investments found in DB"}

    # 3. Run Business Logic (Fetch NAVs and calculate)
    performance_data = engine.get_live_performance(investments)

    # 4. Trigger WhatsApp via Twilio
    try:
        whatsapp_sid = engine.send_performance_notification(performance_data)
        return {
            "status": "success",
            "message": "WhatsApp sent",
            "sid": whatsapp_sid,
            "data": performance_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"WhatsApp failed: {str(e)}")