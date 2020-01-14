# acis_check_pha_range

## SYNOPSIS

Compute approximate energy range for on-orbit PHA filter.

## SYNTAX

```
acis_check_pha_range  infile [mskfile] [binsize] [verbose]
```

## DESCRIPTION

All ACIS observations use an on-orbit PHA filter. The values used on orbit are stored in the Level 1 mask 
file, \*_msk1.fits: PHAMIN and PHAMAX column values. The default filter used by most observations retains 
event with energies in the approximately the 0.2 to 14 keV range.

However, observers may request an arbitrary energy filter. The only advantage to using an energy filter is 
when the expected count rate in the field would be near the telemetry saturation limit. Nonetheless, there 
are numerous observations which specify an energy filter with low count fields.

The problem is that observers specify a filter in energy units (keV). The actual filtering on orbit is done 
on the events' Pulse Height Amplitude (PHA), in ADU (engineering) units. The on orbit PHA value differs 
from the PHA value computed by acis_process_events since it does not include CTI corrections. The on-orbit 
PHA value is closest to the PHA_RO (PHA Read Out) value in the event list. As a result, the gain conversion 
from on-orbit PHA_RO to observed ENERGY varies spatially (due to CTI and node-to-node gain settings), 
varies with energy (gain is non-linear with energy), and varies with time (short term CTI temperature 
dependent effects and long term time adjustments).

The purpose of this script then is to compute an estimated gain based on the actual observed event data, 
and use it to compute an approximate energy range where all events were telemetered.

### Description of Algorithm

This tool works by ignoring the temporal and spectral (non-linear) gain variations. It computes a gain map 
(eV/ADU) in CHIP coordinates by computing the mean ENERGY/PHA_RO of the events in 128x128 blocks (default 
binsize). It then applies these gain values to the PHA_RO limits obtained from the level1 mask: PHAMIN and 
PHAMAX column values. The maximum, low energy and the minimum, high energy values are then a conservative, 
approximate set of energy limits.

## EXAMPLES

### EXAMPLE 1

```
unix% acis_check_pha_range 5705/primary/acisf05705N003_evt2.fits.gz


acis_check_pha_range
        infile = 5705/primary/acisf05705N003_evt2.fits.gz
       mskfile = 
       binsize = 128
       verbose = 1
          mode = ql

Using maskfile: '5705/secondary/acisf05705_000N003_msk1.fits'
Processing data for CCD_ID=2
Processing data for CCD_ID=3
Processing data for CCD_ID=5
Processing data for CCD_ID=6
Processing data for CCD_ID=7
Processing data for CCD_ID=8
#ccd_id	pha_lo	pha_hi	E_lo	E_hi
2	39	2499	 192.1	  9383.1
3	39	2499	 191.3	  9892.4
5	26	2499	 127.6	 10808.6
6	39	2499	 202.8	  9642.1
7	26	2499	 128.9	 11380.3
8	39	2499	 202.8	 10662.5

Conservative limits are 202.8 to 9383.1 eV
```

This example shows the results for OBSID 5705. The observation used a non-standard high energy threshold. 
The requested cutoff, as reported by ChaSER, was 10keV. However, due to gain corrections on different 
chips, the energy cutoff on CCD_ID 2 is **approximately** 9.4 keV.

### EXAMPLE 2

```
unix% acis_check_pha_range 5705/primary/acisf05705N003_evt2.fits.gz bin=32


acis_check_pha_range
        infile = 5705/primary/acisf05705N003_evt2.fits.gz
       mskfile = 
       binsize = 32
       verbose = 1
          mode = ql

Using maskfile: '5705/secondary/acisf05705_000N003_msk1.fits'
Processing data for CCD_ID=2
Processing data for CCD_ID=3
Processing data for CCD_ID=5
Processing data for CCD_ID=6
Processing data for CCD_ID=7
Processing data for CCD_ID=8
#ccd_id	pha_lo	pha_hi	E_lo	E_hi
2	39	2499	 306.9	  9192.8
3	39	2499	 310.1	  9812.4
5	26	2499	 264.6	 10759.3
6	39	2499	 326.2	  9561.1
7	26	2499	 208.1	 11232.7
8	39	2499	 305.6	 10591.7

Conservative limits are 326.2 to 9192.8 eV
```

