#!/usr/bin/env python3
# ======================================================
# ======  ____  _   _  ____  _   _  ____  _   _  ======
# ====== / ___|| | | ||  _ \| \ | ||  _ \| \ | | ======
# ====== \___ \| |_| || |_) |  \| || |_) |  \| | ======
# ======  ___) |  _  ||  _ <| |\  ||  __/| . ` | ======
# ====== |____/|_| |_||_| \_\_| \_||_|   |_|\_| ======
# ======================================================
# ======  Fetcher - Elite Cyber Threat Intel Grabber  ======
# ======  For DeepDarkCTI - Grabbing CTI from the shadows...  ======
# ======  Usage: python fetcher.py  ======
# ======  Grabs English messages from the last 4 hours from DeepDarkCTI Telegram channels  ======
# ======  Stay 1337, stay safe!  ======
# ======  WARNING: This script is for educational purposes only.  ======
# ======  Do not use for illegal activities. By using this script, you agree to take full responsibility.  ======
# ======================================================

import pyfiglet
import asyncio
import requests
import re
import time
import os
from telethon import TelegramClient
from telethon.tl.types import Channel
from datetime import datetime, timedelta, timezone
from tabulate import tabulate
import threading
import sys
from langdetect import detect, DetectorFactory

# Ensure consistent language detection
DetectorFactory.seed = 0

# Telegram API credentials (replace with your own)
api_id = 1234567  # Replace with your API ID from https://my.telegram.org
api_hash = 'your_api_hash_here'  # Replace with your API Hash from https://my.telegram.org
client = TelegramClient('session_name', api_id, api_hash)

# Hardcoded list of Telegram channels
channels = [
    'altenens', 'AntiPlumbers', 'base_brutesu', 'breachdetector', 'cbanke',
    'cbanke_logs', 'Configsandcombos', 'cpartisans', 'cveNotify', 'cyb3rtr0nian',
    'cybdetective', 'DarkfeedNews', 'databreach', 'dataflows', 'DBleak',
    'flannels', 'freedomf0x', 'gladdos69_official', 'grandgive', 'gulfdocs',
    'hadesh0p', 'HK4GANG', 'icrewhackers', 'itsecalert', 'jester_stealer_channel',
    'joker_logs1', 'latest_leaks', 'leakdataprivate', 'leaked_databases', 'LeaksData',
    'LeaRNEXploIT', 'lefousamples', 'Log_Market_Place', 'mailpassclub', 'MalwareLogs',
    'marketo_leaks', 'MBCRANSOMWARE', 'milkdude', 'openleak', 'pwnwiki_zhchannel',
    'ransomwatcher', 'sanaski', 'shieldteam1', 'silentplug666', 'snatch_news',
    'snatch_cloud', 'spamsmtpcombo', 'Storm_Free_Config', 'techpwnews',
    'We_are_not_eternal', 'windmarketo', 'Cracking_Pro', 'crackinghacks', 'ctinow',
    'offensiveTwitter', 'Offensiv3Sec', 'Hackgit', 'vxunderground', 'CyberSecurityNews',
    'ReverseEngineeringHangout'
]

# Event to signal when the script is done
done_event = threading.Event()

async def authenticate():
    """Handle Telegram authentication before any other operations."""
    session_file = 'session_name.session'
    if not os.path.exists(session_file):
        print("No session found. Please authenticate with your Telegram account.")
        try:
            await client.start()
            if not await client.is_user_authorized():
                print("Authentication failed. Please check your credentials and try again.")
                sys.exit(1)
            print("Authentication successful. Session saved.")
        except Exception as e:
            print(f"Error during authentication: {str(e)}")
            sys.exit(1)
    else:
        try:
            await client.connect()
            if not await client.is_user_authorized():
                print("Session invalid. Please authenticate again.")
                await client.start()
                if not await client.is_user_authorized():
                    print("Authentication failed. Please check your credentials and try again.")
                    sys.exit(1)
                print("Authentication successful. Session updated.")
        except Exception as e:
            print(f"Error connecting to Telegram: {str(e)}")
            sys.exit(1)

