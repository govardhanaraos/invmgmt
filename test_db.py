import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("DATABASE_URL")

try:
    conn = psycopg2.connect(url)
    print("✅ Database Connection Successful!")
    conn.close()
except Exception as e:
    print(f"❌ Connection Failed: {e}")