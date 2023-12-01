# Why Is My Flight Late?

This is our data science project for the Erdos Institute data science bootcamp 2023. We will be using machine learning to answer the question, Why is My Flight Late?

## Team
- Ketan Sand
- Marcus Merryfield
- Simon Guichandut
- Tim Hallatt

PhD students at McGill University and the Trottier Space Institute.

Here is a plot showing 11 years data of departure delay (in mins) from the busiest airport in US - Hartsfield-Jackson Atlanta International Airport Atlanta, GA. We see quite a lot of day to day variation, having an estimate on how much delay we expect and what might be the reason will not only help passengers but also save overhead costs for airports and airlines.

![Atlanta_all](https://github.com/simonguichandut/WhyIsMyFlightLate/assets/55292615/5a75b47d-84a3-4f7e-aeb3-db2d8b5cda09)


## Write a brief description of our analysis here
Stage one of our analysis is to clean and prepare the data for training. 

In /data we include our cleaning and analysis scripts.

In /notebooks we include the following:
- Exoploratory.ipynb contains our preliminary analysis tracking the fraction of delayed flights as functions of origin, destinations, time of year, time of day.
- Classification-final.ipynb contains the classification script using logistic regression, random forest, and XGBoost.
- Hyperparameter_tuning_future.ipynb contains preliminary hyperparameter tuning.

In /models we include the final trained models from our analysis.
