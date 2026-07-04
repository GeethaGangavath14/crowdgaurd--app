import pandas as pd
import requests
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# ----------------- Load Environment Variables -----------------
load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TWOFACTOR_API_KEY = os.getenv('TWOFACTOR_API_KEY')

# ----------------- Evacuation Points -----------------
EVACUATION_POINTS = {
    'Gate 1 (Main Entrance)': {'lat': 17.4047, 'lon': 78.5501},
    'Gate 3 (VIP Gate)': {'lat': 17.4054, 'lon': 78.5512},
    'Parking Area A': {'lat': 17.4045, 'lon': 78.5495},
    'Parking Area B': {'lat': 17.4052, 'lon': 78.5505},
    'Emergency Assembly Point': {'lat': 17.4049, 'lon': 78.5508}
}

ZONE_TO_EVACUATION_MAPPING = {
    'North Pavilion': 'Gate 1 (Main Entrance)',
    'South Pavilion': 'Gate 3 (VIP Gate)',
    'East Stand': 'Parking Area A',
    'West Stand': 'Parking Area B',
    'VIP Box': 'Gate 3 (VIP Gate)',
    'General Stands': 'Emergency Assembly Point',
    'Stand 1 (North Zone)': 'Gate 1 (Main Entrance)',
    'Main Gate': 'Gate 1 (Main Entrance)',
}

# ----------------- Helper Functions -----------------
def get_evacuation_point(zone):
    return ZONE_TO_EVACUATION_MAPPING.get(zone, 'Emergency Assembly Point')

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    try:
        response = requests.post(url, data=payload)
        if response.json().get("ok"):
            print("✅ Telegram alert sent.")
        else:
            print(f"❌ Telegram Error: {response.text}")
    except Exception as e:
        print(f"❌ Telegram Exception: {e}")

def send_email(recipient, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())
        server.quit()
        print(f"✅ Email sent to {recipient}")
    except Exception as e:
        print(f"❌ Email Error: {e}")

def send_sms(phone_number, body):
    try:
        if not phone_number.startswith("+91"):
            phone_number = "+91" + phone_number[-10:]
        
        message = body.replace(" ", "%20")  # Simple URL encoding for spaces

        url = f"https://2factor.in/API/V1/{TWOFACTOR_API_KEY}/SMS/{phone_number[3:]}/{message}"

        response = requests.get(url)
        try:
            result = response.json()
            if result.get("Status") == "Success":
                print(f"✅ SMS sent to {phone_number}")
            else:
                print(f"❌ SMS Error: {result}")
        except Exception as parse_error:
            print(f"❌ SMS Parse Error: {parse_error}")
            print(f"❌ Response Text: {response.text}")

    except Exception as e:
        print(f"❌ SMS Exception: {e}")

# ----------------- Main Alert Logic -----------------
def trigger_alert(zone_detected, person_count):
    evacuation_point = get_evacuation_point(zone_detected)
    location = EVACUATION_POINTS.get(evacuation_point)

    if location:
        lat, lon = location['lat'], location['lon']
        google_maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
    else:
        google_maps_link = "https://www.google.com/maps"

    message = (f"⚠️ ALERT! Overcrowding detected at {zone_detected}. "
               f"People: {person_count}. Evacuate to {evacuation_point}. "
               f"Navigate here: {google_maps_link}")

    try:
        df = pd.read_csv("registered_users.csv")
        for _, row in df.iterrows():
            email = str(row['Email']).strip()
            phone = str(row['Phone']).strip()

            send_email(email, "CrowdGuard Evacuation Alert", message)
            send_sms(phone, message)

        send_telegram_message(message)
        print("🚨 Alerts triggered successfully.")
    except Exception as e:
        print(f"❌ Error sending alerts: {e}")

# ----------------- Run Example -----------------
if __name__ == "__main__":
    trigger_alert('Main Gate', 2)  # Example: Simulate overcrowding at 'Main Gate' with 2 people
