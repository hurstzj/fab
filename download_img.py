import subprocess
import json
import requests
import os

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
        
        # next page if available
        url = data.get("next")
    
    return None

def download_image(image_url, file_name):
    try:
        response = requests.get(image_url)
        response.raise_for_status()

        # save image
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"Image saved as '{file_name}'")
    except requests.RequestException as e:
        print(f"Error downloading image: {e}")

# from user input
card_display_name = input("Enter the card display name: ").strip()
api_url = "https://cards.fabtcg.com/api/search/v1/cards/?limit=100"

# Fetch URL
image_url = find_card_image_by_name(api_url, card_display_name)
if image_url:
    # valid file name for the image
    file_name = f"{card_display_name.replace(' ', '_').replace('/', '_')}.webp"
    print(f"Downloading image for '{card_display_name}'...")
    download_image(image_url, file_name)
else:
    print(f"Card '{card_display_name}' not found.")
