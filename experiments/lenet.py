import numpy as np
import matplotlib.pyplot as plt
import mne

data_dir = '../data/OpenMIIR/data/'
file_name = 'P01-raw.fif'  

# load the data
raw = mne.io.read_raw_fif(data_dir+file_name, preload=True)
print(raw.ch_names)
print(np.unique(raw.get_data()[-1,:]))


