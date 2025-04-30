
# Fetcher

**Cyber Threat Intel Grabber for DeepDarkCTI**

This Python script fetches English-language messages from the last 4 hours from Telegram channels listed in the `fastfire/deepdarkCTI` GitHub repository and a hardcoded list. It checks the repository daily for new Telegram channels, validates them, and adds valid channels to the hardcoded list in the script. The output is displayed in a clean terminal table using `tabulate`.

**WARNING**: This script is for **educational purposes only**. Do not use for illegal activities. By using this script, you agree to take full responsibility for your actions.

## Features

- **Telegram Authentication**: Prompts for phone number, login code, and optional two-factor authentication password before any operations (e.g., banner, GitHub check) on first run or if the session is invalid.
- **Daily GitHub Check**: Scans the `fastfire/deepdarkCTI` repository for new Telegram channels every 24 hours.
- **Persistent Channel Updates**: Adds valid (error-free) channels to the hardcoded `channels` list in `fetcher.py`.
- **English-Only Messages**: Filters messages using `langdetect` to include only English content.
- **Recent Messages**: Fetches messages from the last 4 hours.
- **Clean Output**: Displays results in a terminal table with columns for Channel, Message (truncated to 300 characters), and Timestamp.
- **Message Filtering**: Excludes welcome messages (e.g., "welcome to", "how are you?").
- **Error Suppression**: Suppresses specific Telegram username errors (e.g., "Nobody is using this username").
- **Rate Limiting**: Respects Telegram API limits with a 2-second delay between requests.

## Prerequisites

