import numpy as np
import matplotlib.pyplot as plt
import mne
import utils.data_utils 

data_dir = '../datasets/OpenMIIR/data/'

all_conds = utils.data_utils.get_all_conds()
print(all_conds)
conds_of_interest = all_conds[:2]
cond_trig_dict = utils.data_utils.stim_triggs_for_conds_of_interest(conds_of_interest)

subj_ids = utils.data_utils.get_all_subject_ids()

for i in range(len(subj_ids)):
	
	subj_id = subj_ids[i]
	raw = utils.data_utils.load_raw(data_dir,subj_id)
	
	data, stim_triggs, time = utils.data_utils.get_data_stim_and_time_from_raw(raw)

	trig_is = utils.data_utils.find_stim_trig_time_indices(stim_triggs, cond_trig_dict)
	print(trig_is.shape)


'''
fs = 512
nsecs = 1
epoch_size = fs*nsecs
nchans = 68

X = np.empty([0,nchans,epoch_size]) # dataset
Y = np.empty([0,1]) #labels
for t in range(epoch_size):
	print('current t: ', t)
	idx = np.linspace((trig_is-t),(trig_is-t)+epoch_size,num=epoch_size,dtype=int).T
	X = np.append(
		X,
		np.transpose(data[:,idx],(1,0,2)),
		axis=0)
	Y = np.append(
		Y,
		np.ones((120,1),dtype=int)*t,
		axis=0)

base_secs = 0.1 # baseline period
base_samp = np.floor(0.1*fs).astype(int)
X = X - np.mean(X[:,:,:base_samp],axis=2,keepdims=True)

# separate into traning, validation, and test sets
perc_tr = np.floor(0.85*X.shape[0]).astype(int) 
perc_vl = np.floor(0.1*X.shape[0]).astype(int)

rand_is = np.random.choice(X.shape[0],X.shape[0],replace=False)
X = X[rand_is] # shuffle data
Y = Y[rand_is] # shuffle data

x_tr = X[:perc_tr]
y_tr = Y[:perc_tr]
x_vl = X[perc_tr:(perc_tr+perc_vl)]
y_vl = Y[perc_tr:(perc_tr+perc_vl)]
x_ts = X[(perc_tr+perc_vl):]
y_ts = Y[(perc_tr+perc_vl):]

np.save('tr_data/x_tr',x_tr)
np.save('tr_data/y_tr',y_tr)
np.save('tr_data/x_vl',x_vl)
np.save('tr_data/y_vl',y_vl)
np.save('ts_data/x_ts',x_ts)
np.save('ts_data/y_ts',y_ts)
'''
