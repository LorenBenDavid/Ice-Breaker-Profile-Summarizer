import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """Scrape information from LinkedIn profiles and handle errors gracefully."""

    if mock:
        # במקרה של פיתוח, השתמש בקובץ mock לדוגמה
        linkedin_profile_url = "https://gist.githubusercontent.com/LorenBenDavid/0164d400deb1d4edbea9dd3d1eefd7b9/raw/a1fab7ffd3b6bb21bab73224e0b4dce47b57b8a0/loren-ben-david-scrapin.json"
        try:
            response = requests.get(linkedin_profile_url, timeout=10)
            response.raise_for_status()  # מוודא שהתגובה לא כוללת שגיאות
            # הדפסת התגובה במקרה של mock
            print(f"🔍 Mock API response: {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error with mock request: {e}")
            return None
    else:
        # קריאה לשירות Scrapin.io API
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.environ["SCRAPIN_API_KEY"],  # המפתח שלך
            "linkedInUrl": linkedin_profile_url,  # ה-URL של לינקדאין
        }

        # לוג קריאת API
        print(
            f"🔍 Sending request to Scrapin API: {api_endpoint} with params: {params}")
        try:
            # שלח את הבקשה ל-API עם פרמטרים
            response = requests.get(api_endpoint, params=params, timeout=10)
            response.raise_for_status()  # מוודא שאין שגיאות בקריאה ל-API

            # בדוק את סטטוס התגובה
            # לוג סטטוס של התגובה
            print(f"🔍 API response status: {response.status_code}")

            # הדפסת התגובה המלאה (JSON) לשם ביקורת
            # הדפסת התגובה שקיבלת
            print(f"🔍 API response JSON: {response.json()}")

        except requests.exceptions.RequestException as e:
            # במקרה של שגיאה בתקשורת או ב-API
            print(f"⚠️ Error with API request: {e}")
            return None

    # Parsing JSON response
    try:
        # חילוץ נתוני פרופיל האיש
        data = response.json().get("person")

        # אם אין נתונים או שהתשובה ריקה, הצג שגיאה
        if not data:
            print(
                f"⚠️ No valid data found for the LinkedIn profile: {linkedin_profile_url}")
            return None

    except ValueError as e:
        # במקרה שהתגובה לא תקינה
        print(f"⚠️ Error parsing JSON: {e}")
        return None

    # מסנן את הנתונים כדי להסיר ערכים ריקים
    data = {k: v for k, v in data.items() if v not in (
        [], "", None) and k not in ["certifications"]}

    return data  # מחזירים את הנתונים הסופיים


if __name__ == "__main__":
    linkedin_url = "https://www.linkedin.com/in/loren-ben-david-a26370268/"
    result = scrape_linkedin_profile(linkedin_profile_url=linkedin_url)
    print(result)
