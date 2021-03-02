README - Spotify Podcasts 2020 Dataset
======

Last modified 2020-DEC-23

Dataset Title: 
Spotify Podcasts 2020 Dataset
Data Version:
2020-MAY-14
Test Set Version:
2020-JUL-21
Contact: 
podcasts-challenge-organizers@spotify.com
When using this dataset please cite this paper: 
"100,000 Podcasts: A Spoken English Document Corpus" by Ann Clifton, Sravana Reddy, Yongze Yu, Aasish Pappu, Rezvaneh Rezapour, Hamed Bonab, Maria Eskevich, Gareth Jones, Jussi Karlgren, Ben Carterette, and Rosie Jones, COLING 2020

Permission to use - You must sign up for TREC here: https://ir.nist.gov/trecsubmit.open/application.html 
and also sign the data usage agreement which can be obtained by by contacting: podcasts-challenge-organizers@spotify.com

How to Download From Box.com
============================
You can download directly from the website, or from the command line using rclone. Box.com also provides other tools.

From website
-	When you are given access to the shared directory on Box.com you will be able to right-click on a file or directory and select download

-  	We recommend first downloading the subdirectory podcasts-no-audio-13GB/ which contains transcripts, rss, scripts, metadata, etc., to your project.
	Then if you also want the ~ 2TB of audio data, download podcasts-audio-only-2TB.  If you download the entire Spotify-Podcast-2020 directory
	the entire dataset would take up ~2Tb disk space. See below for descriptions of the subdirectories and space requirements.

OR

Using rclone

$curl https://rclone.org/install.sh | sudo bash
$rclone config
- No remotes found - make a new one  n/s/q> n
- name> trecbox 
- Choose a number from below, or type in your own value Storage> 6
- client_id>:  #enter leave empty
- client_secret>: #enter leave empty
- box_config_file>: #enter leave empty
- box_sub_type>: 1
- Edit advanced config? (y/n)  y/n> n
- Use auto config? (y/n)  y/n> n
- Then paste the result below:
	- $rclone authorize box #run this on a seperate terminal
	- result> {"access_token":"....","token_type":"...","refresh_token":".....","expiry":"...."}

$rclone ls trecbox:
$rclone copy -P trecbox:{PODCASTS_DIRECTORY} /path/to/your/project

OR

Other Tools You can Use
https://www.box.com/resources/downloads/drive


Unpacking and checking your downloaded data set
===============================================

There are two sub-directories, podcasts-audio-only-2TB and podcasts-no-audio-13GB in main directory in box.com. The contents in those directories are described below.


Audio files
-----------

There are 105360 ogg files arranged in the show-id subdirectories in the podcasts-audio-only-2TB directory. For details, please refer to section data structure below.

Transcripts
-----------
There are three tar files of transcripts in podcasts-no-audio-13GB directory
podcasts-transcripts-0to2.tar.gz (4.6 GB)- 39892 transcripts
podcasts-transcripts-3to5.tar.gz (4.6 GB)- 41273 transcripts
podcasts-transcripts-6to7.tar.gz (2.8 GB)- 24195 transcripts


Untar on Unix/Mac using 
tar -xzvf <filename>.tar -C <your_data_path>

