import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """Scrape information from LinkedIn profiles and handle errors gracefully."""

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/LorenBenDavid/0164d400deb1d4edbea9dd3d1eefd7b9/raw/a1fab7ffd3b6bb21bab73224e0b4dce47b57b8a0/loren-ben-david-scrapin.json"
        try:
            response = requests.get(linkedin_profile_url, timeout=10)
            response.raise_for_status() 
            print(f"🔍 Mock API response: {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error with mock request: {e}")
            return None
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.environ["SCRAPIN_API_KEY"],  
            "linkedInUrl": linkedin_profile_url, 
        }

        print(
            f"🔍 Sending request to Scrapin API: {api_endpoint} with params: {params}")
        try:
            response = requests.get(api_endpoint, params=params, timeout=10)
            response.raise_for_status() 


            print(f"🔍 API response status: {response.status_code}")

            print(f"🔍 API response JSON: {response.json()}")

        except requests.exceptions.RequestException as e:
           
            print(f"⚠️ Error with API request: {e}")
            return None

    # Parsing JSON response
    try:

        data = response.json().get("person")

 
        if not data:
            print(
                f"⚠️ No valid data found for the LinkedIn profile: {linkedin_profile_url}")
            return None

    except ValueError as e:
        print(f"⚠️ Error parsing JSON: {e}")
        return None

    data = {k: v for k, v in data.items() if v not in (
        [], "", None) and k not in ["certifications"]}

    return data  


if __name__ == "__main__":
    linkedin_url = "https://www.linkedin.com/in/loren-ben-david-a26370268/"
    result = scrape_linkedin_profile(linkedin_profile_url=linkedin_url)
    print(result)