def check_last_github_fetch():
    """Check if 24 hours have passed since the last GitHub fetch."""
    last_check_file = "last_check.txt"
    current_time = time.time()
    one_day = 24 * 60 * 60  # 24 hours in seconds

    if os.path.exists(last_check_file):
        try:
            with open(last_check_file, 'r') as f:
                last_check = float(f.read().strip())
            if current_time - last_check < one_day:
                return False, last_check
        except (ValueError, IOError):
            pass
    return True, current_time

def update_last_github_fetch(timestamp):
    """Update the last GitHub fetch timestamp."""
    last_check_file = "last_check.txt"
    try:
        with open(last_check_file, 'w') as f:
            f.write(str(timestamp))
    except IOError as e:
        print(f"Error updating last check timestamp: {str(e)}")

def fetch_github_telegram_links():
    """Fetch Telegram links from all files in the DeepDarkCTI GitHub repository."""
    repo_url = "https://api.github.com/repos/fastfire/deepdarkCTI/contents"
    new_channels = set()
    
    try:
        # Get list of files in the repository
        print("Checking GitHub repository for new Telegram channels...")
        response = requests.get(repo_url, timeout=10)
        response.raise_for_status()
        files = response.json()

        # Regex for Telegram links
        channel_pattern = r'(?:@|t\.me/)([\w+]+)|t\.me/\+[\w-]+'

        # Iterate through files and folders
        for item in files:
            if item['type'] == 'file':
                # Fetch raw file content
                raw_url = item['download_url']
                try:
                    file_response = requests.get(raw_url, timeout=10)
                    file_response.raise_for_status()
                    content = file_response.text
                    # Find Telegram links
                    matches = re.findall(channel_pattern, content)
                    for match in matches:
                        if match:  # Handle tuple from regex groups
                            new_channels.add(match.strip())
                except requests.RequestException as e:
                    print(f"Error fetching file {item['name']}: {str(e)}")
            elif item['type'] == 'dir':
                # Recursively fetch files in directories
                dir_url = item['url']
                try:
                    dir_response = requests.get(dir_url, timeout=10)
                    dir_response.raise_for_status()
                    dir_files = dir_response.json()
                    for dir_item in dir_files:
                        if dir_item['type'] == 'file':
                            raw_url = dir_item['download_url']
                            try:
                                file_response = requests.get(raw_url, timeout=10)
                                file_response.raise_for_status()
                                content = file_response.text
                                matches = re.findall(channel_pattern, content)
                                for match in matches:
                                    if match:
                                        new_channels.add(match.strip())
                            except requests.RequestException as e:
                                print(f"Error fetching file {dir_item['name']}: {str(e)}")
                except requests.RequestException as e:
                    print(f"Error fetching directory {item['name']}: {str(e)}")

        return new_channels
    except requests.RequestException as e:
        print(f"Error checking GitHub repository: {str(e)}")
        return set()

