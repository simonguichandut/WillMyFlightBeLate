- `download.py` uses selenium to download month-by-month delay data from the BTS into files `20XX/all_data_monthN.csv`, where N=1,...,12. Each download takes ~1-2 minutes.
- `Get_Airports.py` selects the rows with flights departing from top 6 busiest airports in the US, assembling all months of the year, and saves to `20XX/[airport_name].csv`.

Note that these csv's are not stored on the public repo..