- **Python 3.6+**: Ensure Python is installed (`python --version`).
- **Telegram API Credentials**: Obtain an API ID and Hash from my.telegram.org.
- **Telegram Account**: A phone number registered with Telegram for initial authentication.
- **GitHub Access**: The script queries the public `fastfire/deepdarkCTI` repository (no authentication required).

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/allthecyvbers/fetcher.git
   cd fetcher
   ```

2. **Install Dependencies**:

   Save the provided `requirements.txt` and install:

   ```bash
   pip install -r requirements.txt
   ```

   This installs:

   - `telethon`: For Telegram API interactions and authentication.
   - `pyfiglet`: For the ASCII banner.
   - `tabulate`: For terminal table output.
   - `requests`: For GitHub API requests.
   - `langdetect`: For English message filtering.

3. **Obtain Telegram API Credentials**:

   - Visit my.telegram.org and log in with your phone number.
   - Click “API development tools” &gt; “Create new application.”
   - Fill in:
     - **App title**: e.g., “CTI Fetcher”
     - **Short name**: e.g., “Fetcher”
     - **Platform**: “Desktop”
     - **App URL/Description**: Optional (e.g., “http://localhost”)
   - Copy the **API ID** (e.g., `1234567`) and **API Hash** (e.g., `0123456789abcdef0123456789abcdef`).

4. **Configure the Script**:

   - Open `fetcher.py` in a text editor.

   - Replace the placeholder credentials:

     ```python
     api_id = 1234567
     api_hash = 'your_api_hash_here'
     ```

     with your credentials, e.g.:

     ```python
     api_id = 1234567
     api_hash = '0123456789abcdef0123456789abcdef'
     ```

   - Save the file.

## Usage

1. **Run the Script**:

   ```bash
   python fetcher.py
   ```

   - **First Run or Invalid Session**:

     - The script prompts for Telegram authentication before any other operations:
       - **Phone number**: Enter in international format (e.g., `+12025550123`).
       - **Login code**: Enter the code sent to your Telegram app.
       - **Password**: If two-factor authentication is enabled, enter your Telegram account password.
     - After successful authentication, a `session_name.session` file is created to store the session, preventing future prompts unless the session is deleted or invalidated.
     - Example authentication prompt:

       ```
       No session found. Please authenticate with your Telegram account.
       Phone number (+1234567890): +12025550123
       Enter the code sent to your Telegram app: 12345
       Authentication successful. Session saved.
       ```

   - **Subsequent Runs**: If a valid `session_name.session` exists, the script skips authentication and proceeds directly to fetching messages.

   - **General Output**:

     - After authentication, the script displays an ASCII banner, status messages, and a table of English messages from the last 4 hours.

     - A `last_check.txt` file tracks the last GitHub check timestamp.

     - Example output (after authentication):

       ![image](https://github.com/user-attachments/assets/23807ec3-7afd-4823-8aec-2ba0464e0d54)



## Files

- **fetcher.py**: The main script that authenticates with Telegram, fetches, and displays messages.
- **requirements.txt**: Lists Python dependencies.
- **session_name.session**: Created after first successful authentication to store Telegram session data (do not share).
- **last_check.txt**: Tracks the last GitHub check timestamp.

## Troubleshooting

- **Authentication Issues**:

  - **Error**: “Invalid phone number”
    - **Fix**: Use the international format (e.g., `+12025550123`). Ensure the number is registered with Telegram.
  - **Error**: “Invalid code”
    - **Fix**: Verify the code sent to your Telegram app. Request a new code if expired.
  - **Error**: “Two-factor authentication password required”
    - **Fix**: Enter the password set for your Telegram account.
  - **Error**: “Session invalid”
    - **Fix**: Delete `session_name.session` and rerun to re-authenticate.
  - **Error**: “Error during authentication: ...”
    - **Fix**: Check your API credentials in `fetcher.py`. Ensure internet connectivity and correct phone number.

- **GitHub Check Fails**:

  - **Error**: “Error checking GitHub repository: HTTPSConnectionPool...”

    - **Fix**: Check internet connection, retry later, or use a GitHub Personal Access Token in `fetcher.py`:

      ```python
      headers = {'Authorization': 'token your_token'}
      response = requests.get(repo_url, headers=headers, timeout=10)
      ```

  - **Error**: “404 Client Error: Not Found”

    - **Fix**: Verify the repository at https://github.com/fastfire/deepdarkCTI.

- **New Channels Not Added**:

  - **Cause**: Channels may be invalid or private.
    - **Fix**: Check channel names in the GitHub repository or via `t.me/channel_name`. Ensure you have access to private channels.

- **Non-English Messages Appear**:

  - **Cause**: `langdetect` misclassification.

    - **Fix**: Add a minimum text length check in `fetcher.py`:

      ```python
      if detect(text) == 'en' and len(text) > 10:
      ```

- **Script File Not Updated**:

  - **Error**: “Error updating script file with new channels: Permission denied”
    - **Fix**: Ensure write permissions for `fetcher.py` (`chmod u+w fetcher.py`).

- **No Messages in Output**:

  - **Cause**: No English messages in the last 4 hours.

    - **Fix**: Verify channels via `t.me/channel_name`. Adjust the time window in `fetcher.py`:

      ```python
      four_hours_ago = datetime.now(timezone.utc) - timedelta(hours=8)
      ```

- **Table Misalignment**:

  - **Fix**: Widen the terminal or reduce truncation in `fetcher.py`:

    ```python
    truncated_text = text[:200] + ("..." if len(text) > 200 else "")
    ```

- **Rate Limits**:

  - **Error**: “FloodWaitError: A wait of X seconds is required”

    - **Fix**: Wait the specified time or increase the delay in `fetcher.py`:

      ```python
      await asyncio.sleep(5)
      ```

## Notes

- **Authentication**: The script prompts for a phone number, login code, and optional password before any operations on the first run or if `session_name.session` is missing/invalid. After successful authentication, the session file prevents future prompts.
- **Channel Growth**: The script adds valid Telegram channels to the hardcoded list, which may increase runtime over time. Manually prune the `channels` list in `fetcher.py` if it grows too large.
- **Language Detection**: `langdetect` may misclassify short or mixed-language messages. Non-detectable messages are excluded.
- **Security**: Protect your Telegram API credentials and `session_name.session` file to secure your account. Do not share the session file.
- **Legal Compliance**: Ensure you have permission to access Telegram channels per Telegram’s Terms of Service and local laws.

## Contributing

Contributions are welcome! Please:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- fastfire/deepdarkCTI for the Telegram channel data.

---

**Stay 1337, stay safe!**
