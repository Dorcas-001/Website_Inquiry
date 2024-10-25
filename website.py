import streamlit as st
import matplotlib.colors as mcolors
import plotly.express as px
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from itertools import chain
from matplotlib.ticker import FuncFormatter



st.set_page_config(
    page_title="Eden Care Inquiries View",
    page_icon=Image.open("EC_logoo.png"),
    layout="wide",
    initial_sidebar_state="expanded"
)

# Centered and styled main title using inline styles
st.markdown('''
    <style>
        .main-title {
            color: #e66c37; /* Title color */
            text-align: center; /* Center align the title */
            font-size: 3rem; /* Title font size */
            font-weight: bold; /* Title font weight */
            margin-bottom: .5rem; /* Space below the title */
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1); /* Subtle text shadow */
        }
        div.block-container {
            padding-top: 2rem; /* Padding for main content */
        }
    </style>
''', unsafe_allow_html=True)

logo_url = 'EC_logo.png'  
st.sidebar.image(logo_url, use_column_width=True)


st.markdown('<h1 class="main-title">Eden Care Website Inquiries</h1>', unsafe_allow_html=True)

filepath="export (1).csv"

# Read all sheets into a dictionary of DataFrames
df = pd.read_csv(filepath, encoding="ISO-8859-1")



# Ensure the 'Start Date' column is in datetime format if needed
df["Start Date"] = pd.to_datetime(df["Query date"], errors='coerce')

# Get minimum and maximum dates for the date input
startDate = df["Start Date"].min()
endDate = df["Start Date"].max()

# Define CSS for the styled date input boxes
st.markdown("""
    <style>
    .date-input-box {
        border-radius: 10px;
        text-align: left;
        margin: 5px;
        font-size: 1.2em;
        font-weight: bold;
    }
    .date-input-title {
        font-size: 1.2em;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)


# Create 2-column layout for date inputs
col1, col2 = st.columns(2)

# Function to display date input in styled boxes
def display_date_input(col, title, default_date, min_date, max_date):
    col.markdown(f"""
        <div class="date-input-box">
            <div class="date-input-title">{title}</div>
        </div>
        """, unsafe_allow_html=True)
    return col.date_input("", default_date, min_value=min_date, max_value=max_date)

# Display date inputs
with col1:
    date1 = pd.to_datetime(display_date_input(col1, "Start Date", startDate, startDate, endDate))

with col2:
    date2 = pd.to_datetime(display_date_input(col2, "End Date", endDate, startDate, endDate))

# Filter DataFrame based on the selected dates
df = df[(df["Start Date"] >= date1) & (df["Start Date"] <= date2)].copy()


# Sidebar styling and logo
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .sidebar .sidebar-content h3 {
        color: #007BFF; /* Change this color to your preferred title color */
        font-size: 1.5em;
        margin-bottom: 20px;
        text-align: center;
    }
    .sidebar .sidebar-content .filter-title {
        color: #e66c37;
        font-size: 1.2em;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
        text-align: center;
    }
    .sidebar .sidebar-content .filter-header {
        color: #e66c37; /* Change this color to your preferred header color */
        font-size: 2.5em;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 20px;
        text-align: center;
    }
    .sidebar .sidebar-content .filter-multiselect {
        margin-bottom: 15px;
    }
    .sidebar .sidebar-content .logo {
        text-align: center;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content .logo img {
        max-width: 80%;
        height: auto;
        border-radius: 50%;
    }
            
    </style>
    """, unsafe_allow_html=True)




# Extract month numbers
df["Start Month Number"] = df["Start Date"].dt.month

# Dictionary with numerical month values as keys
month_order = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
}

# Map month numbers to month names
df["Start Month"] = df["Start Month Number"].map(month_order)

# Sort unique month names based on their numerical order
sorted_month_numbers = sorted(df['Start Month Number'].dropna().unique())
sorted_month_names = [month_order[month] for month in sorted_month_numbers]
# Sidebar for filters
st.sidebar.header("Filters")

month = st.sidebar.multiselect("Select Month", options=sorted_month_names)
form = st.sidebar.multiselect("Select Form Type", options=df['Form type'].unique())
product = st.sidebar.multiselect("Select Product", options=df['Products'].unique())
inquiry = st.sidebar.multiselect("Select Reason For Inquiry", options=df['Reason for inquiry'].unique())



if month:
    df = df[df['Start Month'].isin(month)]
if form:
    df = df[df['Form type'].isin(form)]
if product:
    df = df[df['ProductS'].isin(product)]
if inquiry:
    df = df[df['Reason for inquiry'].isin(inquiry)]


df_new = df[df['Products'] == 'Health Insurance and ProActiv Package']
df_renew = df[df['Products'] == 'Health Insurance Only Package']
df_proactiv = df[df['Products'] == 'ProActiv Only Package']

