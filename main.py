import os
import json
import requests
import colorama
from colorama import Fore
import ctypes

colorama.init()
os.system('mode con: cols=85 lines=28')
ctypes.windll.kernel32.SetConsoleTitleW('Discord Server Info | Created by Ali')

def sanitize_filename(filename):
    """Sanitizes filenames by replacing invalid characters with underscores."""
    return ''.join(c if c.isalnum() or c in (' ', '_') else '_' for c in filename)

def save_json_data(filepath, data):
    """Saves data to a JSON file."""
    os.makedirs('saved', exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def load_config(filepath='./data/config.json'):
    """Loads configuration from a JSON file."""
    with open(filepath, 'r') as file:
        return json.load(file)

def fetch_discord_server_info():
    """Fetches and displays Discord server information."""
    config = load_config()

    while True:
        invite_code = input(f"{Fore.LIGHTYELLOW_EX}[{Fore.RESET}+{Fore.LIGHTYELLOW_EX}] Enter the Discord invite code: {Fore.RESET}")
        url = f"https://discord.com/api/v9/invites/{invite_code}?with_counts=true&with_expiration=true"
        headers = {
            'accept': 'application/json',
            'accept-language': 'en',
            'user-agent': 'ios:2.65.0:488:14:iPhone13,3',
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            guild = data.get("guild", {})
            guild_id = guild.get("id", "Not found")
            guild_name = guild.get("name", "Not found")
            description = guild.get("description", "No description available")
            member_count = data.get("approximate_member_count", "Not available")
            presence_count = data.get("approximate_presence_count", "Not available")
            verification_level = guild.get("verification_level", "Not available")
            vanity_url_code = guild.get("vanity_url_code", "Not available")
            nsfw_level = guild.get("nsfw_level", "Not available")
            nsfw = guild.get("nsfw", "Not available")
            premium_subscription_count = data.get("premium_subscription_count", "Not available")
            splash = guild.get("splash", None)
            banner = guild.get("banner", None)
            icon = guild.get("icon", None)
            expires_at = data.get("expires_at", "Not available")
            invite_type = data.get("type", "Not available")

            splash_url = f"https://cdn.discordapp.com/splashes/{guild_id}/{splash}.png" if splash else "Splash not available"
            banner_url = f"https://cdn.discordapp.com/banners/{guild_id}/{banner}.png" if banner else "Banner not available"
            icon_url = f"https://cdn.discordapp.com/icons/{guild_id}/{icon}.png" if icon else "Icon not available"

            # Add URLs to data dictionary
            data.update({
                "splash_url": splash_url,
                "banner_url": banner_url,
                "icon_url": icon_url
            })

            if config.get("save_invite_json", False):
                filename = f"{sanitize_filename(invite_code)}.json"
                save_json_data(os.path.join('saved', filename), data)

            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}${Fore.LIGHTGREEN_EX}] Server Name: {Fore.RESET}{guild_name}")
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}${Fore.LIGHTGREEN_EX}] Server ID: {Fore.RESET}{guild_id}")
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}${Fore.LIGHTGREEN_EX}] Description: {Fore.RESET}{description}")
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}${Fore.LIGHTGREEN_EX}] Total Members: {Fore.RESET}{member_count}")
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}${Fore.LIGHTGREEN_EX}] Online Members: {Fore.RESET}{presence_count}")
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}${Fore.LIGHTGREEN_EX}] Verification Level: {Fore.RESET}{verification_level}")
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}${Fore.LIGHTGREEN_EX}] Custom URL Code: {Fore.RESET}{vanity_url_code}")
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}${Fore.LIGHTGREEN_EX}] NSFW Level: {Fore.RESET}{nsfw_level}")
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}${Fore.LIGHTGREEN_EX}] NSFW Status: {Fore.RESET}{nsfw}")
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}${Fore.LIGHTGREEN_EX}] Server Boosts: {Fore.RESET}{premium_subscription_count}")
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}${Fore.LIGHTGREEN_EX}] Splash Image URL: {Fore.RESET}{splash_url}")
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}${Fore.LIGHTGREEN_EX}] Banner Image URL: {Fore.RESET}{banner_url}")
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}${Fore.LIGHTGREEN_EX}] Icon Image URL: {Fore.RESET}{icon_url}")
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}${Fore.LIGHTGREEN_EX}] Invite Expires At: {Fore.RESET}{expires_at}")
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}${Fore.LIGHTGREEN_EX}] Invite Code: {Fore.RESET}{invite_code}")
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}${Fore.LIGHTGREEN_EX}] Invite Type: {Fore.RESET}{invite_type}")

            break

        except requests.RequestException as e:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{Fore.LIGHTRED_EX}[{Fore.RESET}-{Fore.LIGHTRED_EX}] Request error: {str(e)}. Please try again.")

    input(f"{Fore.LIGHTYELLOW_EX}Press Enter to exit...")

if __name__ == "__main__":
    fetch_discord_server_info()