This directory contains the raw EEG files of the [OpenMIIR dataset](<https://github.com/sstober/openmiir>) in the
FIF format used by [MNE](<http://martinos.org/mne>).

P01-raw.fif  
P04-raw.fif  
P05-raw.fif  
P06-raw.fif  
P07-raw.fif  
P09-raw.fif  
P11-raw.fif  
P12-raw.fif  
P13-raw.fif  
P14-raw.fif

For more information, please visit [https://github.com/sstober/openmiir](<https://github.com/sstober/openmiir>)

--------------------------------------------------------------

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
