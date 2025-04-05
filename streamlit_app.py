import plotly.graph_objects as go
import pandas as pd
import streamlit as st

# Streamlit app title
st.title("Plotly Line Chart")

# Define the path to your CSV file
data_file = "data.csv"

# Attempt to load the CSV data
try:
    df = pd.read_csv(data_file)
except Exception as e:
    st.error(f"Error reading {data_file}: {e}")
    df = None

if df is not None:
    
    # Assuming the CSV has columns: 'Time', 'Series1', 'Series2', 'Series3'
    if {'Time', 'Series1', 'Series2', 'Series3'}.issubset(df.columns):
        # Create figure
        fig = go.Figure()
        
        # Add traces
        fig.add_trace(go.Scatter(x=df['Time'], y=df['Series1'], mode='lines', name='Series1'))
        fig.add_trace(go.Scatter(x=df['Time'], y=df['Series2'], mode='lines', name='Series2'))
        fig.add_trace(go.Scatter(x=df['Time'], y=df['Series3'], mode='lines', name='Series3'))
        
        # Customize layout
        fig.update_layout(
            title='Multiple Line Series Plot from CSV',
            xaxis_title='Time',
            yaxis_title='Value',
            template='plotly_dark',
            dragmode='pan',  # Enables panning
            xaxis=dict(rangeslider=dict(visible=True)),  # Enables zooming with range slider
        )
        
        # Display figure
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("CSV file must contain 'Time', 'Series1', 'Series2', and 'Series3' columns.")
