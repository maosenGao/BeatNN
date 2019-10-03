#!/bin/bash

# create container directories
mkdir OpenMIIR
mkdir OpenMIIR/data

# download the data
curl http://www.ling.uni-potsdam.de/mlcog/OpenMIIR-RawEEG_v1/README.md --output OpenMIIR/data/README.md
curl http://www.ling.uni-potsdam.de/mlcog/OpenMIIR-RawEEG_v1/P01-raw.fif --output OpenMIIR/data/P01-raw.fif
curl http://www.ling.uni-potsdam.de/mlcog/OpenMIIR-RawEEG_v1/P04-raw.fif --output OpenMIIR/data/P04-raw.fif
curl http://www.ling.uni-potsdam.de/mlcog/OpenMIIR-RawEEG_v1/P05-raw.fif --output OpenMIIR/data/P05-raw.fif
curl http://www.ling.uni-potsdam.de/mlcog/OpenMIIR-RawEEG_v1/P06-raw.fif --output OpenMIIR/data/P06-raw.fif
curl http://www.ling.uni-potsdam.de/mlcog/OpenMIIR-RawEEG_v1/P07-raw.fif --output OpenMIIR/data/P07-raw.fif
curl http://www.ling.uni-potsdam.de/mlcog/OpenMIIR-RawEEG_v1/P09-raw.fif --output OpenMIIR/data/P09-raw.fif
curl http://www.ling.uni-potsdam.de/mlcog/OpenMIIR-RawEEG_v1/P11-raw.fif --output OpenMIIR/data/P11-raw.fif
curl http://www.ling.uni-potsdam.de/mlcog/OpenMIIR-RawEEG_v1/P12-raw.fif --output OpenMIIR/data/P12-raw.fif
curl http://www.ling.uni-potsdam.de/mlcog/OpenMIIR-RawEEG_v1/P13-raw.fif --output OpenMIIR/data/P13-raw.fif
curl http://www.ling.uni-potsdam.de/mlcog/OpenMIIR-RawEEG_v1/P14-raw.fif --output OpenMIIR/data/P14-raw.fif