All three tar files untar to the same directory with the subdirectories which will be described in next section: 
spotify-podcasts-2020/podcasts-transcripts/0/A/show_*/*.json

Check the total number of transcripts files:
$find spotify-podcasts-2020/podcasts-transcripts/ -name '*.json' |wc -l
105360

RSS Headers
-----------
The single tar file containing xml files for 18,376 distinct podcast shows untars to the directory with the subdirectories:
spotify-podcasts-2020/show-rss/0/A/show_*.xml

Check the total number of RSS header files:
$find spotify-podcasts-2020/show-rss/ -name '*.xml' |wc -l
 18376

Metadata
--------
There is a metadada.tsv for preview and a duplicate copy as a single tar file metadata.tar.gz which will untar into:
spotify-podcasts-2020/metadata.tsv

Fields and explanations in metadata.tsv :
- show_uri :  Spotify uri for the show. e.g. spotify:show:7gozmLqbcbr6PScMjc0Zl4
- show_name :  Name of the show. e.g. Reply All
- show_description : Description of the show. e.g. "'A podcast about the internet' that is actual…”
- publisher : Publisher of the show. e.g. Gimlet
- language : Language the show is in in BCP 47 format. e.g. [en]
- rss_link: links of show rss feed. e.g. https://feeds.megaphone.fm/replyall
- episode_uri : Spotify uri for the episode. e.g. spotify:episode:4vYOibPeC270jJlnRoAVO6
- episode_name : Name of the episode. e.g. #109 Is Facebook Spying on You?
- episode_description :	Description of the episode. e.g. “This year we’ve gotten one question more than …”
- duration : duration of the episode in minutes. e.g. 31.680000
- show_filename_prefix: Filename_prefix of the show. e.g. show_7gozmLqbcbr6PScMjc0Zl4
- episode_filename_prefix: Filename_prefix of the episode. e.g. 4vYOibPeC270jJlnRoAVO6

Scripts
-------
A single tar file scripts.tar.gz containing helper scripts and files untars into:
spotify-podcasts-2020/scripts/. Please refer to section "Retraction of episodes".

Summarization Test Set
----------------------
There is also a tar file of test episodes for summarization 
spotify-podcasts-2020-summarization-testset.tar.gz  (147MB, 1027 episodes)
It contains metadata, transcripts and RSS headers in the same format as above.


Dataset description (unpacked)
===================

README 		this README

metadata.tsv	the metadata associated with each podcast episode - one line per episode

show-rss/ 			RSS headers made by podcast show creators in XML format. One RSS header file per show, named using show_filename_prefix, Spotify URI for the show, given in metadata.tsv. Each show contains multiple episodes. Not all episodes in the RSS headers are included in the dataset.

podcasts-transcripts/	transcripts consist of JSON format files, one per podcast episode. Each transcript is named using the episode_filename_prefix given in metadata.tsv. 

podcasts-audio/ 	an OGG format audio file per podcast episode. Each OGG file is named using the episode_filename_prefix given in metadata.tsv. 

scripts/ 		contains utility scripts
compliance.py - a deletion script which MUST be run before using the data. 

trec2020podcastsTrackGuidelines.txt	Task Guidelines for TREC2020 podcasts challenge


Directory structure (unpacked)
===================

The data set is organized into subdirectories under the transcripts and audio directories by the first two characters of the show-id to avoid overwhelming filesystem operations. The show-ids and the episode-ids are alphanumeric character sequences of length 22. Since some operating systems do not distinguish between upper and lower case, the subdirectory paths are all in upper case and include both upper and lower case show-ids in the same subdirectory. 

The default data structure is:
    $ spotify-podcasts-2020/podcasts-transcripts/0/A/show_*/*.json
    $ spotify-podcasts-2020/podcasts-audio/0/A/show_*/*.ogg
    $ spotify-podcasts-2020/show-rss/0/A/show_*.xml
    $ spotify-podcasts-2020/metadata.tsv 
    $ spotify-podcasts-2020/scripts/compliance.py
    $ spotify-podcasts-2020/scripts/delete_file.txt 

Retraction of episodes
======================
 
Occasionally some episodes may be retracted from the data set. When this happens, this will be communicated to all participants, and you are required to comply with the deletion. To facilitate this, a deletion script - compliance.py - has been provided in the scripts directory. If you retain the default directory structure as given above without renaming files, you can simply run the compliance script as per below and it will do the deletion for you; otherwise you will be responsible for deleting the requested items yourself.

Run the deletion script using:
`$ cd spotify-podcasts-2020/
 $ python3 scripts/compliance.py`

The file "delete_file.txt" has two columns which are show_filename_prefix and episode_filename_prefix.
It could be empty if nothing needs to be deleted. When delete requests are issued, we will update the delete_file.txt in the repository and ask you to download it. 
Example : 
        show_0F2zZNU9wzNSfAW1IJTjU2,2rPk0aN8NIArjJuJEqz8KL
        show_0F2zZNU9wzNSfAW1IJTjU2,5m0lPlDNjMeFjtukFBFpiC
        show_0f2P0fH4EwuEtXKpXIt7Ui,0BDVyuIPWhu8XoG5y9m7nF

============= END OF README.txt - Spotify Podcasts 2020 Dataset




