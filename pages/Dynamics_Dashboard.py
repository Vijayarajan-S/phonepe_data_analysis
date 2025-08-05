# 📦 Imports
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import requests

# 🌐 App Configuration
st.set_page_config(
    page_title="PhonePe Transaction Insights",
    page_icon="🪐",
    layout="wide"
)

# 📄 Load Transaction Data
agg_df = pd.read_csv('agg_trans_detail.csv')

# 📋 Utility Function to Display Tables
def display_table(data):
    return st.dataframe(data, use_container_width=True)

# 🧠 Main Function with Title and Filters
def main():
    st.title('📱 PhonePe Dashboard: Decoding Transaction Dynamics')
    st.caption('Visualizing transaction trends, growth patterns, and user engagement across India.')

    # Sidebar Filters
    trans_year = st.sidebar.multiselect('📆 Select Year(s)', agg_df['trans_year'].unique())
    quarter = st.sidebar.multiselect("🗓️ Select Quarter(s)", agg_df['quarter'].unique())
    category = st.sidebar.multiselect("💳 Select Mode(s) of Transaction", agg_df['mode_of_trans'].unique())

    # Filtered Data
    agg_df_select = agg_df[
        agg_df['trans_year'].isin(trans_year) &
        agg_df['quarter'].isin(quarter) &
        agg_df['mode_of_trans'].isin(category)
    ]

    st.subheader("📄 Filtered Transaction Data")
    display_table(agg_df_select)
    st.write('---')

if __name__ == "__main__":
    main()

# 📊 Function to Classify States by Transaction Volume
def overall_growth(agg_df):
    category = st.sidebar.multiselect("Select Transaction Mode for State Classification", agg_df['mode_of_trans'].unique())

    if not category:
        st.warning("⚠️ Please select at least one transaction mode.")
        return pd.DataFrame()

    filtered_df = agg_df[agg_df['mode_of_trans'].isin(category)]

    # Sum transaction count per state
    total_transcount = filtered_df.groupby('state_name')['trans_count'].sum()

    # Average transaction count
    avg_transaction = total_transcount.mean()

    # Classification Logic
    def classify(trans):
        if trans > avg_transaction:
            return 'HIGH'
        elif trans < avg_transaction * 0.5:
            return 'LOW'
        else:
            return 'POTENTIAL'

    result = total_transcount.reset_index(name='trans_count')
    result['category'] = result['trans_count'].apply(classify)
    result = result.sort_values(by='trans_count', ascending=False)

    return result

# 🧭 Get Classified State-wise Growth Data
potential_area = overall_growth(agg_df)

# 🧾 Display Tables for Classified Data
if not potential_area.empty:
    st.subheader("📊 Summary Table by State")
    st.dataframe(potential_area, use_container_width=True)

    st.subheader("🧮 Descriptive Statistics")
    st.dataframe(potential_area.describe().T.round(2))

    st.subheader("🌟 Potential Growth Areas")
    st.dataframe(potential_area[potential_area['category'] == 'POTENTIAL'])

# 🗺️ Choropleth Map of App Engagement by State
st.subheader("🗺️ State-wise App Engagement Map")

try:
    geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    india_states = requests.get(geojson_url).json()
except Exception as e:
    st.error(f"Failed to load India state map: {e}")
    st.stop()

classified_df = potential_area.copy()
classified_df['state_name'] = classified_df['state_name'].str.title().str.strip()
classified_df['category'] = classified_df['category'].str.title()

# Add open_per_user as dummy metric for color mapping if not available
if 'open_per_user' not in classified_df.columns:
    classified_df['open_per_user'] = classified_df['trans_count'] / classified_df['trans_count'].mean()

color_map = {'Low': 0, 'Potential': 1, 'High': 2}
classified_df['category_value'] = classified_df['category'].map(color_map)

# 🌐 Choropleth Plot
fig = go.Figure(go.Choropleth(
    geojson=india_states,
    featureidkey='properties.ST_NM',
    locations=classified_df['state_name'],
    z=classified_df['category_value'],
    locationmode='geojson-id',
    colorscale=[[0, '#d9f0a3'], [0.5, '#78c679'], [1.0, '#238443']],
    colorbar=dict(
        title="Category",
        tickvals=[0, 1, 2],
        ticktext=['Low', 'Potential', 'High']
    ),
    customdata=classified_df[['category', 'trans_count']],
    hovertemplate="<b>%{location}</b><br>" +
                  "Category: %{customdata[0]}<br>" +
                  "Transaction Count: %{customdata[1]:,.0f}<extra></extra>"
))

fig.update_geos(
    visible=False,
    projection=dict(
        type='conic conformal',
        parallels=[12.4729, 35.1728],
        rotation={'lat': 24, 'lon': 80}
    ),
    lonaxis=dict(range=[68, 98]),
    lataxis=dict(range=[6, 38])
)

fig.update_layout(
    title=dict(text="📍 App Engagement Categories by State", x=0.5),
    margin=dict(r=0, t=30, l=0, b=0),
    height=750,
    width=850
)

st.plotly_chart(fig, use_container_width=True)

# 📈 Line Chart for User Growth Over Time
st.subheader("📈 Registered User Growth Over Time")

user_growth = agg_df.groupby(['trans_year', 'quarter'])['reg_user'].sum().reset_index()
user_growth['Year_Quarter'] = user_growth['trans_year'].astype(str) + " Q" + user_growth['quarter'].astype(str)

fig_line = px.line(
    user_growth.sort_values(by=['trans_year', 'quarter']),
    x='Year_Quarter',
    y='reg_user',
    title="User Registration Trend (Quarter-wise)",
    labels={'reg_user': 'Registered Users', 'Year_Quarter': 'Time'},
    markers=True
)

st.plotly_chart(fig_line, use_container_width=True)
