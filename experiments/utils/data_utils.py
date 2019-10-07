import numpy as np
import mne

def get_all_subject_ids():
	subj_ids = ('P01', 'P05', 'P07', 'P11', 'P13', 'P04', 'P06', 'P09', 'P12', 'P14')
	return subj_ids

def get_all_conds():
	all_conds = ('C1', 'C2', 'C3', 'C4')
	return all_conds

def load_raw(data_dir,subj_id):		
	raw = mne.io.read_raw_fif(data_dir+subj_id+'-raw.fif', preload=True)
	return raw

def get_data_stim_and_time_from_raw(raw,tot_rec_chs=71):
	data = raw.get_data()[:-1,:]
	stim = raw.get_data()[-1,:]
	time = raw.times

	if len(raw.ch_names) < tot_rec_chs:
		blank_chs = np.zeros((2,data.shape[1]))
		data = np.concatenate((data,blank_chs))

	return data, stim, time

def get_all_stim_ids():
	
	all_stim_ids = (
		1, 2, 3, 4,
		11,12,13,14,
		21,22,23,24
		)

	return all_stim_ids

def get_all_triggers(tot_conds = 4):

	all_stim_ids = get_all_stim_ids()
	all_conds = get_all_conds()
	all_triggers = dict()
	for i in range(tot_conds):
		all_triggers[all_conds[i]] = tuple([istim_id*10+i+1 for istim_id in all_stim_ids])
	
	return all_triggers

def stim_triggs_for_conds_of_interest(conds_of_interest):
	all_triggers = get_all_triggers()
	triggers = {icond:all_triggers[icond] for icond in conds_of_interest}

	return triggers
		 
def find_stim_trig_time_indices(stim_triggs,cond_trig_dict):
	
	trig_is = np.empty([0,1], dtype=int)
	triggs = np.empty([0,1], dtype=int)
	for cond, trigs in cond_trig_dict.items():
		for itrig in trigs:
			curr_trig_is = np.where(stim_triggs==itrig)[0]
			print(curr_trig_is)
			trig_is = np.append(trig_is, curr_trig_is)		
			triggs = np.append(triggs, np.ones(curr_trig_is.shape)*itrig)		
	return trig_is, triggs
	
def get_epochs(data, trig_is, epoch_size, nchans=70):
	idx = np.linspace((trig_is-(epoch_size/2)),(trig_is+(epoch_size/2)),num=epoch_size,dtype=int).T
	epoched_data =np.transpose( data[:,idx],(1,0,2))
	return epoched_data

def generate_labels_trig_id_and_isubj_matrix(epoched_data, target, subj_id, triggs):
	ndata_points = epoched_data.shape[0]
	labels_matrix = np.concatenate((
		np.ones((ndata_points,1))*target,
		np.ones((ndata_points,1))*int(subj_id[-2:]),
		triggs[:,np.newaxis]),
		axis=1)
	return labels_matrix
