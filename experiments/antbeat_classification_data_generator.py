import numpy as np
import matplotlib.pyplot as plt
import mne
import antbeat_utils.data_utils 
import scipy.io as sp

# global variables
data_dir = '../datasets/AntBeatRateChanges/data/'
subj_names_ids = antbeat_utils.data_utils.get_subj_names_ids_dict()
phase_trigger_dict = antbeat_utils.data_utils.get_phases_trig_dict()
trial_type_trigger_dict = antbeat_utils.data_utils.get_trial_type_trig_dict()
phase_trial_type_trigger_dict = antbeat_utils.data_utils.generate_phase_trial_type_trigger_dict()	
epoch_size = 75
nchans = 64
nlabels = 4


# preparing the general montage
montage = antbeat_utils.data_utils.get_eeg_montage(data_dir)

x_tr = np.empty([0,nchans,epoch_size])
y_tr = np.empty([0,nlabels])
x_ts = np.empty([0,nchans,epoch_size])
y_ts = np.empty([0,nlabels])

for isubj_count, (subj, isubj) in enumerate(subj_names_ids.items()):
	for irec in range(8):
		print('Loading data for subject ', subj, ' in recording ',irec)
		raw = antbeat_utils.data_utils.load_raw(data_dir,subj,isubj,irec+1,montage)
		raw.info['bads']=['M1','M2','T7','T8','TP8','TP7','CB1','CB2','FT7','FT8']
		all_trigger_events = antbeat_utils.data_utils.load_trigger_events(data_dir,subj,isubj,irec+1,phase_trial_type_trigger_dict)
		epochs = antbeat_utils.data_utils.epoch_raw_with_ssp(all_trigger_events,phase_trial_type_trigger_dict, raw,subj,irec, tmin=-0.1, tmax=0.5)
		labels = antbeat_utils.data_utils.generate_epoch_label_matrix(epochs.events,phase_trigger_dict,trial_type_trigger_dict,isubj_count)
		epochs = epochs.resample(125)
		curr_epochs = epochs.get_data()[:,:64,:] # keep only eeg channels
		perc_test = int(curr_epochs.shape[0]/10)
		rand_i = np.random.choice(curr_epochs.shape[0]-perc_test,1)[0]
		x_tr = np.concatenate(
			(x_tr,curr_epochs[:rand_i],curr_epochs[rand_i+perc_test:]),axis=0)
		y_tr = np.concatenate(
			(y_tr,labels[:rand_i],labels[rand_i+perc_test:]),axis=0)
		x_ts = np.concatenate(
			(x_ts,curr_epochs[rand_i:rand_i+perc_test]),axis=0)
		y_ts = np.concatenate(
			(y_ts,labels[rand_i:rand_i+perc_test:]),axis=0)
		if curr_epochs.shape[0] < 450:	
			print('WARNING: too many epochs dropped for subj ', subj, ' in recordng ', irec, '. ', curr_epochs.shape[0]-perc_test, ' epochs added for training and ', perc_test, ' added for evaluation. Press ENTER to continue.')
			#input()

np.save('tr_data/x_tr',x_tr)
np.save('tr_data/y_tr',y_tr)
np.save('ts_data/x_ts',x_ts)
np.save('ts_data/y_ts',y_ts)
