
# YTBot 1.0 Update

## New Features

- **Scheduled File Deletion**: Using the Linux script, files are now scheduled for deletion. This includes `Cornjob` and `delete_mp3.sh`.
- **Queue Feature**: Added the `!queue` command. You can also use `!play` while a file is already playing.
- **Enhanced Play Command**: The `!play` command now searches for files if a non-valid URL is detected.
- **Skip Feature**: Added the `!skip` command to skip currently playing files.
- **Nuke Queue Feature**: Added `!nuke` to clear the entire queue.

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

5. **Install and Use Screen for Background Running**
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
     python3 [path to your python script]
     ```
   - Detach from Screen session:
     ```
     Ctrl-A then Ctrl-D
     ```
   - To return to the session:
     ```
     screen -r
     ```

6. **Setup Cronjob for Scheduled Deletion**
   - Change directory to where your shell script is located.
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