def update_channels_list_file(new_channels):
    """Update the channels list in the script file with new valid channels."""
    script_file = __file__
    try:
        with open(script_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Find the channels list definition
        start_idx = -1
        end_idx = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('channels = ['):
                start_idx = i
            elif start_idx != -1 and line.strip().endswith(']'):
                end_idx = i
                break

        if start_idx == -1 or end_idx == -1:
            print("Error: Could not locate channels list in script file")
            return

        # Extract existing channels
        existing_channels = []
        for line in lines[start_idx+1:end_idx]:
            channel = line.strip().strip("',")
            if channel:
                existing_channels.append(channel)

        # Add new channels
        updated_channels = existing_channels + [ch for ch in new_channels if ch not in existing_channels]

        # Format the new channels list
        new_list_lines = ['channels = [\n']
        for i, ch in enumerate(updated_channels):
            new_list_lines.append(f"    '{ch}',{'' if i < len(updated_channels) - 1 else ''}\n")
        new_list_lines.append(']\n')

        # Rewrite the script file
        new_lines = lines[:start_idx] + new_list_lines + lines[end_idx+1:]
        with open(script_file, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
    except IOError as e:
        print(f"Error updating script file with new channels: {str(e)}")

def listen_for_keypress():
    """Run in a separate thread to listen for keypresses."""
    while not done_event.is_set():
        try:
            input()  # Wait for Enter key after any input
            if not done_event.is_set():
                print("I TOLD YOU I WAS BUSY, GIVE ME A MINUTE!")
        except EOFError:
            pass  # Handle Ctrl+C or other input errors gracefully

# Start the keypress listener in a background thread
keypress_thread = threading.Thread(target=listen_for_keypress, daemon=True)
keypress_thread.start()

async def main():
    # Print the banner
    print(pyfiglet.figlet_format("FETCHER", font="doom"))
    print("Elite Cyber Threat Intel Grabber for DeepDarkCTI")
    print("Usage: python fetcher.py")
    print("Grabs English messages from the last 4 hours from DeepDarkCTI Telegram channels")
    print("Stay 1337, stay safe!")
    print("\n")
    print("hang on, I'm busy...")  # Startup message
    print("\n")

    # Check for new Telegram channels from GitHub once a day
    should_check, current_time = check_last_github_fetch()
    new_channels = []
    valid_new_channels = []
    if should_check:
        new_channels = list(fetch_github_telegram_links())
        if new_channels:
            print(f"Found {len(new_channels)} new Telegram channels to validate: {', '.join(new_channels)}")
        else:
            print("No new Telegram channels found in GitHub repository")
        update_last_github_fetch(current_time)
    else:
        print("GitHub repository check skipped (less than 24 hours since last check)")

    async with client:
        # Validate new channels and collect valid ones
        for channel in new_channels:
            if channel not in channels:
                try:
                    entity = await client.get_entity(channel)
                    if isinstance(entity, Channel):
                        valid_new_channels.append(channel)
                    await asyncio.sleep(2)  # Avoid rate limits
                except Exception as e:
                    error_str = str(e)
                    # Skip channels with username errors
                    if "Nobody is using this username" in error_str or "No user has" in error_str:
                        continue
                    print(f"Error validating {channel}: {error_str}\n")

        # Add valid new channels to the hardcoded list and update the script file
        if valid_new_channels:
            channels.extend(valid_new_channels)
            print(f"Added {len(valid_new_channels)} valid channels to hardcoded list: {', '.join(valid_new_channels)}")
            update_channels_list_file(valid_new_channels)

        # Combine channels for this run
        combined_channels = channels

        four_hours_ago = datetime.now(timezone.utc) - timedelta(hours=4)
        table_data = []
        print("attempting to update table")
        for channel in combined_channels:
            try:
                entity = await client.get_entity(channel)
                if isinstance(entity, Channel):
                    messages = await client.get_messages(entity, limit=100)  # Fetch recent messages
                    for message in messages:
                        if message.date >= four_hours_ago:
                            text = message.text or "No text content"
                            # Skip welcome messages
                            if text and not ("welcome to" in text.lower() or "how are you?" in text.lower()):
                                # Check if the message is in English
                                try:
                                    if detect(text) == 'en':
                                        # Truncate message for table (max 300 characters)
                                        truncated_text = text[:300] + ("..." if len(text) > 300 else "")
                                        # Format timestamp
                                        timestamp = message.date.strftime("%Y-%m-%d %H:%M:%S UTC")
                                        table_data.append([channel, truncated_text, timestamp])
                                except:
                                    # Skip if language detection fails (assume non-English)
                                    continue
                else:
                    print(f"{channel} is not a channel\n")
                await asyncio.sleep(2)  # Avoid rate limits
            except Exception as e:
                error_str = str(e)
                # Suppress specific username errors
                if "Nobody is using this username" in error_str or "No user has" in error_str:
                    continue
                print(f"Error fetching {channel}: {error_str}\n")
        
        # Print table if there are valid messages
        if table_data:
            print("Messages from the last 4 hours (English only):")
            print(tabulate(table_data, headers=["Channel", "Message", "Timestamp"], tablefmt="grid"))
            print("\n")
    
    # Signal the keypress listener to stop
    done_event.set()

if __name__ == '__main__':
    try:
        # Run authentication first
        asyncio.run(authenticate())
        # Proceed with main operations
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped by user")
        done_event.set()
        sys.exit(0)
    finally:
        # Ensure client disconnection
        if client.is_connected():
            asyncio.run(client.disconnect())