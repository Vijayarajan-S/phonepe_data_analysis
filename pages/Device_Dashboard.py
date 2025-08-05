# ------------------------- #
# 📦 Import Required Libraries
# ------------------------- #
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import requests
import seaborn as sns

# ------------------------- #
# ⚙️ Streamlit Page Configuration
# ------------------------- #
st.set_page_config(
    page_title="PhonePe Device Dashboard",
    page_icon="📳",
    layout="wide"
)

# ------------------------- #
# 📥 Load Data
# ------------------------- #
device_df = pd.read_csv('device_usage.csv')

# ------------------------- #
# 🏷️ Page Title
# ------------------------- #
st.title('📱 Device Dominance and User Engagement Analysis')

# ------------------------- #
# 📋 Display Data Table Helper Function
# ------------------------- #
def display_table(data):
    return st.dataframe(data, use_container_width=True)

# ------------------------- #
# 🧠 Main Filter Function with Sidebar Inputs
# ------------------------- #
def main():
    # Sidebar Filters for Year, Quarter, and Brand
    year = st.sidebar.multiselect(
        'Select Year to Filter Data',
        device_df['trans_year'].unique()
    )
    
    quarter = st.sidebar.multiselect(
        'Select Quarter to Filter Data',
        device_df['quarter'].unique()
    )
    
    mobile_category = st.sidebar.multiselect(
        'Select Mobile Brand(s)',
        device_df['brand'].unique()
    )

    # Filter data based on user selections
    device_df_select = device_df[
        device_df['trans_year'].isin(year) &
        device_df['quarter'].isin(quarter) &
        device_df['brand'].isin(mobile_category)
    ]

    # Display Filtered Data Table
    display_table(device_df_select)
    st.write('---')

# Execute the main filtering section
if __name__ == "__main__":
    main()

# ------------------------- #
# 📊 Function: Max Registered Users by Brand and State
# ------------------------- #
def max_device_state(device_df):
    st.subheader('📊 Max Registered Users by Brand in Each State and Year')

    # Get index of row with maximum users per state and year
    idx = device_df.groupby(['state_name', 'trans_year'])['reg_user'].idxmax()
    max_user_device = device_df.loc[idx].sort_values(by='reg_user', ascending=False)

    # Display the max user device data
    st.dataframe(max_user_device, use_container_width=True)

    # Bar Chart Visualization
    st.subheader("States by Max Brand Users (per Year)")
    fig = px.bar(
        max_user_device,
        x='state_name',
        y='reg_user',
        color='brand',
        hover_data=['trans_year'],
        title='Top States and Their Most Popular Device Brands (per Year)',
        labels={'reg_user': 'Registered Users', 'state_name': 'State'}
    )
    st.plotly_chart(fig, use_container_width=True)

    return max_user_device

# Call the function and store result
max_use_device = max_device_state(device_df)

# ------------------------- #
# 📶 Function: Device Count per State for Selected Brands
# ------------------------- #
def mobile_wise_data(device_df):
    # 📱 Sidebar filter for brand selection
    mobile_category = st.sidebar.multiselect("Select Brand(s) for Device Usage", device_df['brand'].unique())

    if not mobile_category:
        st.warning("Please select at least one brand.")
        return pd.DataFrame()

    # 🎯 Filter and aggregate by state
    filtered_df = device_df[device_df['brand'].isin(mobile_category)]
    total_users = filtered_df.groupby('state_name')['reg_user'].sum()
    result = total_users.reset_index().sort_values(by='reg_user', ascending=False)

    return result

# 🚀 Display mobile-wise data
mobile_cat = mobile_wise_data(device_df)
with st.expander("🔍 View Table To See Data"):
 st.dataframe(mobile_cat, use_container_width=True)

# 📊 Bar Plot: Registered Users by State for Selected Brands
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=mobile_cat, x="state_name", y="reg_user", ax=ax)

# ✅ Add x and y labels
ax.set_xlabel("State", fontsize=12)
ax.set_ylabel("Registered Users", fontsize=12)

plt.xticks(rotation=90)
plt.title("📊 Registered Users by State for Selected Mobile Brands")
st.pyplot(fig)

# ------------------------- #
# 🌐 Function: Brand Distribution for Selected State(s)
# ------------------------- #
def state_wise_data(device_df):
    # Sidebar Filter for states
    state_name_data = st.sidebar.multiselect("Select State(s) to View Brand Share", device_df['state_name'].unique())

    if not state_name_data:
        st.warning("Please select at least one state.")
        return pd.DataFrame()

    # Filter and aggregate
    filtered_df = device_df[device_df['state_name'].isin(state_name_data)]
    mobile_data = filtered_df.groupby('brand')['count'].sum()
    result = mobile_data.reset_index().sort_values(by='count', ascending=False)

    return result

# Call and display state-wise brand data
state_cat = state_wise_data(device_df)
with st.expander("🔍 View Table To See Data"):
  st.dataframe(state_cat, use_container_width=True)

# 🍩 Donut Chart for Device Brand Share by Selected States
labels = state_cat['brand']
values = state_cat['count']

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    hole=0.4,  # Donut hole
    textinfo='label+percent',
    hoverinfo='label+value'
)])

fig.update_layout(
    title_text="📱 Device Brand Share by Selected State(s)",
    height=500,
    width=600
)

st.plotly_chart(fig)
