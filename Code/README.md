# About the code

The Python code for all calculations is provided here in the form of [Jupyter notebooks](http://jupyter.org/).

## How the notebooks are structured

The Emissions Index combines data from EIA (EIA-923 and Electric Power Monthly) and EPA CEMS. These notebooks provide code to download, clean, and combine that data.

### EPA data

EPA CEMS data with hourly emissions is posted to an ftp site on a quarterly basis. We access hourly emissions data from each state with facilities that report to CEMS.

The `EPA Emissions data` notebook downloads all of files. It also logs the filenames and datetime that each was last updated.

After the individual files are downloaded, the data are grouped to a monthly level and exported as a single file in the `Group EPA emissions data by month` notebook.

### EIA data

We use generation and fuel consumption data (EIA-923) reported in EIA's bulk download. Because not all facilities report to 923 on a monthly basis, we also use the national-level generation and consumption totals calculated for the Electric Power Monthly. These two sets of data are extracted from the `ELEC.txt` bulk download file in the `EIA Bulk Download - extract facility generation` and `EIA bulk download - non-facility (distributed PV & state-level)` notebooks.

Finally, we use published EIA combustion emission factors (suplemented with data from EPA and IPCC), found in the `Emission factors` notebook.
