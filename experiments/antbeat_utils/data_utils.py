import numpy as np
import scipy.io as sp
import mne

def get_subj_names_ids_dict():
	subj_names_ids_dict = {
		'EGnew':'S01',
		'CPDnew':'S02',
		'TDnew':'S03',
		'CDnew':'S04',
		'SYLnew':'S06',
		'MH':'S07',
		'AC':'S08',
		'EC':'S09',
		'IR':'S11',
		'CB':'S12',
		'WD':'S13',
		'DJ':'S14',
		'JH':'S15',
		'MHert':'S16',
		'JC':'S18',
		'KK':'S19',
		'YA':'S20',
		'AW':'S21',
		'CT':'S23'}
	return subj_names_ids_dict

def get_trial_type_trig_dict():
	trial_type_trigger_dict = {
		'Accel short norm':[
			117,
			115,1115,2115,
			111,1111,2111,
			110],
		'Accel medium norm':[
			127,
			125,1125,2125,
			122,1122,2122,
			121,1121,2121,
			120],	
		'Accel long norm':[
			137,
			135,1135,2135,
			133,1133,2133,
			132,1132,2132,
			131,1131,2131,
			130],
		'Decel short norm':[
			217,
			215,1215,2215,
			211,1211,2211,
			210],
		'Decel medium norm':[
			227,
			225,1225,2225,
			222,1222,2222,
			221,1221,2221,
			220],
		'Decel long norm':[
			237,
			235,1235,2235,
			233,1233,2233,
			232,1232,2232,
			231,1231,2231,
			230],
		'Steady short norm':[
			61 ,
			59 ,1059,2059,
			55 ,1055,2055,
			54 ],
		'Steady medium norm':[
			71 ,
			69 ,1069,2069,
			66 ,1066,2066,
			65 ,1065,2065,
			64 ],	
		'Steady long norm':[
			81 ,
			79 ,1079,2079,
			77 ,1077,2077,
			76 ,1076,2076,
			75 ,1075,2075,
			74 ],
		'Accel short targ':  [11,],
		'Accel medium targ': [12,],
		'Accel long targ':   [13,],
		'Decel short targ':  [21,],
		'Decel medium targ': [22,],
		'Decel long targ':   [23,],
		'Steady short targ': [31,],
		'Steady medium targ':[32,],	
		'Steady long targ':  [33,]
		}
	return trial_type_trigger_dict

def get_phases_trig_dict():
	phase_trigger_dict = {
		'Visual':[117,127,137,217,227,237,61 ,71 ,81 ,],
		'Initial':[115,1115,2115,
			125,1125,2125,
			135,1135,2135,
			215,1215,2215,
			225,1225,2225,
			235,1235,2235,
			59 ,1059,2059,
			69 ,1069,2069,
			79 ,1079,2079,],
		'Anticipation':[111,1111,2111,
			122,1122,2122,
			121,1121,2121,
			133,1133,2133,
			132,1132,2132,
			131,1131,2131,
			211,1211,2211,
			222,1222,2222,
			221,1221,2221,
			233,1233,2233,
			232,1232,2232,
			231,1231,2231,
			55 ,1055,2055,
			66 ,1066,2066,
			65 ,1065,2065,
			77 ,1077,2077,
			76 ,1076,2076,
			75 ,1075,2075,],
		'Changing':[110,120,130,210,220,230,54,64,74,
			11 ,12 , 13 ,21 ,22 ,23 ,31 ,32 ,33 ,],
			}
	return phase_trigger_dict

def generate_phase_trial_type_trigger_dict():
	phase_trial_type_trigger_dict = {
		'ASV':117,
		'ASI0':115,'ASI1':1115,'ASI2':2115,
		'AS10':111,'AS11':1111,'AS12':2111,
		'ASC':110,

		'AMV':127,
		'AMI0':125,'AMI1':1125,'AMI2':2125,
		'AM10':122,'AM11':1122,'AM12':2122,
		'AM20':121,'AM21':1121,'AM22':2121,
		'AMC':120,	

		'ALV':137,
		'ALI0':135,'ALI1':1135,'ALI2':2135,
		'AL10':133,'AL11':1133,'AL12':2133,
		'AL20':132,'AL21':1132,'AL22':2132,
		'AL30':131,'AL31':1131,'AL32':2131,
		'ALC':130,

		'DSV':217,
		'DSI0':215,'DSI1':1215,'DSI2':2215,
		'DS10':211,'DS11':1211,'DS12':2211,
		'DSC':210,

		'DMV':227,
		'DMI0':225,'DMI1':1225,'DMI2':2225,
		'DM10':222,'DM11':1222,'DM11':2222,
		'DM20':221,'DM21':1221,'DM22':2221,
		'DMC':220,
	
		'DLV':237,
		'DLI0':235,'DLI1':1235,'DLI2':2235,
		'DL10':233,'DL11':1233,'DL12':2233,
		'DL20':232,'DL21':1232,'DL22':2232,
		'DL30':231,'DL31':1231,'DL32':2231,
		'DLC':230,

		'SSV':61 ,
		'SSI0':59 ,'SSI1':1059,'SSI2':2059,
		'SS10':55 ,'SS11':1055,'SS12':2055,
		'SSC':54 ,
		
		'SMV':71 ,
		'SMI0':69 ,'SMI1':1069,'SMI2':2069,
		'SM10':66 ,'SM11':1066,'SM12':2066,
		'SM20':65 ,'SM21':1065,'SM22':2065,
		'SMC':64 ,	
		
		'SLV':81 ,
		'SLI0':79 ,'SLI1':1079,'SLI2':2079,
		'SL10':77 ,'SL11':1077,'SL12':2077,
		'SL20':76 ,'SL21':1076,'SL22':2076,
		'SL30':75 ,'SL31':1075,'SL32':2075,
		'SLC':74 ,
		
		'TASC':11,
		'TAMC':12,
		'TALC':13,		
		'TDSC':21,
                'TDMC':22,
		'TDLC':23,
		'TSSC':31,
                'TSMC':32,
	        'TSLC':33
		}
	return phase_trial_type_trigger_dict		

