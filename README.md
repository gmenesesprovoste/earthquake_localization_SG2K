# earthquake_localization_SG2K

This script automates the task of locating earthquakes by picking seismic waves on a local seismic dataset. 

- Interacts with the user via Seisgram2K (Source code: http://alomax.net/projects/java), a program for interactive viewing of earthquake seismograms
- Generates .pick files for a set of folders "aammdd_hhmm" (each an earthquake) containing MSEED or SAC records of several seismic stations
- nstamin variable sets the minimum number of station required to locate
- Localization is performed folder by folder (event by event)
- Adds the possibility to correct high RMS stations

Following folder configuration needed:
* Assuming that the event folders "aammdd_hhmm" are located in /home/region:
  - add a "/home/region/LOC/TIME" and "/home/region/LOC/GRIDMODEL" folders. TIME and GRIDMODEL are generated with NonLinLoc (Lomax A. et al., 2000, 2014)       with the commands Vel2Grid and Grid2Time
  - add the configuration file "/home/region/NLLOC.IN"
  - add the empty folder "/home/region/FINAL"