if not df.empty:  

    total_inq = len(df)
    inq_health = len(df_renew)
    inq_combined = len(df_new)
    inq_proactiv = len(df_proactiv)

    # Create 4-column layout for metric cards
    col1, col2, col3, col4 = st.columns(4)

    # Define CSS for the styled boxes
    st.markdown("""
        <style>
        .custom-subheader {
            color: #e66c37;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
            padding: 5px;
            border-radius: 5px;
            display: inline-block;
        }
        .metric-box {
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            margin: 10px;
            font-size: 1.2em;
            font-weight: bold;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            border: 1px solid #ddd;
        }
        .metric-title {
            color: #e66c37; /* Change this color to your preferred title color */
            font-size: 0.9em;
            margin-bottom: 10px;
        }
        .metric-value {
            color: #009DAE;
            font-size: 1.2em;
        }
        </style>
        """, unsafe_allow_html=True)

    # Function to display metrics in styled boxes
    def display_metric(col, title, value):
        col.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    display_metric(col1, "Total Inquiries", total_inq)
    display_metric(col2, "Inquiries For Health Insurance", inq_health)
    display_metric(col3, "Inquiries For ProActiv", inq_proactiv)
    display_metric(col4, "Inquiries For Health Insurance and ProActiv", inq_combined)



   
    # Sidebar styling and logo
    st.markdown("""
        <style>
        .sidebar .sidebar-content {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .sidebar .sidebar-content h2 {
            color: #007BFF; /* Change this color to your preferred title color */
            font-size: 1.5em;
            margin-bottom: 20px;
            text-align: center;
        }
        .sidebar .sidebar-content .filter-title {
            color: #e66c37;
            font-size: 1.2em;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 10px;
            text-align: center;
        }
        .sidebar .sidebar-content .filter-header {
            color: #e66c37; /* Change this color to your preferred header color */
            font-size: 2.5em;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 20px;
            text-align: center;
        }
        .sidebar .sidebar-content .filter-multiselect {
            margin-bottom: 15px;
        }
        .sidebar .sidebar-content .logo {
            text-align: center;
            margin-bottom: 20px;
        }
        .sidebar .sidebar-content .logo img {
            max-width: 80%;
            height: auto;
            border-radius: 50%;
        }
                
        </style>
        """, unsafe_allow_html=True)

    custom_colors = ["#009DAE", "#e66c37", "#461b09", "#f8a785", "#CC3636"]

    cols1, cols2 = st.columns(2)

    with cols1:
        st.markdown('<h2 class="custom-subheader">Number of Inquiries Over Time</h2>', unsafe_allow_html=True)
        # Group data by day and count visits
        daily_visits = df.groupby(df['Start Date'].dt.to_period('D')).size()
        daily_visits.index = daily_visits.index.to_timestamp()

        # Create a DataFrame for the daily visits
        daily_visits_df = daily_visits.reset_index()
        daily_visits_df.columns = ['Day', 'Number of Inquiries']

        # Create area chart for visits per day
        fig_area = go.Figure()

        fig_area.add_trace(go.Scatter(
            x=daily_visits_df['Day'],
            y=daily_visits_df['Number of Inquiries'],
            fill='tozeroy',
            mode='lines',
            marker=dict(color='#009DAE'),
            line=dict(color='#009DAE'),
            name='Number of Visits'
        ))

        fig_area.update_layout(
            xaxis_title="Days of the Month",
            yaxis_title="Number of Inquiries",
            font=dict(color='black'),
            width=1200,  # Adjust width as needed
            height=600   # Adjust height as needed
        )

        # Display the plot
        st.plotly_chart(fig_area, use_container_width=True)


    # Count the occurrences of each Status
    coverage_counts = df["Start Month"].value_counts().reset_index()
    coverage_counts.columns = ["Month", "Count"]

    with cols2:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Monthly Distribution Of Inquiries</h3>', unsafe_allow_html=True)

        # Create a bar chart
        fig = px.bar(coverage_counts, x="Month", y="Count", text="Count", template="plotly_white", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textfont=dict(color='white'))
        fig.update_layout(
            xaxis_title="Form Type",
            yaxis_title="Number of Inquiries",
            height=450,
            margin=dict(l=0, r=10, t=30, b=50)
        )

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    # Create the layout columns
    cls1, cls2 = st.columns(2)

    coverage_counts = df.groupby("Start Month")["Products"].value_counts().reset_index()
    coverage_counts.columns = ["Month", "Product", "Count"]

    with cls1:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Monthly Inquiries Distribution by Product</h3>', unsafe_allow_html=True)

        # Create a bar chart
        fig = px.bar(coverage_counts, x="Month", y="Count", color="Product", text="Count", template="plotly_white",color_discrete_sequence=custom_colors, barmode="group")
        fig.update_traces(textposition='inside', textfont=dict(color='white'))
        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Number of Inquiries",
            height=450,
            margin=dict(l=0, r=10, t=30, b=50)
        )

        # Display the Number of Inquiries chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)



 # Calculate the Total Premium by Client Segment
    int_owner = df["Products"].value_counts().reset_index()
    int_owner.columns = ["Product", "Count"]    

    with cls2:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Total Inquiries by Product</h3>', unsafe_allow_html=True)


        # Create a donut chart
        fig = px.pie(int_owner, names="Product", values="Count", hole=0.5, template="plotly_dark", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    # Create the layout columns
    cls1, cls2 = st.columns(2)

    # Count the occurrences of each Status
    coverage_counts = df["Reason for inquiry"].value_counts().reset_index()
    coverage_counts.columns = ["Reason", "Count"]

    with cls1:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Reason For Inquiry</h3>', unsafe_allow_html=True)

        # Create a bar chart
        fig = px.bar(coverage_counts, x="Reason", y="Count", text="Count", template="plotly_white", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textfont=dict(color='white'))
        fig.update_layout(
            xaxis_title="Reason For Inquiry",
            yaxis_title="Number of Inquiries",
            height=450,
            margin=dict(l=0, r=10, t=30, b=50)
        )

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    # Count the occurrences of each Status
    coverage_counts = df["Form type"].value_counts().reset_index()
    coverage_counts.columns = ["Form", "Count"]

    with cls2:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Inquiries By Form Type</h3>', unsafe_allow_html=True)

        # Create a bar chart
        fig = px.bar(coverage_counts, x="Form", y="Count", text="Count", template="plotly_white", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textfont=dict(color='white'))
        fig.update_layout(
            xaxis_title="Form Type",
            yaxis_title="Number of Inquiries",
            height=450,
            margin=dict(l=0, r=10, t=30, b=50)
        )

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)


