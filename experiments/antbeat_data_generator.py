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

for isubj_count, (subj, isubj) in enumerate(subj_names_ids.items()):
	for irec in range(8):
		raw = antbeat_utils.data_utils.load_raw(data_dir,subj,isubj,irec+1,montage)
		all_trigger_events = antbeat_utils.data_utils.load_trigger_events(data_dir,subj,isubj,irec+1)
		epochs = antbeat_utils.data_utils.epoch_raw_with_ssp(all_trigger_events,phase_trial_type_trigger_dict, raw, tmin=-0.1, tmax=0.5)
		labels = antbeat_utils.data_utils.generate_epoch_label_matrix(all_trigger_events,phase_trigger_dict,trial_type_trigger_dict,isubj_count)
