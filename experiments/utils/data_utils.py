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

def get_cond_stim_trig_dict(conds_of_interest):
	all_triggers = get_all_triggers()
	triggers = {icond:all_triggers[icond] for icond in conds_of_interest}

	return triggers
		 
def load_raw(data_dir,subj_id):		
	raw = mne.io.read_raw_fif(data_dir+subj_id+'-raw.fif', preload=True)
	return raw

def get_data_trig_and_time_sequences_from_raw(raw,tot_rec_chs=71):
	data = raw.get_data()[:-1,:]
	triggs_sequence = raw.get_data()[-1,:]
	time = raw.times

	if len(raw.ch_names) < tot_rec_chs:
		blank_chs = np.zeros((2,data.shape[1]))
		data = np.concatenate((data,blank_chs))

	return data, triggs_sequence, time

def get_trig_audio_eegonsets_dict(triggs_sequence, cond_trig_dict, audio_onset_trigg = 1000):

	all_audio_onsets = np.where(triggs_sequence==audio_onset_trigg)[0]
	triggs_eegonsets_dict = {itrig : np.where(triggs_sequence==itrig)[0] for icond, triggs in cond_trig_dict.items() for itrig in triggs}
	triggs_audio_eegonsets_dict = {itrig : all_audio_onsets[np.abs(np.repeat(all_audio_onsets[...,np.newaxis],len(onsets),axis=1) - onsets).argmin(axis=0)] for itrig, onsets in triggs_eegonsets_dict.items()}
	return triggs_audio_eegonsets_dict

def get_stim_id_beat_audiosamples_dict(stm_file_list, cue_file_list, fs=44100, stm_dir = '/Users/iranrroman/Research/BeatNN/datasets/OpenMIIR/openmiir/audio/full.v2/'):
	
	all_stim_ids = [int(file[len(stm_dir)+1:len(stm_dir)+3]) for file in stm_file_list]
	
	stim_id_beat_audiosamps_dict = dict()
	for istim, stim_id in enumerate(all_stim_ids):
		
		curr_stm_file = stm_file_list[istim] 
		curr_cue_file = cue_file_list[istim]

		curr_stm, fs = librosa.load(curr_stm_file, fs)
		curr_cue, fs = librosa.load(curr_cue_file, fs)

		tempo_c, cue_beat_samps = librosa.beat.beat_track(curr_cue, fs, units='samples')
		tempo_s, stm_beat_samps = librosa.beat.beat_track(curr_stm[len(curr_cue):], fs, units = 'samples')

		all_beats = np.concatenate((cue_beat_samps,
			stm_beat_samps + len(curr_cue)))

		stim_id_beat_audiosamps_dict[stim_id] = all_beats	

	return stim_id_beat_audiosamps_dict

def get_trig_beat_eegsamples_dict(trig_audio_onsets_dict, stim_id_beat_audiosamps_dict, audio_fs=44100, eeg_fs=512):
	
	trig_beat_eegsamps_dict = dict()

	for trig, onsets in trig_audio_onsets_dict.items():
		beat_audiosamps = stim_id_beat_audiosamps_dict[trig//10]
		beat_eegsamps = eeg_fs*beat_audiosamps//audio_fs
		trig_beat_eegsamps_dict[trig] = np.repeat(onsets[...,np.newaxis],len(beat_eegsamps),axis=1) + beat_eegsamps 
	return trig_beat_eegsamps_dict	

def get_stim_meter_dict():
	# meters are either binary or ternary
	stim_meter_dict = {
			1:3,
			2:3,
			3:2,
			4:2,
			11:3,
			12:3,
			13:2,
			14:2,
			21:3,
			22:3,
			23:2,
			24:2
			}	
	return stim_meter_dict

def get_epochs_and_labels(epoch_size, data, trig_beat_eegsamps_dict, subj_id, nchans = 70, nlabels = 3):

	stim_meter_dict = get_stim_meter_dict()
	isubj_X = np.empty([0, epoch_size, nchans])
	isubj_Y = np.empty([0, nlabels])
	for trig, beat_indices in trig_beat_eegsamps_dict.items():
		for itrial in range(beat_indices.shape[0]):
			beat_is = beat_indices[itrial]
			idx = np.linspace((beat_is-(epoch_size/2)),beat_is+(epoch_size/2),num=epoch_size,dtype=int)
			epoched_data = np.transpose(data[:,idx],(2,1,0))
			labels = np.asarray([trig,stim_meter_dict[trig//10],int(subj_id[1:])])
			isubj_X = np.concatenate(
				(isubj_X,
				epoched_data), 
				axis=0)
			isubj_Y = np.concatenate(
				(isubj_Y,
				np.repeat(labels[np.newaxis,...],epoched_data.shape[0],axis=0)),
				axis=0)
	return isubj_X, isubj_Y

def split_data_for_cross_validation(X,Y,perc_test=0.05,perc_val=0.1):

	rand_is = np.random.choice(X.shape[0],X.shape[0],replace=False)
	rand_tr_is = rand_is[:int((1-perc_test-perc_val)*X.shape[0])]
	rand_vl_is = rand_is[int((1-perc_test-perc_val)*X.shape[0]):int((1-perc_test)*X.shape[0])]
	rand_ts_is = rand_is[int((1-perc_test)*X.shape[0]):]

	x_tr = X[rand_tr_is]
	y_tr = Y[rand_tr_is]
	x_vl = X[rand_vl_is]
	y_vl = Y[rand_vl_is]
	x_ts = X[rand_ts_is]
	y_ts = Y[rand_ts_is]

	return x_tr,y_tr,x_vl,y_vl,x_ts,y_ts

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
		stm_dir+'S11_Chim Chim Cheree_no lyrics.wav',
		stm_dir+'S12_Take Me Out To The Ballgame_no lyrics.wav',
		stm_dir+'S13_Jingle Bells_no lyrics.wav',
		stm_dir+'S14_Mary Had A Little Lamb_no lyrics.wav',
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
		cue_dir+'S11_Chim Chim Cheree_no lyrics_cue.wav',
		cue_dir+'S12_Take Me Out To The Ballgame_no lyrics_cue.wav',
		cue_dir+'S13_Jingle Bells_no lyrics_cue.wav',
		cue_dir+'S14_Mary Had A Little Lamb_no lyrics_cue.wav',
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
			stm_dir_v1+'S11_Chim Chim Cheree_no lyrics.wav',
			stm_dir_v1+'S12_Take Me Out To The Ballgame_no lyrics.wav',
			stm_dir+'S13_Jingle Bells_no lyrics.wav',
			stm_dir+'S14_Mary Had A Little Lamb_no lyrics.wav',
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
			cue_dir_v1+'S11_Chim Chim Cheree_no lyrics_cue.wav',
			cue_dir_v1+'S12_Take Me Out To The Ballgame_no lyrics_cue.wav',
			cue_dir+'S13_Jingle Bells_no lyrics_cue.wav',
			cue_dir+'S14_Mary Had A Little Lamb_no lyrics_cue.wav',
			cue_dir+'S21_EmperorWaltz_cue.wav',
			cue_dir_v1+'S22_Harry Potter Theme_cue.wav',
			cue_dir+'S23_Star Wars Theme_cue.wav',
			cue_dir+'S24_Eine kleine Nachtmusic_cue.wav'
			]	

	return stm_file_list, cue_file_list
