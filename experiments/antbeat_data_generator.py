import numpy as np
import matplotlib.pyplot as plt
import mne
import utils.data_utils 
import scipy.io as sp

# global variables
data_dir = '../datasets/AntBeatRateChanges/data/'


subject_ids = dict(SubjGA='39')

# preparing the general mountage
mat_channel_file = sp.loadmat(data_dir+'channel_initial.mat')['Channel']
positions = np.zeros((len(mat_channel_file[0,:]),3))
for ichan in range(len(mat_channel_file[0,:])):
	positions[ichan,0] = -mat_channel_file[0,ichan][3].T[0,1]
	positions[ichan,1] = mat_channel_file[0,ichan][3].T[0,0]
	positions[ichan,2] = mat_channel_file[0,ichan][3].T[0,2]
ch_names = []
for ichan in range(len(mat_channel_file[0,:])):	
	ch_names.append(mat_channel_file[0,ichan][0][0])
montage = mne.channels.Montage(positions,ch_names,'Neuroscan64',range(len(mat_channel_file[0,:])))

# loading the raw data
raw = mne.io.read_raw_cnt(data_dir+'IR/'+'ANT_S11_B01_Data.cnt',montage=montage,preload=True)								
# extracting the triggers for stimuli
stim_events = mne.events_from_annotations(raw)		
print(np.diff(stim_events[0][:,0]))
stim_ev = [] 
for ival in stim_events[0][:,2]:
	for key, val in stim_events[1].items():
		if val == ival:
			stim_ev.append(int(key))
print(stim_ev[:200])

