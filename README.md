# Discord Music & Emojify Bot

A feature-rich Discord bot built with `discord.py` that provides high-quality music playback using Wavelink (Lavalink) and a fun image-to-emoji conversion tool.

## Features

### 🎵 Music Player
High-performance music streaming powered by Lavalink.
- **/play [keyword/url]**: Play audio from a keyword search or direct URL (YouTube supported).
- **/pause & /resume**: Control playback state.
- **/skip**: Skip the current track.
- **/stop**: Stop playback and clear the queue.
- **/queue**: View the current song queue.
- **/join & /disconnect**: Manually control the bot's voice channel connection.
- **Auto-disconnect**: Automatically leaves the channel when the queue is empty.

### 🖼️ Emojify
Convert images into emoji art!
- **!emojify [user/url] [size]**: Converts a user's avatar or an image URL into a grid of emojis.
  - `user/url`: Mention a user to use their avatar, or provide an image URL.
  - `size`: (Optional) Size of the emoji grid (default is 14).

### 🛠️ Utilities
- **/help**: Displays a list of all available commands and their descriptions.

## Prerequisites

- **Python 3.8+**
- **Java 13+** (Required for running `Lavalink.jar`)
- A Discord Bot Token (from the [Discord Developer Portal](https://discord.com/developers/applications))
- **Message Content Intent**: You must enable the "Message Content Intent" toggle in your bot's settings on the Discord Developer Portal for the `!emojify` command to work.

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd DiscordBot
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   Create a `.env` file in the root directory and add the following:
   ```env
   TOKEN=your_discord_bot_token
   HOST=127.0.0.1
   PW=youshallnotpass
   ```
   *Note: `HOST` and `PW` must match the configuration in `application.yml` for Lavalink.*

## Running the Bot

1. **Start the Lavalink Server**
   The bot requires a running Lavalink server for music functionality.
   ```bash
   java -jar Lavalink.jar
   ```

2. **Start the Bot**
   Open a new terminal window/tab and run:
   ```bash
   python main.py
   ```

## Project Structure

- `main.py`: Entry point of the bot. Handles startup and extension loading.
- `MusicPlayer.py`: Cog for music commands and Wavelink event handling.
- `Emojify.py`: Cog for the image-to-emoji conversion command.
- `emoji.py`: Helper logic for mapping image pixels to closest colored emojis.
- `Lavalink.jar`: The audio player server node.
- `application.yml`: Configuration for Lavalink.

## Dependencies

- `discord.py`: The core library for the Discord bot.
- `wavelink`: A robust Lavalink client for discord.py.
- `requests`: Used for fetching image data from URLs.
- `Pillow`: Used for image processing in the Emojify feature.
- `python-dotenv`: Loads environment variables from `.env`.
