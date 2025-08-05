import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import requests

# Page config
st.set_page_config(page_title="PhonePe Analytics Dashboard", page_icon="📗", layout="wide")

# Load data
user_df = pd.read_csv('user_data.csv')

# -------------------- Display Helper --------------------
def disply_table(data):
    st.dataframe(data, use_container_width=True)

# -------------------- MAIN DASHBOARD --------------------
def main():
    st.title("📈 PhonePe User Analytics Dashboard")
    st.subheader("Analyze User Growth, App Opens, and Identify Potential States for Business Expansion")

    year = st.sidebar.multiselect(
        '📅 Select Year',
        sorted(user_df['user_year'].unique()),
        default=[2019]
    )

    state_name = st.sidebar.multiselect(
        '📍 Select State(s)',
        sorted(user_df['state_name'].unique()),
        default=[user_df['state_name'].iloc[1]]
    )

    user_df_select = user_df[
        user_df['user_year'].isin(year) &
        user_df['state_name'].isin(state_name)
    ]

    st.write("### 🔍 Filtered User Data")
    with st.expander("📄 Show Filtered User Table"):
        disply_table(user_df_select)
    st.write('---')

# -------------------- MAX USER PER QUARTER --------------------
def max_user_every_year_quarter(df):
    st.subheader("🚀 Top Performing States by Quarter & Year (Maximum Registered Users)")

    df = df.copy()
    df['user_year'] = df['user_year'].astype(str)
    df['quarter'] = df['quarter'].astype(str)

    if df.empty:
        st.warning("⚠️ No data available for the selected filters.")
        return

    idx = df.groupby(['user_year', 'quarter'])['reguser'].idxmax()
    max_user = df.loc[idx].sort_values(by=['user_year', 'quarter'])

    with st.expander("📄 Show Max Registered Users Table"):
        disply_table(max_user)

    fig = px.bar(
        max_user,
        x='user_year',
        y='reguser',
        color='quarter',
        hover_data=["state_name"],
        title='📈 Top States by Registered Users (2018–2024)'
    )
    st.plotly_chart(fig, use_container_width=True)

# -------------------- MIN USER PER QUARTER --------------------
def min_user_every_year_quarter(df):
    st.subheader("📉 Least Performing States by Quarter & Year (Minimum Registered Users)")

    df = df.copy()
    df['user_year'] = df['user_year'].astype(str)
    df['quarter'] = df['quarter'].astype(str)

    if df.empty:
        st.warning("⚠️ No data available for the selected filters.")
        return

    idx = df.groupby(['user_year', 'quarter'])['reguser'].idxmin()
    min_user = df.loc[idx].sort_values(by=['user_year', 'quarter'])

    with st.expander("📄 Show Min Registered Users Table"):
        disply_table(min_user)

    fig = px.scatter(
        min_user,
        x="user_year",
        y="reguser",
        color='quarter',
        hover_data=["state_name"],
        title='📉 States with Minimum Registered Users (2018–2024)',
        labels={"user_year": "Year", "reguser": "Registered Users"}
    )
    st.plotly_chart(fig, use_container_width=True)

# -------------------- USER GROWTH LINE CHART --------------------
def user_growth_over_time(df):
    st.subheader("📊 Year-wise Growth of Registered Users (2018–2024)")

    df = df.copy()
    df['user_year'] = df['user_year'].astype(str)
    growth_df = df.groupby('user_year')['reguser'].sum().reset_index()

    fig = px.line(
        growth_df,
        x='user_year',
        y='reguser',
        markers=True,
        title='📈 User Registration Growth Over the Years',
        labels={'user_year': 'Year', 'reguser': 'Total Registered Users'}
    )

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📄 Show Yearly Growth Table"):
        st.dataframe(growth_df, use_container_width=True)

# -------------------- POTENTIAL AREA --------------------
def potential_area(df):
    st.subheader("📍 Potential Business Areas Based on App Engagement")

    grouped = df.groupby('state_name').agg({
        'appopens': 'sum',
        'reguser': 'sum'
    }).reset_index()

    grouped['open_per_user'] = round(grouped['appopens'] / grouped['reguser'])
    avg_open = grouped['open_per_user'].mean()

    def classify(row):
        if row['open_per_user'] >= avg_open:
            return 'High'
        elif row['open_per_user'] >= avg_open * 0.5:
            return 'Potential'
        else:
            return 'Low'

    grouped['category'] = grouped.apply(classify, axis=1)

    with st.expander("📄 Show Potential Classification Table"):
        st.dataframe(grouped, use_container_width=True)

    return grouped

# -------------------- CHOROPLETH --------------------
def plot_choropleth(classified_df):
    st.subheader("🗺️ App Engagement Level by State (Choropleth Map)")

    geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    india_states = requests.get(geojson_url).json()

    classified_df['state_name'] = classified_df['state_name'].str.title().str.strip()
    classified_df['category'] = classified_df['category'].str.title()
    color_map = {'High': 2, 'Potential': 1, 'Low': 0}
    classified_df['category_value'] = classified_df['category'].map(color_map)

    fig = go.Figure(go.Choropleth(
        geojson=india_states,
        featureidkey='properties.ST_NM',
        locations=classified_df['state_name'],
        locationmode='geojson-id',
        z=classified_df['category_value'],
        colorscale=[[0, '#D8BFD8'], [0.5, '#BA55D3'], [1.0, '#4B0082']],
        colorbar=dict(title="Category", tickvals=[0, 1, 2], ticktext=['Low', 'Potential', 'High']),
        customdata=classified_df[['category', 'open_per_user']],
        hovertemplate="<b>%{location}</b><br>" +
                      "Category: %{customdata[0]}<br>" +
                      "App Opens per User: %{customdata[1]:.2f}<extra></extra>"
    ))

    fig.update_geos(
        visible=False,
        projection=dict(type='conic conformal', parallels=[12.4729, 35.1728], rotation={'lat': 24, 'lon': 80}),
        lonaxis={'range': [68, 98]},
        lataxis={'range': [6, 38]}
    )

    fig.update_layout(
        title=dict(text="State-wise App Engagement Category", x=0.5),
        margin=dict(r=0, t=30, l=0, b=0),
        height=750,
        width=850
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------- APP FLOW --------------------
if __name__ == "__main__":
    main()
    max_user_every_year_quarter(user_df)
    min_user_every_year_quarter(user_df)
    user_growth_over_time(user_df)
    classified_df = potential_area(user_df)
    plot_choropleth(classified_df)