The same as the previous example but now using a smaller bin size. Since this observation contains a low 
number of counts, the mean gain value in each bin is somewhat sensitive to the binsize. The approximate low 
energy threshold has changed from 0.2 to 0.36keV.

### EXAMPLE 3

```
unix% acis_check_pha_range 2785/primary/acisf02785N003_evt2.fits.gz


acis_check_pha_range
        infile = 2785/primary/acisf02785N003_evt2.fits.gz
       mskfile = 
       binsize = 128
       verbose = 1
          mode = ql

Using maskfile: '2785/secondary/acisf02785_000N003_msk1.fits'
Processing data for CCD_ID=2
Processing data for CCD_ID=3
Processing data for CCD_ID=5
Processing data for CCD_ID=6
Processing data for CCD_ID=7
Processing data for CCD_ID=8
#ccd_id	pha_lo	pha_hi	E_lo	E_hi
2	126	3124	 554.6	 11794.5
3	126	3124	 592.9	 12370.8
5	126	3124	 613.8	 13579.9
6	126	3124	 602.3	 12109.2
7	126	3124	 622.8	 14141.2
8	126	3124	 640.2	 13332.6

Conservative limits are 640.2 to 11794.5 eV
```

OBSIS 2785 is an example were a low energy threshold was requested. The requested threshold was 0.5keV. 
Based on the approximate gain maps, the minimum safe energy (above which we expect to have received all 
events) is closer to 0.64 keV.

## PARAMETERS

|  NAME   |  TYPE   | FILETYPE | DEF | MIN | MAX | REQD | STACKS |
|---------|---------|----------|-----|-----|-----|------|--------|
| infile  | file    | input    |     |     |     | yes  | no     |
| mskfile | file    | input    |     |     |     | no   |        |
| binsize | integer |          | 128 |     |     |      |        |
| verbose | integer |          | 1   | 0   | 5   |      |        |

## DETAILED PARAMETER DESCRIPTIONS

### `infile`

          type=file
          filetype=input
          reqd=yes
          stacks=no

Input ACIS Level 2 event file.

The level 2 event file. Users should not use the Level 1 event file since the bad grades and bad pixels 
lead to different gain estimates.

### `mskfile`

          type=file
          filetype=input
          reqd=no

The ACIS mask file

The mask file, \*_msk1.fits, for the observation. If left blank, the tool will attempt to locate the 
file specified in the MASKFILE keyword in the event file.

### `binsize`

          type=integer
          def=128

Block size in chip coordinates used to estimate the gain.

The gain is estimated by computing the mean ENERGY/PHA_RO for the events in 128x128 blocks (in chip 
coordinates). Since it is computing an average, a large number of events is required to get a 
meaningful estimate. For observations with large number of events, the binsize can be decreased to 
better capture the spatial variation across the detector.

Since the mean gain must not be compute across node boundaries, the binsize is restricted to the 
following values: 1,2,4,8,16,32,64,128,256.

### `verbose`

          type=integer
          def=1
          min=0
          max=5

Amount of tool chatter level.

## About Contributed Software

This script is not an official part of the CIAO release but is made available as "contributed" software via 
the CIAO scripts page https://cxc.harvard.edu/ciao/download/scripts/ . Please see this page for 
installation instructions.


## BUGS

See the bug pages https://cxc.harvard.edu/ciao/bugs/acis_check_pha_range.html on the CIAO website for an 
up-to-date listing of known bugs.


## SEE ALSO

      ------------------------------------------------------------------------------------------------------------
      | CONTEXT |                                            SUBJECTS                                            |
      |---------|------------------------------------------------------------------------------------------------|
      | chandra | eventdef                                                                                       |
      |---------|------------------------------------------------------------------------------------------------|
      | tools   | acis_build_badpix, acis_clear_status_bits, acis_detect_afterglow, acis_find_afterglow,         |
      |         | acis_process_events, acis_streak_map, acisreadcorr, destreak, readout_bkg                      |
      ------------------------------------------------------------------------------------------------------------

## LAST MODIFIED

January 2020
