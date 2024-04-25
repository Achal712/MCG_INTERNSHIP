import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Load CSS file
def local_css(file_path):
    with open(file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("styles.css")

st.markdown('<h1 class="title">Covid-19 World-wide Cases</h1>', unsafe_allow_html=True)

# Load COVID-19 data
@st.cache_resource
def load_data():
    data = pd.read_csv("country_wise_latest.csv")
    return data

data = load_data()

# Sidebar
st.sidebar.markdown('<h3 class="sidebar-header">TEAM 2</h3>', unsafe_allow_html=True)
st.sidebar.markdown('<h4 class="sidebar-title">COVID-19 Dashboard</h4>', unsafe_allow_html=True)
visualization = st.sidebar.selectbox('Select a Chart type',('Bar Chart','Line Chart'))
selected_country = st.sidebar.selectbox('Select a country', data['Country/Region'].unique())
st.sidebar.markdown(f'<div class="sub">You selected: {selected_country}</div>', unsafe_allow_html=True)

# Filter data by selected country
df = data[data['Country/Region'] == selected_country]
df = df.drop(columns=['Deaths / 100 Cases', 'Recovered / 100 Cases', 'Deaths / 100 Recovered', '1 week % increase'])
df = df.sum()

st.markdown(f'<div class="sub">Total confirmed cases:</div>', unsafe_allow_html=True)

# Display total confirmed cases in a container
latest_cases = df[1]
st.markdown(f'<div class="stInfo">{latest_cases}</div>', unsafe_allow_html=True)
    
# Main section
st.markdown('<div class="pub">Visualization</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown(f'<div class="app">Total confirmed cases in {selected_country}</div>', unsafe_allow_html=True)
    if visualization == 'Bar Chart':
        st.bar_chart(df)
    elif visualization == 'Line Chart':
        st.line_chart(df)

with col2:
    st.markdown(f'<div class="app">Total confirmed cases in {selected_country} (for 7 days)</div>', unsafe_allow_html=True)
    recent_data = df.tail(7)
    if visualization == 'Bar Chart':
        st.bar_chart(recent_data)
    elif visualization == 'Line Chart':
        st.line_chart(recent_data)

st.header('Pie Chart for COVID-19 Cases')
cases_labels = ['Confirmed', 'Deaths', 'Recovered', 'Active']
cases_data = [df['Confirmed'], df['Deaths'], df['Recovered'], df['Active']]
fig = px.pie(values=cases_data, names=cases_labels)
st.plotly_chart(fig)
st.header('Male female Pie Chart')
cases_labels = ['Male', 'Female', 'Children']
cases_data = [df['Male'], df['Female'], df['Children']]
fig = px.pie(values=cases_data, names=cases_labels)
st.plotly_chart(fig)

st.sidebar.header('COVID-19 Cases in '+selected_country)
st.sidebar.markdown(f'<p class="custom-text">Confirmed: {df["Confirmed"]}</p>', unsafe_allow_html=True)
st.sidebar.markdown(f'<p class="custom-text">Deaths: {df["Deaths"]}</p>', unsafe_allow_html=True)
st.sidebar.markdown(f'<p class="custom-text">Recovered: {df["Recovered"]}</p>', unsafe_allow_html=True)
st.sidebar.markdown(f'<p class="custom-text">Active: {df["Active"]}</p>', unsafe_allow_html=True)
st.sidebar.markdown(f'<p class="custom-text">Male: {df["Male"]}</p>', unsafe_allow_html=True)
st.sidebar.markdown(f'<p class="custom-text">Female: {df["Female"]}</p>', unsafe_allow_html=True)
st.sidebar.markdown(f'<p class="custom-text">Children: {df["Children"]}</p>', unsafe_allow_html=True)
st.set_option('deprecation.showPyplotGlobalUse', False)
