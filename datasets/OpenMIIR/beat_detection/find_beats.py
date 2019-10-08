import librosa
import glob

fs = 44100
wav_directory = "../openmiir/audio/full.v2/"
wav_filenames = glob.glob(wav_directory+"*.wav")

for iwav in wav_filenames:
	
	curr_wav, fs = librosa.load(iwav,fs)
	tempo, beat_times = librosa.beat.beat_track(curr_wav, fs, units='time')
	print(iwav, tempo, beat_times)
	input()
