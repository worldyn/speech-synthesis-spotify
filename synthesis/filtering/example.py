from utilsfilter import *
from segment import Segment

def main():
    testpath = './smaller7tmono.wav'
    #testpath = './testdata/7quCH1LZWMKX9xg2tJBMsP.wav'
    fs_wav, data_wav = get_wav(testpath)
    print("fs wav: ", fs_wav)
    #samp_freq = 
    fs = 44100.0
    # start end time not used on wav file
    test_text = "The media and of story is a business. now when it comes to business everybody has a reason a very personal one for why they're in that particular business and everyone has their own personal best interests to consider."
    seg = Segment(testpath, 0, 20, fs, test_text)
    #print("Amplitude")
    #seg.draw_data()
    #seg.write("test.wav")
    #plt.show()
    sr = seg.get_speech_rate()
    print("SPEECH RATE:" , sr)
main()

