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
nsecs = 2
epoch_size = fs*nsecs

# iterate over subjects
for i in range(len(subj_ids)):
	
	subj_id = subj_ids[i]
	raw = utils.data_utils.load_raw(data_dir,subj_id)
	
	data, stim_triggs, time = utils.data_utils.get_data_stim_and_time_from_raw(raw)

	trig_is, triggs = utils.data_utils.find_stim_trig_time_indices(stim_triggs, cond_trig_dict)

	epoched_data = utils.data_utils.get_epochs(data, trig_is, epoch_size)

	labels_matrix = utils.data_utils.generate_labels_trig_id_and_isubj_matrix(epoched_data, epoch_size/2, subj_ids[i], triggs)

	X = np.concatenate(
		(X,
		epoched_data),
		axis = 0
		)
	
	Y = np.concatenate(
		(Y,
		labels_and_isubj),
		axis = 0
		)

np.save('tr_data/X',X)
np.save('tr_data/Y',Y)

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
