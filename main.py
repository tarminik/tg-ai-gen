"""
One-shot content generation and posting to Telegram channels.

When you run `python3 main.py`, we will:
1) Generate content for each configured channel using DeepSeek
2) Post the generated content to the channel via aiogram v3 Bot API

Notes:
- Ensure the bot is an admin of the channels you target
- Configure prompts per channel in `tg_config.py`
"""

import asyncio
from typing import Dict

from aiogram import Bot

from config import config
from tg_config import channel_id_to_prompt
from deepseek_client import generate_text


async def run_once() -> None:
    """
    Generate messages for all channels and send them once.

    We iterate sequentially to keep it simple and readable.
    If volume grows, we can switch to bounded concurrency later.
    """

    # Build the bot instance. The context manager ensures session cleanup.
    async with Bot(token=config.telegram.tg_bot_token) as bot:
        for channel_id_str, prompt in channel_id_to_prompt.items():
            channel_id = int(channel_id_str)  # aiogram accepts int chat_id

            try:
                # 1) Ask DeepSeek to generate the content for this channel.
                text = await generate_text(prompt)

                # 2) Send the text to the channel.
                await bot.send_message(chat_id=channel_id, text=text)

                print(f"[OK] Sent message to channel {channel_id}")
            except Exception as err:
                # Keep running for the rest even if one channel fails.
                print(f"[ERR] Failed for channel {channel_id}: {err}")


if __name__ == "__main__":
    asyncio.run(run_once())