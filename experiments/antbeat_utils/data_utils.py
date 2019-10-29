import numpy as np
import scipy.io as sp
import mne

def get_subj_names_ids_dict():
	subj_names_ids_dict = {
		'EGnew':'S01',
		'CPDnew':'S02',
		'TDnew':'S03',
		'CDnew':'S04',
		'SYLnew':'S06',
		'MH':'S07',
		'AC':'S08',
		'EC':'S09',
		'IR':'S11',
		'CB':'S12',
		'WD':'S13',
		'DJ':'S14',
		'JH':'S15',
		'MHert':'S16',
		'BN':'S17',
		'JC':'S18',
		'KK':'S19',
		'YA':'S20',
		'AW':'S21',
		'CT':'S23'}
	return subj_names_ids_dict

def get_all_triggers():

	all_triggers = (
		((117,), (115,), (111,), (110,)),
		((127,), (125,), (122, 121), (120,)),
		((137,), (135,), (133, 132, 131), (130,)),
		((217,), (215,), (211,), (210,)),
		((227,), (225,), (222, 221), (220,)),
		((237,), (235,), (233, 232, 231), (230,)),
		((61,),  (59,),  (55,),  (54,)),
		((71,),  (69,),  (66,  65),  (64,)),
		((81,),  (79,),  (77,  76,  75),  (74,)),
		((119,), (115,), (111,), (11,)),
		((129,), (125,), (122, 121), (12,)),
		((139,), (135,), (133, 132, 131), (13,)),
		((219,), (215,), (211,), (21,)),
		((229,), (225,), (222, 221),  (22,)),
		((239,), (235,), (233, 232, 231),  (23,)),
		((63,),  (59,),  (55,), (31,)),
		((73,),  (69,),  (66, 65), (32,)),
		((83,),  (79,),  (77, 76, 75), (33,))
		)

	return all_triggers

def get_all_phase_names():
	phase_names = ('Visual', 'Initial', 'Anticipation', 'Changing')
	return phase_names

def get_trial_types():
	trial_types = ('Accel short norm',
			'Accel medium norm',
			'Accel long norm',
			'Decel short norm',
                        'Decel medium norm',
                        'Decel long norm',
			'Steady short norm',
                        'Steady medium norm',
                        'Steady long norm',
			'Accel short targ',
			'Accel medium targ',
			'Accel long targ',
			'Decel short targ',
                        'Decel medium targ',
                        'Decel long targ',
			'Steady short targ',
                        'Steady medium targ',
                        'Steady long targ')
	return trial_types

def remove_dict_val_repeats(dict_w_repeats):
	dict_wo_repeats = {key:list(set(val))for key, val in dict_w_repeats.items()}
	return dict_wo_repeats

def get_trial_type_trig_dict():
	all_trial_types = get_trial_types()
	all_triggers = get_all_triggers()
	trial_type_trigger_dict = {trial:[trigger for trig_list in all_triggers[itrial] for trigger in trig_list] for itrial, trial in enumerate(all_trial_types)}
	
	trial_type_trigger_dict = remove_dict_val_repeats(trial_type_trigger_dict)

	return trial_type_trigger_dict

def get_phases_trig_dict():
	all_phases = get_all_phase_names()
	all_triggers = get_all_triggers()
	phase_trigger_dict = {phase:[] for phase in all_phases}
	for itrial in range(len(all_triggers)):
		for iphase,phase in enumerate(all_phases):
			phase_trigger_dict[phase].append(
						all_triggers[itrial][iphase])
	phase_trigger_dict = {key:[item for sublist in val for item in sublist] for key, val in phase_trigger_dict.items()} 

	phase_trigger_dict = remove_dict_val_repeats(phase_trigger_dict)
	
	return phase_trigger_dict