def get_eeg_montage(data_dir):
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

	return montage

def load_raw(data_dir,subj,isubj,irec,montage):		
	raw = mne.io.read_raw_cnt(data_dir+subj+'/ANT_'+isubj+'_B0'+str(irec)+'_Data.cnt',montage=montage,preload=True)
	return raw

def get_beat_trigs():
	beat_trigs = [115,125,135,215,225,235,59,69,79,
			111,122,121,133,132,131,
			211,222,221,233,232,231,
			55 ,66 ,65 ,77 ,76 ,75]
	return beat_trigs

def load_trigger_events(data_dir,subj,isubj,irec,phase_trial_type_trigger_dict):
	trigger_events = mne.io.curry.curry._read_events_curry(data_dir+subj+'/ANT_'+isubj+'_B0'+str(irec)+'.ceo')
	beat_trigs = get_beat_trigs() 
	num_trigs = trigger_events.shape[0]
	itrig = 0
	while itrig < num_trigs:
		trig = trigger_events[itrig,2]
		if trig == 119:
			trigger_events[itrig,2] = 117
		if trig == 129:
			trigger_events[itrig,2] = 127
		if trig == 139:
			trigger_events[itrig,2] = 137
		if trig == 219:
			trigger_events[itrig,2] = 217
		if trig == 229:
			trigger_events[itrig,2] = 227
		if trig == 239:
			trigger_events[itrig,2] = 237
		if trig == 63:
			trigger_events[itrig,2] = 61
		if trig == 73:
			trigger_events[itrig,2] = 71
		if trig == 83:
			trigger_events[itrig,2] = 81
		if trig in beat_trigs:
			trigger_events = np.insert(trigger_events,itrig+1,
						trigger_events[itrig]+[300,0,1000],
						axis=0)
			itrig += 1
			num_trigs += 1
			trigger_events = np.insert(trigger_events,itrig+1,
						trigger_events[itrig]+[300,0,1000],
						axis=0)
			itrig += 1
			num_trigs += 1

		itrig += 1			
	trigger_events = np.asarray([event for event in trigger_events if (event[-1] in phase_trial_type_trigger_dict.values())])
	return trigger_events

def apply_ssp(raw,subj,irec):
	raw.set_channel_types(mapping={'HEO':'eog','VEO':'misc','Trigger':'misc'}) # making HEO channel be of 'eog' type to find its projectors                        
	projs_heo, events = mne.preprocessing.compute_proj_eog(raw, n_eeg=1, average=True) # SSP HEO
	raw.set_channel_types(mapping={'HEO':'misc','VEO':'eog','Trigger':'misc'}) # making VEO channel be of 'eog' type to find its projectors                        
	print(subj,irec)
	projs_veo, events = mne.preprocessing.compute_proj_eog(raw, n_eeg=1, average=True) # SSP VEO
	raw.add_proj(projs_veo) # adding the projectors
	raw.add_proj(projs_heo) # adding the projectors
	raw.set_channel_types(mapping={'HEO':'misc','VEO':'misc','Trigger':'misc'}) # making non EEG channels be of 'misc' type   
	return raw

def epoch_raw_with_ssp(all_trigger_events,phase_trial_type_trigger_dict, raw,subj,irec, tmin=-0.1, tmax=0.5):
	unique_trigger_events_in_raw = np.unique(all_trigger_events[:,2])
	phase_trial_type_trigger_dict_in_raw = {key:val for key, val in phase_trial_type_trigger_dict.items() if val in unique_trigger_events_in_raw} 
	raw = apply_ssp(raw,subj,irec) 
	event_id, tmin, tmax = phase_trial_type_trigger_dict_in_raw, tmin, tmax 
	epoch_params = dict(events = all_trigger_events, event_id = event_id, tmin=tmin, tmax=tmax, preload=True) 
	epochs = mne.Epochs(raw, **epoch_params) 	
	return epochs

def generate_epoch_label_matrix(all_trigger_events, phase_trigger_dict, trial_type_trigger_dict,isubj_count):
	# isubj_count, iphase, itrial_type 
	num_events = all_trigger_events.shape[0]
	labels = np.empty((num_events,3))*np.nan
	for ievent in range(num_events):
		labels[ievent,0] = isubj_count
		event = all_trigger_events[ievent,2]
		for iphase, (phase, triggs) in enumerate(phase_trigger_dict.items()):
			if event in triggs:
				labels[ievent,1] = iphase
		for itrial_type, (trial_type, triggs) in enumerate(trial_type_trigger_dict.items()):
			if event in triggs:
				labels[ievent,2] = itrial_type
	return labels
