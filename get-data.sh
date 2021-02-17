# Before running: 
# 1. make sure you have box account credentials
# 2. install rclone
# 3. Follow instructions in data/README.txt so you have a remote called trecbox
# Running: exec get-data.sh {spotify-dir} 
# Example: exec get-data.sh Spotify-Podcasts-2020/podcasts-audio-only-2TB/podcasts-audio/0/F/show_0Fvt7eaJFKwwVengB9x9IZ/7zIPUGJIClsFZUTgB4BuQ2.ogg

# For each complete path
for var in "$@"
do
    # Split the path according to /
    IFS=$'/'
    read -a remotepatharr <<< "$var"

    # Removing the last component of the array
    localpathstr=${remotepatharr[@]::${#remotepatharr[@]}-1}

    # Split the resultant text to join it with /
    IFS=$' '
    read -a localpatharr <<< "$localpathstr"
    IFS=$'/'
    localpathstr="${localpatharr[*]}"
    IFS=$' '

    remotepath="trecbox:Spotify-Podcasts-2020/podcasts-audio-only-2TB/podcasts-audio/$var"
    localpath="./data/spotify-podcasts-2020/podcasts-transcripts/$localpathstr"

    printf "\nDownloading file: $remotepath \nInto: $localpath\n\n"

    # Retrieve the remote audio file into the local path
    rclone copy -P $remotepath $localpath
done