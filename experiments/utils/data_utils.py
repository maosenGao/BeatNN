import numpy as np

def get_all_subject_ids():
	subj_ids = ('P01', 'P05', 'P07', 'P11', 'P13', 'P04', 'P06', 'P09', 'P12', 'P14')
	return subj_ids

def load_raw(data_dir,subj_ids):		
	raw_list = [mne.io.read_raw_fif(data_dir+isubj+'-raw.fif', preload=True) for isubj in subj_ids]
	return raw_list

def get_data_stim_and_time_from_raw(raw):
	data = raw.get_data()[:-1,:]
	stim = raw.get_data()[-1,:]
	time = raw.times
	return data, stim, time
	
	 

