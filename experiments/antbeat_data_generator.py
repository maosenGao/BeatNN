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
epoch_size = 76
nchans = 64
nlabels = 4


# preparing the general montage
montage = antbeat_utils.data_utils.get_eeg_montage(data_dir)

all_subj_epochs = np.empty([0,nchans,epoch_size])
all_subj_labels = np.empty([0,nlabels])

for isubj_count, (subj, isubj) in enumerate(subj_names_ids.items()):
	for irec in range(8):
		print('Loading data for subject ', subj, ' in recording ',irec)
		raw = antbeat_utils.data_utils.load_raw(data_dir,subj,isubj,irec+1,montage)
		all_trigger_events = antbeat_utils.data_utils.load_trigger_events(data_dir,subj,isubj,irec+1,phase_trial_type_trigger_dict)
		epochs = antbeat_utils.data_utils.epoch_raw_with_ssp(all_trigger_events,phase_trial_type_trigger_dict, raw,subj,irec, tmin=-0.1, tmax=0.5)
		labels = antbeat_utils.data_utils.generate_epoch_label_matrix(all_trigger_events,phase_trigger_dict,trial_type_trigger_dict,isubj_count)
		curr_epochs = epochs.get_data()[:,:64,::4] # downsample and keep only eeg channels
		all_subj_epochs = np.concatenate(
			(all_subj_epochs,curr_epochs),axis=0)
		all_subj_labels = np.concatenate(
			(all_subj_labels,labels),axis=0)

x_tr,y_tr,x_ts,y_ts = antbeat_utils.data_utils.split_data_for_cross_validation(all_subj_epochs, all_subj_labels)

np.save('tr_data/x_tr',x_tr)
np.save('tr_data/y_tr',y_tr)
np.save('ts_data/x_ts',x_ts)
np.save('ts_data/y_ts',y_ts)

		