# Literature Review

## Stober S, Sternin A, Owen AM, Grahn JA. Towards Music Imagery Information Retrieval: Introducing the OpenMIIR Dataset of EEG Recordings from Music Perception and Imagination. InISMIR 2015 (pp. 763-769).

- Significance: first open dataset of eeg recordings during music listening and imagination. Meant to allow MIR researchers, who usually don't have brain recording devices, to access brain data.
- Dataset metadata: 10 participants (4 excluded due to low melody familiarity scores). The publicly available dataset is the raw eeg data with no pre-processing applied to it. 
- Stimuli: 2 parts, 5 blocks per part, 12 melody stimuli in random order per block. The first part of the experiment consisted of cued (metronome clicks before the beginning of the melody) perception and imagination trials, and uncued imagination trials. The second part consisted of uncued imagined trials after which participants indicated whether they were able to imagine the simulus correctly. 240 trials recorded per subject. The first 4 melody stimuli had lyrics. The next 4 melody stimuli were the instrumental version of the simuli with lyrics. The last 4 melody stimuli were excerpts from instrumental pieces of music. All 12 melody stimuli had somewhat different beat speeds. 

## Stober S. Toward studying music cognition with information retrieval techniques: Lessons learned from the OpenMIIR initiative. Frontiers in psychology. 2017 Aug 3;8:1255.

- Significance: overview of the work on music imagery information retrieval (MIIR), carried out between 2015 and 2017, using the OpenMIIR dataset of eeg recordings (Stober et al. 2015). 
- Describes eeg studies that found rich musical features in eeg recordings when people listen and imagine musical stimuli.
- Three experiments with the OpenMIIR dataset:
	1. erp-inspired single trial analysis
		- goal: musical tempo estimation from eeg recordings when listening and imagining musical stimuli.
		- methodology: autocorrelation analysis using a sliding window over a single trial of eeg. The sliding autocorrelations get stacked to a matrix, and the location of the max value indicates the estimated tempo (Sternin et al. 2015).
		- results: encouraging indication that eeg signals contain musical tempo information.
	2. audio envelope reconstruction
		- goal: reconstruct audio envelopes from eeg signals.
		- methodology: convolutional filter learning to convolve the eeg singal and produce the reconstructed stimulus envelope (O'Sullivan et al. 2015).
		- results: not satisfying. Model was overfit and did not generalize.
	3. finding musical stimuli features in eeg
		- goal: identify musical features in the eeg signal that are directly related to the imagination or perception of music. 
		- methodology: 1) autoencoder to reduce the noise in the EEG sinal. 2) classification algorithms for stimulus, group, and meter. 
		- results: encouraging but very early-stage
