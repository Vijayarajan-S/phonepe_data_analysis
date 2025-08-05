import streamlit as st

st.set_page_config(page_title="PhonePe Home", page_icon="🏠", layout="centered")

st.title("📱 Welcome to the PhonePe Analytics Dashboard")
st.caption("Choose a dashboard page to explore various insights.")

# Buttons that navigate to other dashboard pages
st.title("Uncovering Transaction Trends & Growth Opportunities Across India")
st.caption("PhonePe operates in a competitive digital payments landscape. This dashboard decodes state-level transaction dynamics to uncover key trends, growth opportunities, and strategic expansion areas across India.")
st.page_link("pages/Transaction_Dashboard.py", label="Transaction Analysis for Market Expansion", icon="📳")
st.title("User Engagement Insights: PhonePe’s Strategy Across States and Districts")
st.caption("To strengthen its market presence, PhonePe analyzes user engagement across states and districts. By examining registered users and app opens, the platform gains actionable insights for strategic growth and user-centric decisions.")
st.page_link("pages/User_Dashboard.py", label=" User Engagement and Growth Strategy", icon="📈")
st.title("Decoding India’s Digital Payments Landscape")
st.caption("PhonePe uncovers key variations in transaction trends across states, quarters, and payment modes. By identifying growth and stagnation zones, the platform aims to unlock data-driven strategies for targeted business expansion.")
st.page_link("pages/Dynamics_Dashboard.py", label=" Decoding Transaction Dynamics on PhonePe", icon="🧠")
st.title(" Understanding User Behavior by Device Brand")
st.caption("Analyze how user engagement varies across device brands, regions, and time. Despite high registration numbers, certain brands show lower app open rates — highlighting opportunities for targeted performance improvements and user experience enhancements.")
st.page_link("pages/Device_Dashboard.py", label=" Device Dominance and User Engagement Analysis", icon="🗺️")
st.title(" Top-Performing Regions in Transaction Volume & Value")
st.caption("PhonePe is analyzing transaction data to uncover the highest-performing states, districts, and pin codes. This insight into user engagement helps identify growth hotspots and supports data-driven, targeted marketing strategies.")
st.page_link("pages/District_Pincode_Dashboard.py", label=" Transaction Analysis Across States and Districts", icon="📉")
