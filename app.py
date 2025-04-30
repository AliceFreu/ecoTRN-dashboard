import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

st.set_page_config(page_title="ecoTRN Scenario Analysis", layout="centered")

# === Language selection ===
language = st.sidebar.selectbox("Language", ["English", "Deutsch"])

# === Translations ===
text = {
    "English": {
        "title": "ecoTRN Scenario Analysis",
        "intro": """
Welcome to our training cost scenario analysis! 👋

This tool allows you to compare the cost of traditional in-person training with our VR-based solution for renewable energy technicians.

Please start by selecting one of the following options:

### 📦 License Only
- Access to **existing VR modules** (e.g., solar installation)
- **Annual license per headset: €300**
- **No development or update costs**

### 🛠️ Custom Development
- We develop a **tailored VR training module** for your needs
- **One-time content development: €45,000**
- **Annual update & maintenance: €10,000**
- **Annual license per headset: €200**

This selection will influence the calculation below.
""",
        "inputs": "Your Inputs",
        "participants": "Number of learners per year",
        "days": "Number of training days (traditional)",
        "trainer": "Trainer daily rate (€)",
        "room": "Room cost per day (€)",
        "travel": "Travel cost per person (€)",
        "hardware": "VR headset cost (€)",
        "utilization": "Learners per headset per year",
        "consumables": "Consumables per learner (traditional, €)",
        "years": "Evaluation period (years)",
        "group_size": "Learners per traditional training group",
        "content_option": "Select your training model:",
        "develop": "Custom development by ecoTRN",
        "license": "License existing module",
        "results": "Results Comparison",
        "total_classic": "Total Traditional Cost",
        "total_vr": "Total VR Cost",
        "savings": "Savings over {years} Years",
        "cost_per_learner": "Cost per Learner (Total)",
        "npv_label": "Net Present Value (NPV) of VR",
        "payback_label": "Payback Year",
        "chart_title1": "Cumulative Training Cost (ROI View)",
        "chart_title2": "Annual Training Costs Comparison - {anzahl} Learners/Year",
        "footer": "This analysis is based on standard training cost assumptions and simulates ROI at scale."
    }
}

T = text[language]

# === Fixed Parameters ===
headset_lifespan = 5
vr_license_only = 300
vr_license_custom = 200
vr_content_cost = 45000
vr_update_cost = 10000
discount_rate = 0.05

