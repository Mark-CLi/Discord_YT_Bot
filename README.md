# YTBot 1.1 Update
A Music Bot By Mark

## New Features
 
- **Added Command** `!ythelp` command, this will show as an embed message of all available command
- **Discord Token** Discord token get read from `Discord_Token.txt` instead of showing in the .py file itself for security

# YTBot 1.0 Update

## New Features

- **Scheduled File Deletion**: Using the Linux script, files are now scheduled for deletion. This includes `Cornjob` and `delete_mp3.sh`.
- **Queue Feature**: Added the `!queue` command. You can also use `!play` while a file is already playing.
- **Enhanced Play Command**: The `!play` command now searches for files if a non-valid URL is detected.
- **Skip Feature**: Added the `!skip` command to skip currently playing files.
- **Nuke Queue Feature**: Added `!nuke` to clear the entire queue.
- **Stop Queue(Bot Disconnect)** : The `!stop` command will disconnect the bot from current voice channel

## Installation Instructions

1. **Discord Library**
   ```
   pip install discord.py
   ```

2. **yt-dlp for YouTube Downloads**
   ```
   pip install yt-dlp
   ```

3. **FFmpeg Library for Audio Processing**
   For Ubuntu/Debian:
   ```
   sudo apt-get install ffmpeg
   ```

4. **Moving Files to Your Linux Machine**
   - Create a folder:
     ```
     mkdir project/production/YTBot
     ```
   - Move your files to the YTBot directory.
  
5. **Make your bot token File**
   - For Linux
   ```
   cd path/to/your/BOT/Folder
   ```
   - Create the file
   ```
   touch Discord_Token.txt
   ```
   - Edit the file
   ```
   nano Discord_Token.txt
   ```
   - Paste your discord token into the file
   - Save and exit (Ctrl+O, Enter, Ctrl+X).

  6. **Edit the Python file to direct the bot to the right Path**
      - Assume you are already cd in the correct path
     ```
      nano Bot.py
      ```
      - edit
      ```
      with open('path/to/your/BOT/Folder/Discord_Token.txt','r') as file:
       TOKEN = file.read().strip()
      ```
      - Save and exit (Ctrl+O, Enter, Ctrl+X).
   

8. **Install and Use Screen for Background Running**
   - Install Screen:
     ```
     sudo apt-get install screen
     ```
   - Start Screen session:
     ```
     screen
     ```
   - Run your Python script:
     ```
     python3 [path to your Python script]
     ```
   - Detach from Screen session:
     ```
     Ctrl-A then Ctrl-D
     ```
   - To return to the session:
     ```
     screen -r
     ```

9. **Setup Cronjob for Scheduled Deletion**
   - Change the directory to where your shell script is located.
   - Edit crontab:
     ```
     crontab -e
     ```
   - Add the following line to schedule the job:
     ```
     0 9 * * * /path/to/delete_mp3.sh
     ```
   - Save and exit (Ctrl+O, Enter, Ctrl+X).
   - Verify the scheduled jobs:
     ```
     crontab -l
     ```
