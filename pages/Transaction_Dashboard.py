# 📦 Required libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# 🛠️ Streamlit page configuration
st.set_page_config(page_title="PhonePe", page_icon="🧊", layout="wide")

# 📥 Load the dataset
pt_df = pd.read_csv("phonepe_trasaction.csv")

# 🧾 Utility function to display a DataFrame
def disply_table(data):
    st.dataframe(data, use_container_width=True)

# 🧠 Main filter UI
def main():
    st.title("**Transaction Analysis for Strategic Market Expansion**")

    # Sidebar filters: Year, Quarter, and State
    year = st.sidebar.multiselect(
        'Select Year',
        pt_df['trans_year'].unique(),
        default=[2019]
    )
    quarter = st.sidebar.multiselect(
        'Select Quarter',
        pt_df['quarter'].unique(),
        default=[1]
    )
    state_name = st.sidebar.multiselect(
        'Select State Name',
        pt_df['state_name'].unique(),
        default=pt_df['state_name'][1]
    )

    # Filter data based on sidebar selections
    pt_df_select = pt_df[
        pt_df['trans_year'].isin(year) &
        pt_df['quarter'].isin(quarter) &
        pt_df['state_name'].isin(state_name)
    ]

    # Display filtered data
    disply_table(pt_df_select)
    st.write('---')

# Run the main UI section
if __name__ == "__main__":
    main()

# 📊 Max transaction per year-quarter across all states
def max_trans_every_year_quarter(pt_df):
    st.title("📈 Maximum Transaction per Quarter and Year (by District)")
    
    pt_df['trans_year'] = pt_df['trans_year'].astype(str)
    pt_df['quarter'] = pt_df['quarter'].astype(str)

    # Find index of max transaction for each year-quarter group
    idx = pt_df.groupby(['trans_year', 'quarter'])['transaction_count'].idxmax()
    
    max_trans = pt_df.loc[idx].sort_values(by=['trans_year', 'quarter'])
    return max_trans

max_trans_year_quarter = max_trans_every_year_quarter(pt_df)
with st.expander("📄 Show Maximum Transaction Data Table"):
    st.dataframe(max_trans_year_quarter, use_container_width=True)

# 📈 Line chart of maximum transaction counts
fig1 = px.line(
    max_trans_year_quarter,
    x='trans_year',
    y='transaction_count',
    color='district',
    markers=True,
    title="Maximum Transaction Data (2018–2024)"
)
fig1.update_layout(
    xaxis_title="Year",
    yaxis_title="Transaction Count",
    legend_title="District",
    template="simple_white"
)
st.plotly_chart(fig1)

# 📉 Minimum transaction per year-quarter across all states
def min_trans_every_year_quarter(pt_df):
    st.title("📉 Minimum Transaction per Quarter and Year (by District)")
    
    pt_df['trans_year'] = pt_df['trans_year'].astype(str)
    pt_df['quarter'] = pt_df['quarter'].astype(str)

    idx = pt_df.groupby(['trans_year', 'quarter'])['transaction_count'].idxmin()
    
    min_trans = pt_df.loc[idx].sort_values(by=['trans_year', 'quarter'])
    return min_trans

min_trans_year_quarter = min_trans_every_year_quarter(pt_df)
with st.expander("📄 Show Minimum Transaction Data Table"):
    st.dataframe(min_trans_year_quarter, use_container_width=True)

# 🟣 Scatter chart for minimum transactions
min_trans_year_quarter['tooltip_info'] = (
    min_trans_year_quarter['district'] + " | Count: " +
    min_trans_year_quarter['transaction_count'].astype(str)
)

fig2 = px.scatter(
    min_trans_year_quarter,
    x="trans_year",
    y="quarter",
    color='district',
    hover_name='tooltip_info',
    title='Minimum Transaction Data (2018–2024)',
    labels={"trans_year": "Year", "quarter": "Quarter"}
)
st.plotly_chart(fig2, use_container_width=True)

# 🔍 Classify districts based on transaction potential
def pontential_area(pt_df):
    pt_df['transaction_count'] = pd.to_numeric(pt_df['transaction_count'], errors='coerce')

    # Total transactions by district
    total_transcount = pt_df.groupby(['state_name', 'district'])['transaction_count'].sum()

    # Calculate average transaction across all districts
    avg_transaction = total_transcount.mean()

    # Classify based on thresholds
    def classify(trans):
        if trans > avg_transaction:
            return 'HIGH'
        elif trans < avg_transaction * 0.5:
            return 'LOW'
        else:
            return 'PONTENTIAL'

    result = total_transcount.reset_index()
    result['category'] = result['transaction_count'].apply(classify)
    result = result.sort_values(by='transaction_count', ascending=False)
    return result

find_potential = pontential_area(pt_df)

# 🎯 State-wise potential area selection
state_potential = st.sidebar.multiselect(
    'Select State(s) to View District Potential',
    find_potential['state_name'].unique()
)

# Filter potential results based on selected states
find_tential = find_potential[find_potential['state_name'].isin(state_potential)]
disply_table(find_tential)
st.write('---')

# 📊 Plot potential areas for each selected state
if not find_tential.empty:
    for state in state_potential:
        st.subheader(f"🗺️ District-wise Potential in {state}")
        state_df = find_tential[find_tential['state_name'] == state]

        fig = px.bar(
            state_df,
            x='district',
            y='transaction_count',
            color='category',
            title=f"Transaction Potential by District in {state}",
            labels={'transaction_count': 'Transaction Count', 'district': 'District'},
            color_discrete_map={'HIGH': 'green', 'PONTENTIAL': 'orange', 'LOW': 'red'}
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Please select at least one state to display potential chart.")

st.write('---')
