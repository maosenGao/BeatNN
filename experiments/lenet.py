import numpy as np
import matplotlib.pyplot as plt
import mne

data_dir = '../data/OpenMIIR/data/'
file_name = 'P01-raw.fif'  

# load the data
raw = mne.io.read_raw_fif(data_dir+file_name, preload=True)
'''
Stimuli trigger codes are in the data channel called 'STI 014'. 

In this channel, a zero means no stimulus trigger present. Each stimulus type has an identifying code (either two- or three-long). These codes work the following way:

-The rightmost number indicates the condition
-The other number(s) indicate the stimulus ID (12 different total)

Additionally there are four-long codes. 
'''
print(raw.ch_names)
print(np.unique(raw.get_data()[-1,:], return_counts=True))


