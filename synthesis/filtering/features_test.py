import audio_filtering as af

filename = 'smaller7tmono.wav'

res = af.pitch_energy(filename)

print(len(res[0]))

'''
This will depend on the length of the audio, the sample rate and the volume of the audio. A better metric is the Power which is energy per second


#power - energy per unit of time
1.0/(2*(channel1.size)+1)*np.sum(channel1.astype(float)**2)/rate

Next i wanted to plot my track. I plotted the amplitude over time for each channel


import matplotlib.pyplot as plt

#create a time variable in seconds
time = np.arange(0, float(audData.shape[0]), 1) / rate

#plot amplitude (or loudness) over time
plt.figure(1)
plt.subplot(211)
plt.plot(time, channel1, linewidth=0.01, alpha=0.7, color='#ff7f00')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.subplot(212)
plt.plot(time, channel2, linewidth=0.01, alpha=0.7, color='#ff7f00')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()



The next thing to look at is the frequency of the audio. In order to do this you need todecompose the single audio wave into audio waves at different frequencies. This can be done using a Fourier transform. However, the last time I thought about Fourier transforms was at university, so I thought I better brush up. I went through the first few weeks of this free signal processing course on coursera, and it was a great help.

The Fourier transform effectively iterates through a frequency for as many frequencies as there are records (N) in the dataset, and determines the Amplitude of that frequency. The frequency for record (fk) can be calculated using the sampling rate (fs)



The following code performs the Fourier transformation on the left channel sound and plots it. The maths produces a symetrical result, with one real data solution, and an imaginary data solution


from numpy import fft as fft

fourier=fft.fft(channel1)

plt.plot(fourier, color='#ff7f00')
plt.xlabel('k')
plt.ylabel('Amplitude')



We only need the real data solution, so we can grab the first half, then calculate the frequency and plot the frequency against a scaled amplitude.


n = len(channel1)
fourier = fourier[0:(n/2)]

# scale by the number of points so that the magnitude does not depend on the length
fourier = fourier / float(n)

#calculate the frequency at each point in Hz
freqArray = np.arange(0, (n/2), 1.0) * (rate*1.0/n);

plt.plot(freqArray/1000, 10*np.log10(fourier), color='#ff7f00', linewidth=0.02)
plt.xlabel('Frequency (kHz)')
plt.ylabel('Power (dB)')




Another common way to analyse audio is to create a spectogram. Audio spectograms are heat maps that show the frequencies of the sound in Hertz (Hz), the volume of the sound in Decibels (dB), against time.

In order to calculate a Fourier transform over time the specgram function used below uses a time window based Fast Fourier transform. This simplifies the calculation involved, and makes it possible to do in seconds. It calculates many Fourier transforms over blocks of data ‘NFFT’ long. Each Fourier transform over a block, results in the frequencies represented in that block, and to what magnitude. So the resultant array is NFFT times smaller than the original data. The range of frequencies explored relates to half the sample rate. The number of samples in the block (NFFT) determines how many frequencies in that range are considered. So a bigger block results in a greater frequency range, but reduces the information with respect to time.


plt.figure(2, figsize=(8,6))
plt.subplot(211)
Pxx, freqs, bins, im = plt.specgram(channel1, Fs=rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
cbar=plt.colorbar(im)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
cbar.set_label('Intensity dB')
plt.subplot(212)
Pxx, freqs, bins, im = plt.specgram(channel2, Fs=rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
cbar=plt.colorbar(im)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
cbar.set_label('Intensity (dB)')
#plt.show()



The result allows us to pick out a certain frequency and examine it


np.where(freqs==10034.47265625)
MHZ10=Pxx[233,:]
plt.plot(bins, MHZ10, color='#ff7f00')



So thats the basics of audio processing. I’m now looking forward to analysing my favourite music. I’m sure there will be posts on that to come.

As always all of the above code can be found together in the following gist

Posted on April 17, 2017 by James Thomson This entry was posted in matplotlib, Python, Spectogram, Uncategorized and tagged .mp3, .wav, amplitude, audio, fourier transform, frequency, hertz, numpy, python, spectogram. Bookmark the permalink.
POST NAVIGATION
← CLUSTERING ZEPPELIN ON ZEPPELIN
10 THOUGHTS ON “AUDIO SIGNALS IN PYTHON”
MATT SANDY SAYS:
APRIL 20, 2017 AT 4:24 AM
This is really cool. I have been meaning to do something similar, looking for patterns and whatnot, but in R.

REPLY
FLAVIO SAYS:
APRIL 24, 2017 AT 12:21 AM
I received the following error (even using hardcoded path in from_mp3() method:

Do you know what I’m doing wrong?

—————————————————————————
OSError Traceback (most recent call last)
in ()
2 #urllib.urlretrieve(web_file,temp_folder+”file.mp3″)
3 #read mp3 file
—-> 4 mp3 = pydub.AudioSegment.from_mp3(“/Users/myname/Downloads/audio_analysis/file.mp3″)
5 #convert to wav
6 mp3.export(temp_folder+”file.wav”, format=”wav”)

/usr/local/lib/python2.7/site-packages/pydub/audio_segment.pyc in from_mp3(cls, file)
512 @classmethod
513 def from_mp3(cls, file):
–> 514 return cls.from_file(file, ‘mp3’)
515
516 @classmethod

/usr/local/lib/python2.7/site-packages/pydub/audio_segment.pyc in from_file(cls, file, format, **kwargs)
495 log_conversion(conversion_command)
496
–> 497 p = subprocess.Popen(conversion_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
498 p_out, p_err = p.communicate()
499

/usr/local/Cellar/python/2.7.13/Frameworks/Python.framework/Versions/2.7/lib/python2.7/subprocess.pyc in __init__(self, args, bufsize, executable, stdin, stdout, stderr, preexec_fn, close_fds, shell, cwd, env, universal_newlines, startupinfo, creationflags)
388 p2cread, p2cwrite,
389 c2pread, c2pwrite,
–> 390 errread, errwrite)
391 except Exception:
392 # Preserve original exception in case os.close raises.

/usr/local/Cellar/python/2.7.13/Frameworks/Python.framework/Versions/2.7/lib/python2.7/subprocess.pyc in _execute_child(self, args, executable, preexec_fn, close_fds, cwd, env, universal_newlines, startupinfo, creationflags, shell, to_close, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite)
1022 raise
1023 child_exception = pickle.loads(data)
-> 1024 raise child_exception
1025
1026

OSError: [Errno 2] No such file or directory

REPLY
JAMES THOMSON SAYS:
APRIL 25, 2017 AT 8:05 PM
The error you are getting:
OSError: [Errno 2] No such file or directory
Suggests its not finding the file. Is there definitely a file called file.mp3 in the directory?
If not, it sounds like the line before it isn’t working properly
urllib.urlretrieve(web_file,temp_folder+”file.mp3″)

REPLY
ALEC SAYS:
DECEMBER 25, 2017 AT 9:27 AM
Would you try to use linux as your default system?

REPLY
ALYSSA SAYS:
NOVEMBER 13, 2017 AT 6:55 PM
Can you elaborate a bit on the last 3 lines:

np.where(freqs==10034.47265625)
MHZ10=Pxx[233,:]
plt.plot(bins, MHZ10, color=’#ff7f00′)

What exactly is this doing?

REPLY
JAMES THOMSON SAYS:
NOVEMBER 15, 2017 AT 9:38 AM
its just finding the array at 10MHZ, extracting it, and then plotting it

REPLY
BAILEY SAYS:
JANUARY 16, 2018 AT 8:58 PM
Hi, I have a few questions:
1. Can you cite the equation you used and how it relates to the Fourier Transform?
2. What does the value for ‘k’ mean in the equation/second graph you used? And what unit is it at as well?
3. How does amplitude relate to the equation you used, and how did you solve for amplitude without having it within the equation?
Thank you!

REPLY
JAMES THOMSON SAYS:
JANUARY 17, 2018 AT 12:01 PM
k refers to the period or time in the audio. so fk is the frequency at a given time. to answer your other questions would take a lot of explaining instead i really recommend you go through the online signal processing course i suggested in the blog as they explain clear than i could. its also totally free

REPLY
PHANI RITHVIJ SAYS:
JUNE 25, 2018 AT 1:28 PM
Sugesstion:
By averaging we get a damaged wav file as you’ve suggested but it can be fixed by another completely unrelated to averaging method

Use pydub for extracting mono to prevent damage to the audio

mono = pydub.AudioSegment.from_wav(‘Music/file.wav’)
mono.set_channels(1)
mono.export(‘Music/pydubfile.wav’, format=”wav”)

REPLY
MADHURANANDA PAHAR SAYS:
NOVEMBER 12, 2019 AT 11:04 AM
This is very helpful for a beginner to get into audio processing in Python. There are some other libraries like librosa which would do the jobs, but it is good to understand what is going on behind the scene and it is very well explained here.

REPLY
LEAVE A REPLY
Your email address will not be published. Required fields are marked *

Comment 

Name * 

Email * 

Website 

 Notify me of follow-up comments by email.

 Notify me of new posts by email.

PROUDLY POWERED BY WORDPRESS | THEME: TONAL BY WORDPRESS.COM.
'''