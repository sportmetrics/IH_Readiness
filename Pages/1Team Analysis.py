import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(layout="wide")

# Function to load all data (cached)
@st.cache_data
def load_data():
    list_test_data = pd.DataFrame()
    list_test_data = pd.read_csv('Sources/merged_df.csv')
    return list_test_data

# Load Data
data = load_data()

st.markdown("# Team Analysis")
st.sidebar.image('Images/tigers.png')
st.sidebar.subheader("Latest Team Statistics")
st.sidebar.write("Average Weight: " +
                 str(round(data[data["Date"] == data["Date"].max()]["Weight"].mean(), 2)) + " kg")
st.sidebar.write("Average Size: " +
                 str(round(data[data["Date"] == data["Date"].max()]["Size"].mean(), 2)) + " cm")

team_perspective = st.selectbox(
            "Choose the perspective",
            ["Overall", "Speed", "Strength", "Endurance",
             "Fullbody-Strength", "Shoulder-Strength", "Hip-Strength"])
absVals = st.toggle("Use absolute Values for graphs")
seasons = ['All'] + data['Season'].unique().tolist()
selection = st.segmented_control(
    "Seasons", seasons, selection_mode="multi", default="All")

if "All" in selection:
    filtered_data = data  # No filtering, show all data
else:
    filtered_data = data[data['Season'].isin(selection)]  # Filter by selected seasons

col1, col2 = st.columns([2,2])
if team_perspective == "Overall":
    with col1:
        # Define the indices to visualize
        left_indices = {
            'Speed Index': 'Speed_index',
            'Endurance Index': 'Endurance_index',
            'Shoulder Strength Index': 'Shoulder_index',
        }

        # Loop through each index and generate corresponding bar chart
        for index_name, column_name in left_indices.items():

            if not filtered_data.empty and column_name in filtered_data.columns:

                filtered_data = filtered_data.dropna(subset=[column_name])
                sort_order = [True, False]  # Sort by date ascending, then value descending

                top_players_per_date = (
                    filtered_data.sort_values(['Date', column_name], ascending=sort_order)
                    .groupby('Date')
                    .head(3)
                )

                team_average_per_date = (
                    filtered_data.groupby('Date')[column_name].mean().reset_index()
                )

                if not top_players_per_date.empty:
                    fig = px.bar(
                        top_players_per_date,
                        x='Date',
                        y=column_name,
                        color='Name',
                        barmode='group',
                        title=f"Top 3 Players by {index_name} ({'All Seasons' if selection == 'Overall' else ', '.join(selection)})"
                    )

                    fig.update_layout(
                        bargap=0.0,
                        bargroupgap=0.0
                    )

                    # Add the red line for team average
                    fig.add_trace(
                        go.Scatter(
                            x=team_average_per_date['Date'],
                            y=team_average_per_date[column_name],
                            mode='lines+markers',
                            name='Team Average',
                            line=dict(color='orange', width=2, dash='dash')
                        )
                    )

                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.write(f"No data available for {index_name} in the selected season(s).")
            else:
                st.write(f"No data available for {index_name}.")
    with col2:
        right_indices = {
            'Power Index': 'power_index',
            'IMTP Strength Index': 'IMTP_index',
            'Hip Strength Index': 'Hip_index'
        }

        # Loop through each index and generate corresponding bar chart
        for index_name, column_name in right_indices.items():

            if not filtered_data.empty and column_name in filtered_data.columns:
                top_players_per_date = (
                    filtered_data.sort_values(['Date', column_name], ascending=[True, False])
                    .groupby('Date')
                    .head(3)
                )

                if not top_players_per_date.empty:

                    fig = px.bar(
                        top_players_per_date,
                        x='Date',
                        y=column_name,
                        color='Name',
                        barmode='group',
                        title=f"Top 3 Players by {index_name} ({'All Seasons' if selection == 'Overall' else ', '.join(selection)})"
                    )

                    fig.update_layout(
                        bargap=0.0,
                        bargroupgap=0.0
                    )

                    team_average_per_date = (
                        filtered_data.groupby('Date')[column_name].mean().reset_index()
                    )

                    # Add the red line for team average
                    fig.add_trace(
                        go.Scatter(
                            x=team_average_per_date['Date'],
                            y=team_average_per_date[column_name],
                            mode='lines+markers',
                            name='Team Average',
                            line=dict(color='orange', width=2, dash='dash')
                        )
                    )

                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.write(f"No data available for {index_name} in the selected season(s).")
            else:
                st.write(f"No data available for {index_name}.")
