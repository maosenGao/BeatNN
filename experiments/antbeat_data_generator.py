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

# preparing the general montage
montage = antbeat_utils.data_utils.get_eeg_montage(data_dir)

for subj, isubj in subj_names_ids.items():
	for irec in range(8):
		raw = antbeat_utils.data_utils.load_raw(data_dir,subj,isubj,irec+1,montage)
		all_trigger_events = antbeat_utils.data_utils.load_trigger_events(data_dir,subj,isubj,irec+1)
		unique_trigger_events_in_raw = np.unique(all_trigger_events[:,2])
		phase_trial_type_trigger_dict_in_raw = {key:val for key, val in phase_trial_type_trigger_dict.items() if val in unique_trigger_events_in_raw}
		raw = antbeat_utils.data_utils.apply_ssp(raw)
		event_id, tmin, tmax = phase_trial_type_trigger_dict_in_raw, -0.1, 0.5
		epoch_params = dict(events = all_trigger_events, event_id = event_id, tmin=tmin, tmax=tmax, preload=True)
		epochs = mne.Epochs(raw, **epoch_params)
