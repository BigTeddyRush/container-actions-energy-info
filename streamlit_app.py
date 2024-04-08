import requests
from bs4 import BeautifulSoup
import json
import datetime
import pandas as pd
import streamlit as st
import plotly.express as px

# Benutzereingaben für Start- und Enddatum erhalten
start_date = '2024-02-01'
end_date = '2024-02-01'

# URL mit Benutzereingaben für Start- und Enddatum generieren
siteurl = f"https://api.energy-charts.info/total_power?country=de&start={start_date}T00%3A00%2B01%3A00&end={end_date}T23%3A45%2B01%3A00"

print("Generierte URL:", siteurl)

# power consumption in Germany on one specific day
#siteurl = "https://api.energy-charts.info/total_power?country=de&start=2023-01-01T00%3A00%2B01%3A00&end=2023-01-01T23%3A45%2B01%3A00"
response = requests.get(siteurl)
power_consumption = json.loads(response.content.decode('utf-8'))

# create a list of the time_stamps, types and data
unix_seconds_list = []
name_list = []
data_list = []
for typ in range(len(power_consumption['production_types'])):
    for time in range(len(power_consumption['unix_seconds'])):
        # append unix_seconds
        unix_seconds_list.append(datetime.datetime.fromtimestamp(power_consumption['unix_seconds'][time]).strftime("%m/%d/%Y, %H:%M:%S"))
        # append production_types
        name_list.append(power_consumption['production_types'][typ]['name'])
        # append data
        data_list.append(power_consumption['production_types'][typ]['data'][time])

# create dict
power_consumption_dict = {'unix_seconds' : unix_seconds_list, 'name' : name_list, 'data' : data_list}

################################

data = power_consumption_dict

df = pd.DataFrame(data)

# Streamlit-App-Layout definieren
st.title('Visualisierung des DataFrames')

# DataFrame anzeigen
st.write(df)

# Plot erstellen
fig = px.line(df, x='unix_seconds', y='data', color='name', title='Hydro pumped storage consumption über die Zeit')
fig.update_layout(xaxis_title='Zeit', yaxis_title='Verbrauch')
st.plotly_chart(fig)