# Define the mapping of team perspectives to their corresponding columns
team_perspective_columns = {
    "Speed": {
        "left": {
            '10m Sprint (Off)': '10m Off',
            '30m Sprint (Off)': '30m Off',
        },
        "right": {
            '20m Sprint (Off)': '20m Off',
            '5-10-5 Drill': '5_10_5'
        }
    },
    "Strength": {
        "left": {
            'CMJ W/kg': 'CMJ W/kg',
            'SL CMJ L': 'SL CMJ L',
        },
        "right": {
            'SJ W/kg': 'SJ W/kg',
            'SL CMJ R': 'SL CMJ R'
        }
    },
    "Endurance": {
        "left": {
            'WG Ppeak': 'WG Ppeak',
            '3min MMP': '3min MMP',
        },
        "right": {
            'WGPpeak W/kg': 'WGPpeak W/kg',
            '3min W/kg': '3min W/kg',
            'WG Pavg W/kg': 'WG Pavg W/kg'
        }
    },
    "Fullbody-Strength": {
        "left": {
            'IMTP': 'IMTP',
        },
        "right": {}  # No right columns for this perspective
    },
    "Hip-Strength": {
        "left": {
            'AD Mx F 60 L': 'AD Mx F 60 L',
            'AB Mx F 60 L': 'AB Mx F 60 L',
        },
        "right": {
            'AD Mx F 60 R': 'AD Mx F 60 R',
            'AB Mx F 60 R': 'AB Mx F 60 R'
        }
    },
    "Shoulder-Strength": {
        "left": {
            'SH Int L': 'SH Int L',
            'SH Ext L': 'SH Ext L',
        },
        "right": {
            'SH Int R': 'SH Int R',
            'SH Ext R': 'SH Ext R'
        }
    }
}

# Get the selected columns based on team_perspective
selected_columns = team_perspective_columns.get(team_perspective, {"left": {}, "right": {}})


# Function to generate charts
def generate_charts(column_dict, column_position):
    for metric_name, column_name in column_dict.items():
        # Check if absolute values or index values should be used
        display_column = f"{column_name}_index" if not absVals else column_name
        display_metric_name = f"{metric_name} Index" if not absVals else metric_name

        if not filtered_data.empty and display_column in filtered_data.columns:

            #filtered_data = filtered_data.dropna(subset=[column_name])
            if team_perspective  == 'Speed' and absVals:
                sort_order = [True, True]  # Sort by date ascending, then value ascending
            else:
                sort_order = [True, False]  # Sort by date ascending, then value descending
            # Get top 3 players by metric for each date
            top_players_per_date = (
                filtered_data.sort_values(['Date', display_column], ascending=sort_order)
                .groupby('Date')
                .head(3)
            )

            # Calculate team average for each date
            team_average_per_date = (
                filtered_data.groupby('Date')[display_column].mean().reset_index()
            )

            if not top_players_per_date.empty:

                # Create the bar chart for top performers
                fig = px.bar(
                    top_players_per_date,
                    x='Date',
                    y=display_column,
                    color='Name',
                    barmode='group',
                    title=f"Top 3 Performers in {display_metric_name} ({'All Seasons' if selection == 'Overall' else ', '.join(selection)})"
                )

                fig.update_layout(
                    bargap=0.0,
                    bargroupgap=0.0
                )

                # Add red dashed line for team average
                fig.add_trace(
                    go.Scatter(
                        x=team_average_per_date['Date'],
                        y=team_average_per_date[display_column],
                        mode='lines+markers',
                        name='Team Average',
                        line=dict(color='orange', width=2, dash='dash')
                    )
                )



                # Display the chart with a unique key
                st.plotly_chart(fig, use_container_width=True,
                                key=f"{display_column}_{column_position}_chart")
            else:
                st.write(f"No data available for {display_metric_name} in the selected season(s).")
        else:
            st.write(f"No data available for {display_metric_name}.")


# Display charts for the left column
with col1:
    generate_charts(selected_columns["left"], "left")

# Display charts for the right column
with col2:
    generate_charts(selected_columns["right"], "right")