# Using selenium chrome webdriver
# https://www.selenium.dev
# https://chromedriver.chromium.org/getting-started

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

import time
import os
import zipfile
import numpy

# Set up webdriver

chrome_options = Options()
chrome_options.add_argument("−−lang=en")
chrome_options.add_argument("--headless=new")
prefs = {
        "download.default_directory": os.getcwd(),
        "download.prompt_for_download": False
}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr")

# Select fields
# List the html ID of all the ones that need to be either checked or un-checked
fields = ["FL_DATE",
          "OP_UNIQUE_CARRIER",
          "ORIGIN_AIRPORT_SEQ_ID", # unclick
          "ORIGIN_CITY_MARKET_ID", # unclick
          "DEST_AIRPORT_SEQ_ID",   # unclick
          "DEST_CITY_MARKET_ID",   # unclick
          "CRS_DEP_TIME",
          "DEP_DELAY",
          "CANCELLED",
          "CANCELLATION_CODE",
          "AIR_TIME",
          "CARRIER_DELAY",
          "WEATHER_DELAY",
          "NAS_DELAY",
          "SECURITY_DELAY",
          "LATE_AIRCRAFT_DELAY"]

for f in fields:
    checkbox = driver.find_element(By.ID, f)
    checkbox.click()


# Get the dropdowns
year_dropdown = Select(driver.find_element(By.ID, "cboYear"))
month_dropdown = Select(driver.find_element(By.ID, "cboPeriod"))

# Download button
download_button = driver.find_element(By.ID, "btnDownload")

# Download, unzip, rename
def download_one(year,month):

    year,month = str(year),str(month)

    if not os.path.exists(year):
        os.mkdir(year)

    year_dropdown.select_by_value(year)
    month_dropdown.select_by_value(month)
    download_button.click()

    zfile = "DL_SelectFields.zip"

    # Wait until download is finished
    while not os.path.exists(zfile):
        time.sleep(1)

    with zipfile.ZipFile(zfile,"r") as z:
        z.extractall(".")

    os.rename("T_ONTIME_REPORTING.csv", f"{year}/all_data_month{month}.csv")
    os.remove("DL_SelectFields.zip")

# Test
#download_one(2015,10)

if __name__ == "__main__":
    Months = numpy.arange(1,13)
    #Years = numpy.arange(1983,2023)
    Years = [2012,2011]

    for year in Years:
        for month in Months:
            download_one(year,month)
        print(year, " done")

driver.quit()
