import subprocess
import json

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
        
        # go to next page
        url = data.get("next")
    
    return None

# display name from user input
card_display_name = input("Enter the card display name: ").strip()
api_url = "https://cards.fabtcg.com/api/search/v1/cards/?limit=100"

# fetch image URL
image_url = find_card_image_by_name(api_url, card_display_name)
if image_url:
    print(f"Image URL for '{card_display_name}': {image_url}")
else:
    print(f"Card '{card_display_name}' not found.")