def generate_phase_trial_type_trigger_dict():
	phase_trial_type_trigger_dict = {
		'ASV':117,'ASI':115,'AS1':111,'ASC':110,
		'AMV':127,'AMI':125,'AM2':122,'AM3':121,'AMC':120,	
		'ALV':137,'ALI':135,'AL4':133,'AL5':132,'AL6':131,'ALC':130,
		'DSV':217,'DSI':215,'DS1':211,'DSC':210,
		'DMV':227,'DMI':225,'DM2':222,'DM3':221,'DMC':220,	
		'DLV':237,'DLI':235,'DL4':233,'DL5':232,'DL6':231,'DLC':220,
		'SSV':61 ,'SSI':59 ,'SS1':55 ,'SSC':54 ,
		'SMV':71 ,'SMI':69 ,'SM2':66 ,'SM3':65 ,'SMC':64 ,	
		'SLV':81 ,'SLI':79 ,'SL4':77 ,'SL5':76 ,'SL6':75 ,'SLC':74 ,
		'TASC':11,
		'TAMC':12,
		'TALC':13,		
		'TDSC':21,
                'TDMC':22,
		'TDLC':23,
		'TSSC':31,
                'TSMC':32,
	        'TSLC':33
		}
	return phase_trial_type_trigger_dict		

def get_eeg_montage(data_dir):
	mat_channel_file = sp.loadmat(data_dir+'channel_initial.mat')['Channel']
	positions = np.zeros((len(mat_channel_file[0,:]),3))
	for ichan in range(len(mat_channel_file[0,:])):
		positions[ichan,0] = -mat_channel_file[0,ichan][3].T[0,1]
		positions[ichan,1] = mat_channel_file[0,ichan][3].T[0,0]      
		positions[ichan,2] = mat_channel_file[0,ichan][3].T[0,2]      
	ch_names = []
	for ichan in range(len(mat_channel_file[0,:])):
		ch_names.append(mat_channel_file[0,ichan][0][0])
	montage = mne.channels.Montage(positions,ch_names,'Neuroscan64',range(len(mat_channel_file[0,:])))

	return montage

def load_raw(data_dir,subj,isubj,irec,montage):		
	raw = mne.io.read_raw_cnt(data_dir+subj+'/ANT_'+isubj+'_B0'+str(irec)+'_Data.cnt',montage=montage,preload=True)
	return raw

def load_trigger_events(data_dir,subj,isubj,irec):
	trigger_events = mne.io.curry.curry._read_events_curry(data_dir+subj+'/ANT_'+isubj+'_B0'+str(irec)+'.ceo')
	for itrig, trig in enumerate(trigger_events[:,2]):
		if trig == 119:
			trigger_events[itrig,2] = 117
		if trig == 129:
			trigger_events[itrig,2] = 127
		if trig == 139:
			trigger_events[itrig,2] = 137
		if trig == 219:
			trigger_events[itrig,2] = 217
		if trig == 229:
			trigger_events[itrig,2] = 227
		if trig == 239:
			trigger_events[itrig,2] = 237
		if trig == 63:
			trigger_events[itrig,2] = 61
		if trig == 73:
			trigger_events[itrig,2] = 71
		if trig == 83:
			trigger_events[itrig,2] = 81
	return trigger_events

def apply_ssp(raw):
	raw.set_channel_types(mapping={'HEO':'eog','VEO':'misc','Trigger':'misc'}) # making HEO channel be of 'eog' type to find its projectors                        
	projs_heo, events = mne.preprocessing.compute_proj_eog(raw, n_eeg=1, average=True) # SSP HEO
	raw.set_channel_types(mapping={'HEO':'misc','VEO':'eog','Trigger':'misc'}) # making VEO channel be of 'eog' type to find its projectors                        
	projs_veo, events = mne.preprocessing.compute_proj_eog(raw, n_eeg=1, average=True) # SSP VEO
	raw.add_proj(projs_veo) # adding the projectors
	raw.add_proj(projs_heo) # adding the projectors
	raw.set_channel_types(mapping={'HEO':'misc','VEO':'misc','Trigger':'misc'}) # making non EEG channels be of 'misc' type   
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

def baseline_correction(X, baseline_period = 0.01, fs = 512):

	X = X - np.mean(X[:,:int(fs*baseline_period),:],axis=1,keepdims=True)

	return X

def split_data_for_cross_validation(X,Y,perc_test=0.05):

	rand_is = np.random.choice(X.shape[0],X.shape[0],replace=False)
	rand_tr_is = rand_is[:int((1-perc_test)*X.shape[0])]
	rand_ts_is = rand_is[int((1-perc_test)*X.shape[0]):]

	x_tr = X[rand_tr_is]
	y_tr = Y[rand_tr_is]
	x_ts = X[rand_ts_is]
	y_ts = Y[rand_ts_is]

	return x_tr,y_tr,x_ts,y_ts

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
