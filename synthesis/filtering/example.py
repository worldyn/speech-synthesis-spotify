from utilsfilter import *
from segment import Segment

def main():
    #testpath = './testdata/with-noise.wav'
    testpath = './testdata/7quCH1LZWMKX9xg2tJBMsP.wav'
    fs = 44100
    '''
    fs_wav, data_wav = get_wav(testpath)
    data_wav_norm = data_wav / (2**15) # normalize to -1,1
    data_intervals = segment_interval(
        data_wav_norm, fs, 2.5
    )
    data_silence = remove_silent_segments(data_intervals) #* 2**15
    #write_wav("./testdata/tyst.wav",data_silence,fs)
    '''
    
    ##
    test_text = "The media and of story is a business. now when it comes to business everybody has a reason a very personal one for why they're in that particular business and everyone has their own personal best interests to consider."
    seg = Segment(testpath, 30, 37, fs, test_text)
    #print("Amplitude")
    seg.draw_data()
    seg.write("test.wav")
    #plt.show()
    #sr = seg.get_speech_rate()
    #print("SPEECH RATE:" , sr)
main()

