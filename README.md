# Joy SMS Forwarder

This is a Python script that forwards SMS messages to a Discord channel. It utilizes the Termux API to access SMS messages on an Android device and sends the messages to Discord using a webhook.

## Setup

1. Install [Termux](https://f-droid.org/repo/com.termux_118.apk) & [Termux Api](https://f-droid.org/repo/com.termux.api_51.apk) on your Android device.
2. Install the required packages by running the following command in Termux:

   ```shell
   pkg install python
   pkg install git
   ```

3. Clone this repository by running the following command:

   ```shell
   git clone https://github.com/JOY6IX9INE/SMS-FORWARDER
   ```

4. Change to the cloned directory:

   ```shell
   cd SMS-FORWARDER
   ```

5. Install the necessary Python packages by running the following command:

   ```shell
   pip install -r requirements.txt
   ```

6. Open the script file `main.py` in a text editor and replace the `webhook_url` variable with your Discord webhook URL. Make sure the URL is valid and has the appropriate permissions.

7. Save the changes to the script file.

## Usage

1. Open Termux on your Android device.
2. Change to the directory where the script is located:

   ```shell
   cd path/to/SMS-FORWARDER
   ```

3. Run the script by executing the following command:

   ```shell
   python main.py
   ```

4. The script will start monitoring SMS messages and forward any messages it detects to the specified Discord channel.

## Additional Notes

- You can customize the filters used to detect OTP or other messages by modifying the `filters` list in the script. Add or remove keywords as needed.
- Press `Ctrl + C` to stop the script.

**Note:** This script is specifically designed for Android devices running Termux and may not work on other platforms.

## Disclaimer

Please use this script responsibly and respect the privacy of others. Be aware of the legal and ethical implications of intercepting and forwarding SMS messages.