# === Page title and intro ===
st.title(T["title"])
intro_paragraph = T["intro"].split("Please start by selecting")[0]
st.markdown(intro_paragraph)
content_mode = st.sidebar.radio(T["content_option"], [T["develop"], T["license"]])
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    ### 🛠️ Custom Development
    - Tailored VR module just for your needs
    - One-time content development: **€45,000**
    - Annual update & maintenance: **€10,000**
    - License per headset/year: **€200**
    """)
with col2:
    st.markdown("""
    ### 📦 License Only
    - Access to existing VR modules (e.g., solar)
    - No dev or update fees
    - License per headset/year: **€300**
    """)

st.markdown("---")

# === Sidebar inputs ===
st.sidebar.header(T["inputs"])
num_learners = st.sidebar.number_input(T["participants"], min_value=1, value=100)
training_days = st.sidebar.number_input(T["days"], min_value=1, value=2)
trainer_rate = st.sidebar.number_input(T["trainer"], min_value=0.0, value=300.0)
room_cost = st.sidebar.number_input(T["room"], min_value=0.0, value=200.0)
travel_cost = st.sidebar.number_input(T["travel"], min_value=0.0, value=100.0)

headset_cost = st.sidebar.number_input(T["hardware"], min_value=0.0, value=500.0)
learners_per_headset = st.sidebar.number_input(T["utilization"], min_value=1, value=5)
consumables = st.sidebar.number_input(T["consumables"], min_value=0.0, value=70.0)
evaluation_years = st.sidebar.number_input(T["years"], min_value=1, value=5)
group_size = st.sidebar.number_input(T["group_size"], min_value=1, value=15)

# === Assign cost values based on content mode ===
if content_mode == T["develop"]:
    vr_license = vr_license_custom
    vr_content = vr_content_cost
    vr_update = vr_update_cost
else:
    vr_license = vr_license_only
    vr_content = 0
    vr_update = 0

# === Traditional training cost calculation ===
num_groups = math.ceil(num_learners / group_size)
classic_annual_cost = ((trainer_rate + room_cost) * training_days * num_groups) + (travel_cost * num_learners) + (consumables * num_learners)
classic_cumulative = [classic_annual_cost * (i + 1) for i in range(evaluation_years)]

# === VR training cost calculation ===
headsets_needed = math.ceil(num_learners / learners_per_headset)
total_headset_cost = headset_cost * headsets_needed
annual_headset_cost = total_headset_cost / headset_lifespan
vr_license_cost_total = vr_license * headsets_needed
vr_annual = annual_headset_cost + vr_license_cost_total + vr_update

vr_annual_series = [vr_content + vr_annual] + [vr_annual] * (evaluation_years - 1)
vr_cumulative = [sum(vr_annual_series[:i + 1]) for i in range(evaluation_years)]

# === NPV and Payback calculation ===
npv_vr = sum(v / (1 + discount_rate) ** (i + 1) for i, v in enumerate(vr_annual_series))
payback_year = next((i + 1 for i, (vc, tc) in enumerate(zip(vr_cumulative, classic_cumulative)) if vc < tc), None)

# === Results ===
st.header(T["results"])

total_classic = classic_cumulative[-1]
total_vr = vr_cumulative[-1]
savings = total_classic - total_vr

col1, col2, col3 = st.columns(3)
col1.metric(T["total_classic"], f"{total_classic:,.0f} EUR")
col2.metric(T["total_vr"], f"{total_vr:,.0f} EUR")
col3.metric(T["savings"].format(years=evaluation_years), f"{savings:,.0f} EUR", delta=f"{savings / total_classic * 100:.1f}%")

st.markdown(f"**{T['cost_per_learner']}:**")
st.markdown(f"- Traditional: {total_classic / (num_learners * evaluation_years):,.0f} EUR")
st.markdown(f"- VR: {total_vr / (num_learners * evaluation_years):,.0f} EUR")

st.markdown(f"**{T['npv_label']}:** {npv_vr:,.0f} EUR")
if payback_year:
    st.markdown(f"**{T['payback_label']}:** Year {payback_year}")

# === Plot 1: Cumulative cost comparison ===
years = list(range(1, evaluation_years + 1))
fig1, ax1 = plt.subplots()
ax1.plot(years, vr_cumulative, label='Cumulative VR Cost (€)', color='green')
ax1.plot(years, classic_cumulative, label='Cumulative Traditional Cost (€)', color='blue')
ax1.set_xlabel('Year')
ax1.set_ylabel('Cumulative Cost (€)')
ax1.set_title(T["chart_title1"])
ax1.legend()
st.pyplot(fig1)

# === Plot 2: Annual cost comparison ===
x = np.arange(evaluation_years)
bar_width = 0.4
fig2, ax2 = plt.subplots()
ax2.bar(x, [classic_annual_cost] * evaluation_years, label='Traditional Costs (€)', color='blue', width=bar_width)
ax2.bar(x + bar_width, vr_annual_series, label='VR Costs (€)', color='green', width=bar_width)
ax2.set_xticks(x + bar_width / 2)
ax2.set_xticklabels([str(y) for y in years])
ax2.set_xlabel('Year')
ax2.set_ylabel('Cost (€)')
ax2.set_title(T["chart_title2"].format(anzahl=num_learners))
ax2.legend()
st.pyplot(fig2)

# === Footer ===
st.caption(T["footer"] + "\n\n© 2025 ecoTRN")
