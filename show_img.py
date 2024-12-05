import subprocess
import json
import requests
from PIL import Image
from io import BytesIO

def fetch_api_data(url):
    try:
        result = subprocess.run(
            ["curl", "-s", url],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error fetching data: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

def find_card_image_by_name(base_url, display_name):
    url = base_url
    while url:
        data = fetch_api_data(url)
        if not data:
            break
        
        for card in data.get("results", []):
            if card.get("display_name").lower() == display_name.lower():
                return card.get("image", {}).get("normal")
        
        # next page
        url = data.get("next")
    
    return None

def fetch_and_display_image(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        image.show()  # uses default image viewer
    except requests.RequestException as e:
        print(f"Error fetching image: {e}")
    except Exception as e:
        print(f"Error displaying image: {e}")

card_display_name = input("Enter the card display name: ").strip()
api_url = "https://cards.fabtcg.com/api/search/v1/cards/?limit=100"

image_url = find_card_image_by_name(api_url, card_display_name)
if image_url:
    print(f"Displaying image for '{card_display_name}'...")
    fetch_and_display_image(image_url)
else:
    print(f"Card '{card_display_name}' not found.")
