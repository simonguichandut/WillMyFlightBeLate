"""
# App
Will my flight be late?
"""

import streamlit as st
import pandas as pd

airport_stats = pd.read_csv("data/airport_stats.csv", nrows=21)
carrier_stats = pd.read_csv("data/carrier_stats.csv")

# Airports and carriers trained on
# Copied from data/Get_clean_dataset.py
airports = [10397,13930,11298,11292,12892,14107,14771,11057,12266,12889,14747,13487,11433,13204,10721,12953,11618,12478,14869,11278]
carriers = ['WN','DL','AA','OO','UA','B6','AS','NK']

# Convert to names
airports = [airport_stats.loc[airport_stats['ID']==id, 'Name'].values[0] for id in airports]
carriers = [carrier_stats.loc[carrier_stats['Code']==c, 'Name'].values[0] for c in carriers]


##############################################################

st.title("Will My Flight Be Late?")
#st.markdown("# Will My Flight Be Late?")

#flight = st.text_input("Your flight number: ")

col1,col2 = st.columns(2)

with col1:
    carrier = st.selectbox(
            "Flight carrier",
            carriers,
            index=None,
            placeholder="Select carrier")

    orig = st.selectbox(
            "Origin Airport",
            airports,
            index=None,
            placeholder="Select airport")

    dest = st.selectbox(
            "Destination Airport",
            airports,
            index=None,
            placeholder="Select airport")

with col2:
    date = st.date_input("Flight Date", value=None)
    time = st.time_input("Departure Time", value=None)
    airtime = st.slider("Flight duration (hours)", 0.5, 12., value=1., step=0.25)

# st.write(carrier)
# st.write(orig)
# st.write(dest)
# st.write(date)
# st.write(time)
# st.write(airtime)

check_button = st.button("Evaluate", type="primary")

def check():

    # Escape if info is not entered
    if carrier is None or orig is None or dest is None or date is None or time is None:
        st.write("Enter all info!")
        return

    import random
    if random.random() > 0.5:
        st.markdown("<h1 style='text-align: center; color: red;'>YES!</h1>", unsafe_allow_html=True)
        st.text("Our model thinks your flight will be more than 15 minutes late")
    else:
        st.markdown("<h1 style='text-align: center; color: green;'>NO!</h1>", unsafe_allow_html=True)
        st.text("Our model thinks your flight will not be late by more than 15 minutes.")


    with st.expander("Statistics about your flight:"):
        st.write("Over the last 10 years (but excluding pandemic years):")

        st.markdown(":red[%.0f%%] of flights from your carrier have been delayed (:red[%.0f%%] in 2023 only)"%\
                    (carrier_stats.loc[carrier_stats['Name']==carrier, 'delay_frac'].values[0]*100,
                    carrier_stats.loc[carrier_stats['Name']==carrier, 'delay_frac_2023'].values[0]*100))
        
        st.markdown(":red[%.0f%%] of flights from your origin have been delayed (:red[%.0f%%] in 2023 only)"%\
                    (airport_stats.loc[airport_stats['Name']==orig, 'delay_frac_from'].values[0]*100,
                    airport_stats.loc[airport_stats['Name']==orig, 'delay_frac_from_2023'].values[0]*100))
        
        st.markdown(":red[%.0f%%] of flights to your destination have been delayed (:red[%.0f%%] in 2023 only)"%\
                    (airport_stats.loc[airport_stats['Name']==dest, 'delay_frac_to'].values[0]*100,
                    airport_stats.loc[airport_stats['Name']==dest, 'delay_frac_to_2023'].values[0]*100))

if check_button: check()

# About section
st.markdown("### About this app")
st.write("Current model: random")
st.write("By Ketan Sand, Simon Guichandut, Tim Hallatt.")
st.write("We thank the Erdös Institute and our mentor Gleb Zhelezov.")