# Before running: 
# 1. make sure you have box account credentials
# 2. install rclone
# 3. Follow instructions in data/README.txt so you have a remote called trecbox
# Running: exec get-data.sh {spotify-dir} 
# Example: exec get-data.sh Spotify-Podcasts-2020/podcasts-audio-only-2TB/podcasts-audio/0/F/show_0Fvt7eaJFKwwVengB9x9IZ/7zIPUGJIClsFZUTgB4BuQ2.ogg

rclone copy -P trecbox:$1 data/podcasts/

