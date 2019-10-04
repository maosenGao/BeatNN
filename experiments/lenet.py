import numpy as np
import matplotlib.pyplot as plt
import mne
import utils.data_utils 

data_dir = '../datasets/OpenMIIR/data/'
file_name = 'P01-raw.fif'  

subj_ids = utils.data_utils.get_all_subject_ids()

for i in range(len(subj_ids)):
	
	subj_id = subj_ids[i]
	raw = utils.data_utils.load_raw(data_dir,subj_id)
	
	print(raw.ch_names)

	utils.data_utils.get_data_stim_and_time_from_raw(raw)

'''
# load the data
raw = mne.io.read_raw_fif(data_dir+file_name, preload=True)

### get the data array and time array ###
data, stim, time = raw.get_data()[:-1,:], raw.get_data()[-1,:], raw.times

### find stim triggers for all C1 and C2 data ###
triggers = (
	11,  21,  31,  41,
	111, 121, 131, 141,
	211, 221, 231, 241,
	12,  22,  32,  42,
	112, 122, 132, 142,
	212, 222, 232, 242
	) 

trig_is = np.empty([0,1], dtype=int)
	
for trig in triggers:
	trig_is = np.append(trig_is, np.where(stim==trig))
trig_is = np.sort(trig_is, axis=0)

### extract relevant epochs ###
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
