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

x_tr = np.empty([0,nchans,4,epoch_size])
y_tr = np.empty([0,nlabels])
x_ts = np.empty([0,nchans,4,epoch_size])
y_ts = np.empty([0,nlabels])

for isubj_count, (subj, isubj) in enumerate(subj_names_ids.items()):
	for irec in range(8):
		print('Loading data for subject ', subj, ' in recording ',irec)
		raw = antbeat_utils.data_utils.load_raw(data_dir,subj,isubj,irec+1,montage)
		all_trigger_events = antbeat_utils.data_utils.load_trigger_events(data_dir,subj,isubj,irec+1,phase_trial_type_trigger_dict)
		epochs = antbeat_utils.data_utils.epoch_raw_with_ssp(all_trigger_events,phase_trial_type_trigger_dict, raw,subj,irec, tmin=-0.1, tmax=0.5)
		labels = antbeat_utils.data_utils.generate_epoch_label_matrix(all_trigger_events,phase_trigger_dict,trial_type_trigger_dict,isubj_count)
		epochs = epochs.resample(125)
		epochs = mne.time_frequency.tfr_array_morlet(epochs,125,[3,5,10,20],n_cycles=[1,1,3,5],zero_mean=True,output='power')
		curr_epochs = epochs[:,:64,:,:] # keep only eeg channels
		x_tr = np.concatenate(
			(x_tr,curr_epochs[:-60]),axis=0)
		y_tr = np.concatenate(
			(y_tr,labels[:-60]),axis=0)
		x_ts = np.concatenate(
			(x_ts,curr_epochs[-60:]),axis=0)
		y_ts = np.concatenate(
			(y_ts,labels[-60:]),axis=0)

np.save('tr_data/x_tr_w',x_tr)
np.save('tr_data/y_tr_w',y_tr)
np.save('ts_data/x_ts_w',x_ts)
np.save('ts_data/y_ts_w',y_ts)
