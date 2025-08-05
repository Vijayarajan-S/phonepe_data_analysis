import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="PhonePe Analytics Dashboard", page_icon="📊", layout="wide")

# Load data
district_df = pd.read_csv("district_data.csv")
pincode_df = pd.read_csv("pincode_data.csv")

# Title
st.title("📱 PhonePe Dashboard: Decoding Transaction Dynamics")
st.caption("Visualizing transaction trends, growth patterns, and user engagement across India.")

# ------------------------------------------
# SECTION: District-Level Dashboard
# ------------------------------------------
st.sidebar.header("🔎 District-Level Filters")
trans_year = st.sidebar.multiselect("📆 Select Year(s)", sorted(district_df['trans_year'].unique()), key='district_year')
quarter = st.sidebar.multiselect("🗓️ Select Quarter(s)", sorted(district_df['quarter'].unique()), key='district_quarter')
state_name = st.sidebar.multiselect("🏙️ Select State(s)", sorted(district_df['state_name'].unique()), key='district_state')

if trans_year and quarter and state_name:
    filter_df = district_df[
        (district_df['trans_year'].isin(trans_year)) &
        (district_df['quarter'].isin(quarter)) &
        (district_df['state_name'].isin(state_name))
    ]

    st.subheader("📄 Filtered District-Level Transaction Data")
    st.dataframe(filter_df, use_container_width=True)
    st.write("---")

    # Transaction count by district
    st.subheader("📊 Total Transaction Count by District")
    district_plot = filter_df.groupby('district')['transaction_count'].sum().reset_index()
    fig1 = px.bar(
        district_plot,
        x='district',
        y='transaction_count',
        title='Total Transaction Count by District',
        labels={'transaction_count': 'Transaction Count', 'district': 'District'}
    )
    fig1.update_layout(xaxis_tickangle=90)
    st.plotly_chart(fig1, use_container_width=True)

else:
    st.warning("⚠️ Please select Year, Quarter, and State to view district-level data.")

# Function to find district with max transaction per state
def max_transaction_district(df):
    grouped = df.groupby(['state_name', 'district'])['transaction_amount'].sum().reset_index()
    max_trans_df = grouped.loc[grouped.groupby('state_name')['transaction_amount'].idxmax()].reset_index(drop=True)
    return max_trans_df.sort_values(by='transaction_amount', ascending=False)

# Max transaction districts
st.subheader("🏆 Districts with Maximum Transaction Amount in Each State")
max_dis = max_transaction_district(district_df)
st.dataframe(max_dis, use_container_width=True)

fig2 = px.bar(
    max_dis,
    x='district',
    y='transaction_amount',
    color='state_name',
    title='Top Transaction Districts by State',
    labels={'transaction_amount': 'Transaction Amount', 'district': 'District'},
    height=500
)
fig2.update_layout(xaxis_tickangle=45)
st.plotly_chart(fig2, use_container_width=True)

# Yearly trend by state
st.subheader("📈 Yearly Transaction Trend by State")
yearly_trend = district_df.groupby(['trans_year', 'state_name'])['transaction_amount'].sum().reset_index()
fig3 = px.line(
    yearly_trend,
    x='trans_year',
    y='transaction_amount',
    color='state_name',
    title='Year-wise Transaction Trend by State'
)
st.plotly_chart(fig3, use_container_width=True)

df_heatmap = pd.pivot_table(
    pincode_df,
    values='transaction_count',
    index='state_name',
    columns='trans_year',
    aggfunc='sum'
)

fig_heatmap = px.imshow(
    df_heatmap,
    labels=dict(x="Year", y="State", color="Transaction count"),
    title="Heatmap: Yearly Transactions by State",
    aspect="auto",
    color_continuous_scale="Viridis"
)

st.plotly_chart(fig_heatmap, use_container_width=True)
# ------------------------------------------
# SECTION: Pincode-Level Dashboard
# ------------------------------------------
st.sidebar.header("🔎 Pincode-Level Filters")
trans_year1 = st.sidebar.multiselect("📆 Select Year(s)", sorted(pincode_df['trans_year'].unique()), key='pincode_year')
quarter1 = st.sidebar.multiselect("🗓️ Select Quarter(s)", sorted(pincode_df['quarter'].unique()), key='pincode_quarter')
state_name1 = st.sidebar.multiselect("🏙️ Select State(s)", sorted(pincode_df['state_name'].unique()), key='pincode_state')

if trans_year1 and quarter1 and state_name1:
    filter_df_pin = pincode_df[
        (pincode_df['trans_year'].isin(trans_year1)) &
        (pincode_df['quarter'].isin(quarter1)) &
        (pincode_df['state_name'].isin(state_name1))
    ]

    st.subheader("📄 Filtered Pincode-Level Transaction Data")
    st.dataframe(filter_df_pin, use_container_width=True)
    st.write("---")
else:
    st.warning("⚠️ Please select Year, Quarter, and State to view pincode-level data.")

pincode_df['pincode'] =pincode_df['pincode'].astype(str)

def max_transaction_pincode(df):
    grouped = df.groupby(['state_name', 'pincode'])['transaction_count'].sum().reset_index()
    max_trans_df = grouped.loc[grouped.groupby('state_name')['transaction_count'].idxmax()].reset_index(drop=True)
    return max_trans_df.sort_values(by='transaction_count', ascending=False)

# Max transaction pincode
st.subheader("🏆 Pincode with Maximum Transaction Amount in Each State")
max_pin = max_transaction_pincode(pincode_df)
st.dataframe(max_pin, use_container_width=True)

fig5= px.bar(
    max_pin,
    x='pincode',
    y='transaction_count',
    color='state_name',
    title='Top Transaction Districts by State',
    labels={'transaction_count': 'Transaction Count', 'pincode': 'Pincode'},
    height=500
)
fig5.update_layout(xaxis_tickangle=45)
st.plotly_chart(fig5, use_container_width=True)

# Yearly trend by state
st.subheader("📈 Yearly Transaction Trend by State")
yearly_trend = pincode_df.groupby(['trans_year', 'state_name','pincode'])['transaction_count'].sum().reset_index()
fig4 = px.line(
    yearly_trend,
    x='trans_year',
    y='transaction_count',
    color='state_name',hover_data='pincode',
    title='Year-wise Transaction Trend by State'
)
st.plotly_chart(fig4, use_container_width=True)

