import numpy as np
import matplotlib.pyplot as plt
import mne
import utils.data_utils 

data_dir = '../datasets/OpenMIIR/data/'

# load data
all_conds = utils.data_utils.get_all_conds()
conds_of_interest = all_conds[:2]
cond_trig_dict = utils.data_utils.stim_triggs_for_conds_of_interest(conds_of_interest)
nchans = 70
subj_ids = utils.data_utils.get_all_subject_ids()

# sampling & epoch metadata
fs = 512
nsecs = 0.3
epoch_size = int(fs*nsecs)
nlabels = 3

X = np.empty([0,epoch_size,nchans])
Y = np.empty([0,nlabels])
# iterate over subjects
for i in range(len(subj_ids)):
	
	subj_id = subj_ids[i]

	stm_file_list, cue_file_list = utils.data_utils.get_stim_cue_file_lists(subj_id)

	raw = utils.data_utils.load_raw(data_dir,subj_id)

	data, stim_triggs, time = utils.data_utils.get_data_stim_and_time_from_raw(raw)

	stim_audio_onsets_dict = utils.data_utils.get_stim_audio_onset_dict(stim_triggs, cond_trig_dict)

	stim_beat_samps_dict = utils.data_utils.get_stim_beat_samps_dict(stm_file_list, cue_file_list)	

	stim_beat_indices_dict = utils.data_utils.get_stim_beat_indices_dict(stim_audio_onsets_dict, stim_beat_samps_dict)
	isubj_X, isubj_Y = utils.data_utils.get_epochs_and_labels(epoch_size, data, stim_beat_indices_dict, subj_id)

	X = np.concatenate(
		(X,
		isubj_X),
		axis = 0
		)
	
	Y = np.concatenate(
		(Y,
		isubj_Y),
		axis = 0
		)

#np.save('tr_data/X',X)
#np.save('tr_data/Y',Y)

'''
base_secs = 0.1 # baseline period
base_samp = np.floor(0.1*fs).astype(int)
X = X - np.mean(X[:,:,:base_samp],axis=2,keepdims=True)

# separate into traning, validation, and test sets
perc_tr = np.floor(0.85*X.shape[0]).astype(int) 
perc_vl = np.floor(0.1*X.shape[0]).astype(int)

rand_is = np.random.choice(X.shape[0],X.shape[0],replace=False)
X = X[rand_is] # shuffle data
Y = Y[rand_is] # shuffle data

x_tr = X[:perc_tr]
y_tr = Y[:perc_tr]
x_vl = X[perc_tr:(perc_tr+perc_vl)]
y_vl = Y[perc_tr:(perc_tr+perc_vl)]
x_ts = X[(perc_tr+perc_vl):]
y_ts = Y[(perc_tr+perc_vl):]

np.save('tr_data/x_tr',x_tr)
np.save('tr_data/y_tr',y_tr)
np.save('tr_data/x_vl',x_vl)
np.save('tr_data/y_vl',y_vl)
np.save('ts_data/x_ts',x_ts)
np.save('ts_data/y_ts',y_ts)
'''
