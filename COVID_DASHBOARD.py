import streamlit as st
import pandas as pd
import plotly.express as px

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

st.markdown(f'<div class="sub1">Total confirmed cases:</div>', unsafe_allow_html=True)

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

st.header('Male female Pie Chart')
cases_labels = ['Male', 'Female', 'Children']
cases_data = [df['Male'], df['Female'], df['Children']]
fig = px.pie(values=cases_data, names=cases_labels)
st.plotly_chart(fig)
col2_1, col2_2 = st.columns((2))
with col2_1:
    container2_1 = st.container(border=True)
    container2_1.write("<p class='confirmed-container'><b>Confirmed:</b></p>", unsafe_allow_html=True)
    container2_1.write(f'<p class="custom-text confirmed-container">{df["Confirmed"]}</p>', unsafe_allow_html=True)

with col2_2:
    container2_2 = st.container(border=True)
    container2_2.write("**Male**")
    container2_2.write(f'<p class="custom-text"> {df["Male"]}</p>', unsafe_allow_html=True)
with col2_1:
    container2_1 = st.container(border=True)
    container2_1.write("**Female**")
    container2_1.write(f'<p class="custom-text">{df["Female"]}</p>', unsafe_allow_html=True)
with col2_2:
    container2_2 = st.container(border=True)
    container2_2.write("**Children**")
    container2_2.write(f'<p class="custom-text">{df["Children"]}</p>', unsafe_allow_html=True)


st.sidebar.header('COVID-19 Cases in '+selected_country)
st.sidebar.markdown(f'<p class="custom-text">Confirmed: {df["Confirmed"]}</p>', unsafe_allow_html=True)
st.sidebar.markdown(f'<p class="custom-text">Deaths: {df["Deaths"]}</p>', unsafe_allow_html=True)
st.sidebar.markdown(f'<p class="custom-text">Recovered: {df["Recovered"]}</p>', unsafe_allow_html=True)
st.sidebar.markdown(f'<p class="custom-text">Active: {df["Active"]}</p>', unsafe_allow_html=True)
st.sidebar.markdown(f'<p class="custom-text">Male: {df["Male"]}</p>', unsafe_allow_html=True)
st.sidebar.markdown(f'<p class="custom-text">Female: {df["Female"]}</p>', unsafe_allow_html=True)
st.sidebar.markdown(f'<p class="custom-text">Children: {df["Children"]}</p>', unsafe_allow_html=True)
st.set_option('deprecation.showPyplotGlobalUse', False)

st.header('Pie Chart for COVID-19 Cases')
cases_labels = ['Confirmed', 'Deaths', 'Recovered', 'Active']
cases_data = [df['Confirmed'], df['Deaths'], df['Recovered'], df['Active']]
fig = px.pie(values=cases_data, names=cases_labels, hole=0.5)
fig.update_traces(text=cases_labels, textposition="outside")
st.plotly_chart(fig)
st.subheader("Analysis")
container = st.container(border=True)
container.write("**Confirmed**")
container.write(f'<p class="custom-text"> {df["Confirmed"]}</p>', unsafe_allow_html=True)
col2_1, col2_2 = st.columns((2))
with col2_1:
    container2_1 = st.container(border=True)
    container2_1.write("**Death**")
    container2_1.write(f'<p class="custom-text"> {df["Deaths"]}</p>', unsafe_allow_html=True)
with col2_2:
    container2_2 = st.container(border=True)
    container2_2.write("**Recovered**")
    container2_2.write(f'<p class="custom-text"> {df["Recovered"]}</p>', unsafe_allow_html=True)
with col2_1:
    container2_1 = st.container(border=True)
    container2_1.write("**Active**")
    container2_1.write(f'<p class="custom-text">{df["Active"]}</p>', unsafe_allow_html=True)
with col2_2:
    container2_2 = st.container(border=True)
    container2_2.write("**New Cases**")
    container2_2.write(f'<p class="custom-text">{df["New cases"]}</p>', unsafe_allow_html=True)
with st.expander('Covid Details'):
    st.dataframe(data, use_container_width=True, hide_index=True)

csv = df.to_csv(index=False).encode('utf-8')
st.download_button('Download Covid Data', data=csv, file_name="country_wise_latest.csv")
