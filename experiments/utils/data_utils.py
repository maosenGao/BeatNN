import librosa
import glob
import numpy as np
import mne

def get_all_subject_ids():
	subj_ids = ('P01', 'P05', 'P07', 'P11', 'P13', 'P04', 'P06', 'P09', 'P12', 'P14')
	return subj_ids

def get_all_conds():
	all_conds = ('C1', 'C2', 'C3', 'C4')
	return all_conds

def load_raw(data_dir,subj_id):		
	raw = mne.io.read_raw_fif(data_dir+subj_id+'-raw.fif', preload=True)
	return raw

def get_data_stim_and_time_from_raw(raw,tot_rec_chs=71):
	data = raw.get_data()[:-1,:]
	stim = raw.get_data()[-1,:]
	time = raw.times

	if len(raw.ch_names) < tot_rec_chs:
		blank_chs = np.zeros((2,data.shape[1]))
		data = np.concatenate((data,blank_chs))

	return data, stim, time

def get_stim_audio_onset_dict(stim_triggs, cond_trig_dict, audio_onset_trigg = 1000):

	all_unique_triggs = np.unique(stim_triggs)[1:]
	all_audio_onsets = np.where(stim_triggs==audio_onset_trigg)[0]
	stim_trigg_onsets_dict = {itrig : np.where(stim_triggs==itrig)[0] for icond, triggs in cond_trig_dict.items() for itrig in triggs}
	stim_audio_onsets_dict = {itrig : all_audio_onsets[np.abs(np.repeat(all_audio_onsets[...,np.newaxis],len(onsets),axis=1) - onsets).argmin(axis=0)] for itrig, onsets in stim_trigg_onsets_dict.items()}
	return stim_audio_onsets_dict

def get_all_stim_ids():
	
	all_stim_ids = (
		1, 2, 3, 4,
		11,12,13,14,
		21,22,23,24
		)

	return all_stim_ids

def get_all_triggers(tot_conds = 4):

	all_stim_ids = get_all_stim_ids()
	all_conds = get_all_conds()
	all_triggers = dict()
	for i in range(tot_conds):
		all_triggers[all_conds[i]] = tuple([istim_id*10+i+1 for istim_id in all_stim_ids])
	
	return all_triggers

def stim_triggs_for_conds_of_interest(conds_of_interest):
	all_triggers = get_all_triggers()
	triggers = {icond:all_triggers[icond] for icond in conds_of_interest}

	return triggers
		 
def find_stim_trig_time_indices(stim_triggs,cond_trig_dict):
	
	trig_is = np.empty([0,1], dtype=int)
	triggs = np.empty([0,1], dtype=int)
	for cond, trigs in cond_trig_dict.items():
		for itrig in trigs:
			curr_trig_is = np.where(stim_triggs==itrig)[0]
			trig_is = np.append(trig_is, curr_trig_is)		
			triggs = np.append(triggs, np.ones(curr_trig_is.shape)*itrig)		
	return trig_is, triggs

def get_stim_beat_samps_dict(stm_file_list, cue_file_list, fs=44100, stm_dir = '/Users/iranrroman/Research/BeatNN/datasets/OpenMIIR/openmiir/audio/full.v2/'):
	
	all_stim_ids = [int(file[len(stm_dir)+1:len(stm_dir)+3]) for file in stm_file_list]
	
	stim_beat_samps_dict = dict()
	for istim, stim_id in enumerate(all_stim_ids):
		
		curr_stm_file = stm_file_list[istim] 
		curr_cue_file = cue_file_list[istim]

		curr_stm, fs = librosa.load(curr_stm_file, fs)
		curr_cue, fs = librosa.load(curr_cue_file, fs)

		tempo_c, cue_beat_samps = librosa.beat.beat_track(curr_cue, fs, units='samples')
		tempo_s, stm_beat_samps = librosa.beat.beat_track(curr_stm[len(curr_cue):], fs, units = 'samples')

		all_beats = np.concatenate((cue_beat_samps,
			stm_beat_samps + len(curr_cue)))

		stim_beat_samps_dict[stim_id] = all_beats	

	return stim_beat_samps_dict
	
def get_epochs(data, trig_is, epoch_size, nchans=70):
	idx = np.linspace((trig_is-(epoch_size/2)),(trig_is+(epoch_size/2)),num=epoch_size,dtype=int).T
	epoched_data =np.transpose( data[:,idx],(1,0,2))
	return epoched_data

def generate_labels_trig_id_and_isubj_matrix(epoched_data, target, subj_id, triggs):
	ndata_points = epoched_data.shape[0]
	labels_matrix = np.concatenate((
		np.ones((ndata_points,1))*target,
		np.ones((ndata_points,1))*int(subj_id[-2:]),
		triggs[:,np.newaxis]),
		axis=1)
	return labels_matrix

