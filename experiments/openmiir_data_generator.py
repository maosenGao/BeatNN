import numpy as np
import matplotlib.pyplot as plt
import mne
import utils.data_utils 

# global variables
# data_dir = '../datasets/OpenMIIR/data/'
data_dir = 'E:\\OpenMIIR-RawEEG_v1\\OpenMIIR\\eeg\\mne\\'
subj_ids = utils.data_utils.get_all_subject_ids()
all_conds = utils.data_utils.get_all_conds()
nchans = 70 # eeg channels
fs = 512 # sampling rate
nlabels = 3 # number of labels

# epoching variables 
nsecs = 0.6
epoch_size = int(fs*nsecs) # in samples
 
# define conditions of interest  
conds_of_interest = all_conds[:2]
cond_trig_dict = utils.data_utils.get_cond_stim_trig_dict(conds_of_interest)

# initialize data matrices
all_subj_beat_epochs_C1_C2 = np.empty([0,epoch_size,nchans])
all_subj_beat_labels_C1_C2 = np.empty([0,nlabels])

# iterate over subjects to get all epochs
for i in range(len(subj_ids)):
  
	subj_id = subj_ids[i]
	
	raw = utils.data_utils.load_raw(data_dir,subj_id)

	stm_file_list, cue_file_list = utils.data_utils.get_stim_cue_file_lists(subj_id)

	data, triggs_sequence, time = utils.data_utils.get_data_trig_and_time_sequences_from_raw(raw)

	trig_audio_eegonsets_dict = utils.data_utils.get_trig_audio_eegonsets_dict(triggs_sequence, cond_trig_dict)

	stim_id_beat_audiosamps_dict = utils.data_utils.get_stim_id_beat_audiosamples_dict(stm_file_list, cue_file_list)	

	trig_beat_eegsamps_dict = utils.data_utils.get_trig_beat_eegsamples_dict(trig_audio_eegonsets_dict, stim_id_beat_audiosamps_dict)

	isubj_X, isubj_Y = utils.data_utils.get_epochs_and_labels(epoch_size, data, trig_beat_eegsamps_dict, subj_id)

	isubj_X = utils.data_utils.baseline_correction(isubj_X)

	all_subj_beat_epochs_C1_C2 = np.concatenate(
		(all_subj_beat_epochs_C1_C2,
		isubj_X),
		axis = 0
		)
	
	all_subj_beat_labels_C1_C2 = np.concatenate(
		(all_subj_beat_labels_C1_C2,
		isubj_Y),
		axis = 0
		)

x_tr,y_tr,x_ts,y_ts = utils.data_utils.split_data_for_cross_validation(all_subj_beat_epochs_C1_C2, all_subj_beat_labels_C1_C2)

np.save('tr_data/x_tr',x_tr)
np.save('tr_data/y_tr',y_tr)
np.save('ts_data/x_ts',x_ts)
np.save('ts_data/y_ts',y_ts)
