
# YTBot 1.0 Update
A Music Bot By Mark

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

## MIT License

MIT License

Copyright (c) [2024] [Mark Li]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
