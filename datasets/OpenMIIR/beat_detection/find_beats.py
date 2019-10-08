import librosa
import glob
import numpy as np

fs = 44100
wav_full_directory = "../openmiir/audio/full.v2/"
wav_cues_directory = "../openmiir/audio/cues.v2/"
wav_full_filenames = glob.glob(wav_full_directory+"*.wav")
wav_cues_filenames = glob.glob(wav_cues_directory+"*.wav")


for wav_file in wav_full_filenames:
	
	cue_file = wav_file[:18]+"cues"+wav_file[22:-4]+"_cue."+wav_file[-3:]

	curr_stm, fs = librosa.load(wav_file,fs)
	curr_cue, fs = librosa.load(cue_file,fs)

	tempo_c, cue_beat_samps = librosa.beat.beat_track(curr_cue, fs, units='samples')
	tempo_s, stm_beat_samps = librosa.beat.beat_track(curr_stm[len(curr_cue):], fs, units='samples')

	all_beats = np.concatenate((cue_beat_samps,
			stm_beat_samps + len(curr_cue)))
	
	return all_beats
	
