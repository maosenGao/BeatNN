import numpy as np
import matplotlib.pyplot as plt
import mne

data_dir = '../data/OpenMIIR/data/'
file_name = 'P01-raw.fif'  

# load the data
raw = mne.io.read_raw_fif(data_dir+file_name, preload=True)
'''
Stimuli trigger codes are in the data channel called 'STI 014'. 

In this channe a zero means no stimulus trigger present. Each stimulus type has an identifying code (either two- or three-long). These codes work the following way:

-The rightmost number indicates the condition
-The other number(s) indicate the stimulus ID (12 different total)

Additionally there are four-long trigger codes. 

All possible trigger codes are:
--------------------------
Stim     C1   C2   C3   C4
--------------------------
1.	 11   12   13   14   
2.	 21   22   23   24
3. 	 31   32   33   34   
4. 	 41   42   43   44  
5. 	111  112  113  114  
6. 	121  122  123  124  
7. 	131  132  133  134  
8. 	141  142  143  144  
9. 	211  212  213  214  
10. 	221  222  223  224  
11. 	231  232  233  234
12. 	241  242  243  244 

other trigger codes:
0 1000 1111 2001
'''

### get the data array and time array ###
data, stim, time = raw.get_data()[:-1,:], raw.get_data()[-1,:], raw.times

print(type(data[0,0]))

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

X = np.empty([0,nchans,epoch_size])# dataset
for t in range(3):#epoch_size):
	idx = np.linspace((trig_is-t),(trig_is-t)+epoch_size,num=epoch_size,dtype=int).T
	X = np.append(
		X,
		np.transpose(data[:,idx],(1,0,2)),
		axis=0)

base_secs = 0.1 # baseline
base_samp = np.floor(0.1*fs).astype(int)
X = X - np.mean(X[:,:,:base_samp],axis=2,keepdims=True)

plt.plot(X[0].T)
plt.savefig('test.png')





