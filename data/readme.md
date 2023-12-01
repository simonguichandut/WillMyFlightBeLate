- `download.py` uses selenium to download month-by-month delay data from the BTS into files `20XX/all_data_monthN.csv`, where N=1,...,12. Each download takes ~1-2 minutes.
- `Get_Airports.py` selects the rows with flights departing from top 6 busiest airports in the US, assembling all months of the year, and saves to `20XX/[airport_name].csv`.
- `Get_airport_stats.py` and `Get_carrier_stats.py` create small csv's containing statistics about total number of flights and fraction of delays, grouped by airport and carriers.
- `Get_clean_datasets.py` selects flights coming and going from the top 20 airports in the US, creates a proper datetime column for the scheduled departure, and does some more cleaning. Makes the `clean_data.csv` file which we use for exploratory data analysis and machine learning.

Note that these csv's are not stored on the public repo..
