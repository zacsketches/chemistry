import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import requests
import os

# Inject custom CSS to move the Plotly chart controls to the bottom
st.markdown("""
    <style>
        /* Move the modebar (zoom, fullscreen, etc.) to the bottom */
        .plotly .modebar-container {
            position: absolute !important;
            bottom: 10px !important;
            top: auto !important;
        }
    </style>
""", unsafe_allow_html=True)

# Inject custom CSS for the header
st.markdown("""
    <style>
        /* Change the Streamlit header top border color */
  
        /* Remove the default top padding/margin */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 1rem !important;
        }

        /* Optional: Adjust header style to remove unnecessary space */
        .css-1v3fvcr {
            margin-top: 0rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit app title (with custom font size)
# st.markdown("<h3 style='text-align: left; color: black;'>Water Chemistry</h3>", unsafe_allow_html=True)

# Get the API URL from the environment variable
data_url = os.getenv("READINGS_API")

# Attempt to fetch the JSON data from the URL
if data_url:
    try:
        response = requests.get(data_url)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        readings = data["readings"]

        # Convert the JSON data into a Pandas DataFrame
        df = pd.DataFrame(readings)
        
        # Convert 'testDate' to a datetime format for plotting
        df['testDate'] = pd.to_datetime(df['testDate'])

    except requests.exceptions.RequestException as e:
        # If the API call fails, show a message on the chart
        df = None
        error_message = f"Error fetching data from the API: {e}"
else:
    # If the environment variable is not set, show a message on the chart
    df = None
    error_message = "READINGS_API environment variable not set or API unreachable."

if df is not None:
    # Create a single Plotly figure for all the lines (Chlorine, pH, Acid Demand, Total Alkalinity)
    fig = go.Figure()

    # Add Chlorine trace
    fig.add_trace(go.Scatter(x=df['testDate'], y=df['chlorine'], mode='lines', name='Chlorine'))

    # Add pH trace
    fig.add_trace(go.Scatter(x=df['testDate'], y=df['ph'], mode='lines', name='pH'))

    # Add Acid Demand trace
    fig.add_trace(go.Scatter(x=df['testDate'], y=df['acidDemand'], mode='lines', name='Acid Demand'))

    # Add Total Alkalinity trace
    fig.add_trace(go.Scatter(x=df['testDate'], y=df['totalAlkalinity'], mode='lines', name='Total Alkalinity'))

    # Update layout of the plot with interactivity features and compact design
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Value',
        template='plotly_dark',
        dragmode='pan',  # Enables panning
        xaxis=dict(
            rangeslider=dict(visible=True),  # Enables zooming with range slider
            showspikes=True  # Adds spikes when hovering over the chart
        ),
        yaxis=dict(
            showspikes=True  # Adds spikes when hovering over the chart
        ),
        hovermode='closest',  # Ensures hover displays information close to the cursor
        margin=dict(l=40, r=40, t=40, b=40),  # Reduced margins for a more compact chart
        font=dict(
            size=10  # Smaller font size for axis labels, title, and legend
        ),
        legend=dict(
            orientation='h',  # Horizontally align the legend
            yanchor='bottom', 
            y=1.02,  # Place the legend just above the plot
            xanchor='center', 
            x=0.5
        )
    )

    # Display the figure
    st.plotly_chart(fig)
else:
    # If data is unavailable, display an error message on the chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode='text',
        text=[error_message],
        textposition='middle center',
        showlegend=False
    ))

    # Update layout to show error message prominently
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        template='plotly_dark',
        margin=dict(l=40, r=40, t=40, b=40),  # Reduced margins
    )

    # Display the error figure
    st.plotly_chart(fig)
