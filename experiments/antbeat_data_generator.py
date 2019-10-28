import numpy as np
import matplotlib.pyplot as plt
import mne
import antbeat_utils.data_utils 
import scipy.io as sp

# global variables
data_dir = '../datasets/AntBeatRateChanges/data/'
subj_names_ids = antbeat_utils.data_utils.get_subj_names_ids_dict()

# preparing the general montage
montage = antbeat_utils.data_utils.get_eeg_montage(data_dir)

for subj, isubj in subj_names_ids.items():
	for irec in range(8):
		raw = mne.io.read_raw_cnt(data_dir+subj+'/'+'ANT_'+isubj+'_B0'+str(irec+1)+'_Data.cnt',montage=montage,preload=True)								
		curry_events = mne.io.curry.curry._read_events_curry(data_dir+subj+'/'+'ANT_'+isubj+'_B0'+str(irec+1)+'.ceo')

		print(curry_events[:5])


