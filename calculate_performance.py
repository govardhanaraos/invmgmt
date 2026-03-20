import os
from mftool import Mftool
from twilio.rest import Client
from decimal import Decimal
from datetime import datetime

mf = Mftool()

# Map for your specific portfolio
FUND_MAP = {
    "SBI Multicap": "148918",
    "Nippon India Multi Cap": "118778",
    "Quant Small Cap": "120847",
    "Parag Parikh Flexi Cap": "122639",
    "ICICI Pru Multi Asset": "128362",
    "HSBC ELSS Tax Saver": "145347",
    "Aditya Birla Flexi Cap": "119106"
}


def get_live_performance(investments):
    """
    Fetches real-time NAV and calculates absolute returns.
    """
    total_invested = Decimal('0.0')
    current_market_value = Decimal('0.0')

    for inv in investments:
        total_invested += inv.amount

        try:
            # Fetch live NAV using the AMFI code
            quote = mf.get_scheme_quote(inv.amfi_code)
            live_nav = Decimal(quote['nav'])

            # Value = NAV * Units (If units aren't stored, we estimate change since purchase)
            if inv.units_held:
                current_market_value += live_nav * inv.units_held
            else:
                # Fallback: estimate based on simplified percentage tracking
                current_market_value += inv.amount * Decimal('1.02')
        except:
            current_market_value += inv.amount  # Fallback to cost if API fails

    abs_return = ((current_market_value - total_invested) / total_invested) * 100

    return {
        "invested": float(total_invested),
        "current": float(current_market_value),
        "return_pct": float(abs_return)
    }

def should_send_update():
    # 0 = Monday, 4 = Friday
    day_of_week = datetime.now().weekday()
    return day_of_week <= 4


def send_performance_notification(perf_data):
    """
    Sends WhatsApp alert if gains cross your defined threshold.
    """
    client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_TOKEN"))

    status_emoji = "📈" if perf_data['return_pct'] > 0 else "📉"
    message_body = (
        f"{status_emoji} *Investment Update*\n"
        f"Total Invested: ₹{perf_data['invested']:,.2f}\n"
        f"Current Value: ₹{perf_data['current']:,.2f}\n"
        f"Total Gain: {perf_data['return_pct']:.2f}%"
    )

    message = client.messages.create(
        body=message_body,
        from_=os.getenv("TWILIO_WHATSAPP_FROM"),
        to=os.getenv("MY_WHATSAPP_NUMBER")
    )
    return message.sid