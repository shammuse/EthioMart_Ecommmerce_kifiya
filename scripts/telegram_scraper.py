# Import liberaries
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class TelegramScraper:
    def __init__(self):
        # Fetch credentials from environment variables
        self.api_id = int(os.getenv('API_ID'))
        self.api_hash = os.getenv('API_HASH')
        self.phone_number = os.getenv('phone')

        # Create the Telegram client using the credentials
        self.client = TelegramClient('session_name', self.api_id, self.api_hash)
    
    async def connect(self):
        """Connect to the Telegram client."""
        await self.client.start(self.phone_number)
        print("Connected to Telegram")

    async def fetch_messages(self, channels, message_limit=5000, output_file='telegram_messages.csv'):
        """Fetch messages from the list of channels."""
        all_messages = []

        for channel in channels:
            print(f"Joining and fetching messages from {channel}...")
            try:
                # Join the channel using the channel username
                await self.client(JoinChannelRequest(channel))

                # Get the channel entity by username
                entity = await self.client.get_entity(channel)

                # Iterate through messages in the channel with the specified limit
                async for message in self.client.iter_messages(entity, limit=message_limit):  
                    message_data = {
                        'channel': channel,
                        'message_id': message.id,
                        'date': message.date.isoformat(),
                        'sender': message.sender_id,
                        'Message': message.text if message.text else '',
                        'media': None  # Placeholder for media info
                    }

                    # Check for media and save media type/name without downloading
                    if message.media:
                        media_type = message.media.__class__.__name__  # Get media type/class name
                        message_data['media'] = media_type

                    print(f"Saving message {message.id} from {channel}")

                    # Append message data to the list
                    all_messages.append(message_data)

            except Exception as e:
                print(f"Error fetching messages from {channel}: {str(e)}")

        # Create a DataFrame from the collected messages
        df = pd.DataFrame(all_messages)

        # Save the DataFrame to a CSV file
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Finished fetching messages and saved to {output_file}.")
    
    async def disconnect(self):
        """Disconnect the Telegram client."""
        await self.client.disconnect()
        print("Disconnected from Telegram")
