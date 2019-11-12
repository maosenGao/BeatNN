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
epoch_size_s = 460 
epoch_size_m = 685 
epoch_size_l = 910 
nchans = 64

# preparing the general montage
montage = antbeat_utils.data_utils.get_eeg_montage(data_dir)

x_tr_s = np.empty([0,nchans,epoch_size_s])
x_tr_m = np.empty([0,nchans,epoch_size_m])
x_tr_l = np.empty([0,nchans,epoch_size_l])
x_ts_s = np.empty([0,nchans,epoch_size_s])
x_ts_m = np.empty([0,nchans,epoch_size_m])
x_ts_l = np.empty([0,nchans,epoch_size_l])

for isubj_count, (subj, isubj) in enumerate(subj_names_ids.items()):
	for irec in range(8):
		print('Loading data for subject ', subj, ' in recording ',irec)
		raw = antbeat_utils.data_utils.load_raw(data_dir,subj,isubj,irec+1,montage)
		all_trigger_events = antbeat_utils.data_utils.load_trigger_events(data_dir,subj,isubj,irec+1,phase_trial_type_trigger_dict)
		raw = antbeat_utils.data_utils.apply_ssp(raw,subj,irec)
		epochs_short = antbeat_utils.data_utils.epoch_raw(all_trigger_events,phase_trial_type_trigger_dict, raw,subj,irec, tmin=-0.08, tmax=3.6, event_id= {'ASI0':115,'DSI0':215,'SSI0':59 ,})
		epochs_medium = antbeat_utils.data_utils.epoch_raw(all_trigger_events,phase_trial_type_trigger_dict, raw,subj,irec, tmin=-0.08, tmax=5.4, event_id= {'AMI0':125,'DMI0':225,'SMI0':69 ,})
		epochs_long = antbeat_utils.data_utils.epoch_raw(all_trigger_events,phase_trial_type_trigger_dict, raw,subj,irec, tmin=-0.08, tmax=7.2, event_id= {'ALI0':135,'DLI0':235,'SLIO':79})
		epochs_short = epochs_short.resample(125)
		epochs_medium = epochs_medium.resample(125)
		epochs_long = epochs_long.resample(125)
		curr_epochs_short = epochs_short.get_data()[:,:64,:] # keep only eeg channels
		curr_epochs_medium = epochs_medium.get_data()[:,:64,:]
		curr_epochs_long = epochs_long.get_data()[:,:64,:]
		x_tr_s = np.concatenate(
			(x_tr_s,curr_epochs_short[:-2]),axis=0)
		x_tr_m = np.concatenate(
			(x_tr_m,curr_epochs_medium[:-2]),axis=0)
		x_tr_l = np.concatenate(
			(x_tr_l,curr_epochs_long[:-2]),axis=0)
		x_ts_s = np.concatenate(
			(x_ts_s,curr_epochs_short[-2:]),axis=0)
		x_ts_m = np.concatenate(
			(x_ts_m,curr_epochs_medium[-2:]),axis=0)
		x_ts_l = np.concatenate(
			(x_ts_l,curr_epochs_long[-2:]),axis=0)

np.save('tr_data/x_tr_s',x_tr_s)
np.save('tr_data/x_tr_m',x_tr_m)
np.save('tr_data/x_tr_l',x_tr_l)
np.save('ts_data/x_ts_s',x_ts_s)
np.save('ts_data/x_ts_m',x_ts_m)
np.save('ts_data/x_ts_l',x_ts_l)
