import streamlit as st
import pandas as pd

# Backend Stuff
#st.set_page_config(layout="wide")
@st.cache_data
def load_players_data(players):
    player_data = load_data()
    player_data = player_data[player_data['Name'].isin(players)]
    player_data = player_data.loc[player_data.groupby('Name')['Date'].idxmax()]
    return player_data

@st.cache_data
def load_data():
    list_test_data = pd.DataFrame()
    list_test_data = pd.read_csv('Sources/merged_df.csv')
    return list_test_data

def read_groups():
    data_list = pd.read_csv('Sources/groups.csv').squeeze()
    return data_list


data = load_data()

distPlayers = data["Name"].dropna().unique().tolist()
#distPlayers.extend(["Defenders", "Attackers", "Goalkeepers", "Line 1", "Line 2", "Line 3", "Line 4"])
# Frontend Stuff
st.markdown("# Lineup Configuration")

col1, col2 = st.columns([2,5], border=True)

with (col1):
    edit_group = st.text_input("Group name")
    groups = read_groups()
    try:
        if st.button("Create new group"):
            if edit_group in groups.values:
                st.error("Group already exists or has invalid name (no alphanumeric characters)")
            else:
                with st.status("Group successfully created"):
                    groups = pd.concat([groups, pd.Series([edit_group])], ignore_index=True)
                    groups.to_csv('Sources/groups.csv', index=False)

    except:
        st.error("Group creation failed")
    try:
        if st.button("Delete group"):
            if edit_group not in groups.values:
                st.error("Group doesn't exist and can't be deleted")
            else:
                with st.status("Group successfully deleted"):
                    groups = groups[groups != edit_group]
                    groups.to_csv('Sources/groups.csv', index=False)
    except:
        st.error("Group can't be deleted")
with col2:
    selectedplayers = st.multiselect(
        "Choose the players to configure",
        distPlayers
    )


    if not selectedplayers:
        st.error("No players selected")
    else:
        compData = load_players_data(selectedplayers)
        assignableGroups = read_groups()
        line = st.selectbox(
            "Choose the group",
            assignableGroups
        )
        try:
            if st.button("Assign selected players to group"):
                with st.status("Group successfully assigned"):
                    data.loc[data['Name'].isin(selectedplayers), 'assignedLine'] = line
                    data.to_csv('Sources/merged_df.csv', index=False)
                    load_data.clear()
                    load_players_data.clear()

        except:
            st.error("Players can't be assigned to group")

        try:
            if st.button("Delete assigned line for selected players"):
                with st.status("Group successfully assigned"):
                    data.loc[data['Name'].isin(selectedplayers), 'assignedLine'] = None
                    data.to_csv('Sources/merged_df.csv', index=False)
                    load_data.clear()
                    load_players_data.clear()
        except:
            st.error("Players can't be unassigned from group")