def get_stim_cue_file_lists(subj_id):

	subj_id = int(subj_id[1:])

	stm_dir = '/Users/iranrroman/Research/BeatNN/datasets/OpenMIIR/openmiir/audio/full.v2/'
	stm_dir_v1 = '/Users/iranrroman/Research/BeatNN/datasets/OpenMIIR/openmiir/audio/full.v1/'
	cue_dir = '/Users/iranrroman/Research/BeatNN/datasets/OpenMIIR/openmiir/audio/cues.v2/'
	cue_dir_v1 = '/Users/iranrroman/Research/BeatNN/datasets/OpenMIIR/openmiir/audio/cues.v1/'

	stm_file_list = [
		stm_dir+'S01_Chim Chim Cheree_lyrics.wav',
		stm_dir+'S02_Take Me Out To The Ballgame_lyrics.wav',
		stm_dir+'S03_Jingle Bells_lyrics.wav',
		stm_dir+'S04_Mary Had A Little Lamb_lyrics.wav',
		stm_dir+'S11_Chim Chim Cheree_no_lyrics.wav',
		stm_dir+'S12_Take Me Out To The Ballgame_no_lyrics.wav',
		stm_dir+'S13_Jingle Bells_no_lyrics.wav',
		stm_dir+'S14_Mary Had A Little Lamb_no_lyrics.wav',
		stm_dir+'S21_EmperorWaltz.wav',
		stm_dir+'S22_Harry Potter Theme.wav',
		stm_dir+'S23_Star Wars Theme.wav',
		stm_dir+'S24_Eine kleine Nachtmusic.wav'
		]	

	cue_file_list = [
		cue_dir+'S01_Chim Chim Cheree_lyrics_cue.wav',
		cue_dir+'S02_Take Me Out To The Ballgame_lyrics_cue.wav',
		cue_dir+'S03_Jingle Bells_lyrics_cue.wav',
		cue_dir+'S04_Mary Had A Little Lamb_lyrics_cue.wav',
		cue_dir+'S11_Chim Chim Cheree_no_lyrics_cue.wav',
		cue_dir+'S12_Take Me Out To The Ballgame_no_lyrics_cue.wav',
		cue_dir+'S13_Jingle Bells_no_lyrics_cue.wav',
		cue_dir+'S14_Mary Had A Little Lamb_no_lyrics_cue.wav',
		cue_dir+'S21_EmperorWaltz_cue.wav',
		cue_dir+'S22_Harry Potter Theme_cue.wav',
		cue_dir+'S23_Star Wars Theme_cue.wav',
		cue_dir+'S24_Eine kleine Nachtmusic_cue.wav'
		]	

	if subj_id < 9:
		stm_file_list = [
			stm_dir_v1+'S01_Chim Chim Cheree_lyrics.wav',
			stm_dir_v1+'S02_Take Me Out To The Ballgame_lyrics.wav',
			stm_dir+'S03_Jingle Bells_lyrics.wav',
			stm_dir+'S04_Mary Had A Little Lamb_lyrics.wav',
			stm_dir_v1+'S11_Chim Chim Cheree_no_lyrics.wav',
			stm_dir_v1+'S12_Take Me Out To The Ballgame_no_lyrics.wav',
			stm_dir+'S13_Jingle Bells_no_lyrics.wav',
			stm_dir+'S14_Mary Had A Little Lamb_no_lyrics.wav',
			stm_dir+'S21_EmperorWaltz.wav',
			stm_dir_v1+'S22_Harry Potter Theme.wav',
			stm_dir+'S23_Star Wars Theme.wav',
			stm_dir+'S24_Eine kleine Nachtmusic.wav'
			]	

		cue_file_list = [
			cue_dir_v1+'S01_Chim Chim Cheree_lyrics_cue.wav',
			cue_dir_v1+'S02_Take Me Out To The Ballgame_lyrics_cue.wav',
			cue_dir+'S03_Jingle Bells_lyrics_cue.wav',
			cue_dir+'S04_Mary Had A Little Lamb_lyrics_cue.wav',
			cue_dir_v1+'S11_Chim Chim Cheree_no_lyrics_cue.wav',
			cue_dir_v1+'S12_Take Me Out To The Ballgame_no_lyrics_cue.wav',
			cue_dir+'S13_Jingle Bells_no_lyrics_cue.wav',
			cue_dir+'S14_Mary Had A Little Lamb_no_lyrics_cue.wav',
			cue_dir+'S21_EmperorWaltz_cue.wav',
			cue_dir_v1+'S22_Harry Potter Theme_cue.wav',
			cue_dir+'S23_Star Wars Theme_cue.wav',
			cue_dir+'S24_Eine kleine Nachtmusic_cue.wav'
			]	

	return stm_file_list, cue_file_list
