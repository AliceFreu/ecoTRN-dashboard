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

Here you can input your current training costs for traditional in-person programs and compare them to our VR-based training solution at **ecoTRN**.
We show you at a glance how much you can save with scalable, location-independent Virtual Reality learning – both **in total** and **per trainee**.

This tool is designed for institutions, ministries, and NGOs looking for scalable training solutions in the renewable energy sector.
""",
        "inputs": "Your Inputs",
        "participants": "Number of learners per year",
        "days": "Number of training days (traditional)",
        "trainer": "Trainer daily rate (€)",
        "room": "Room cost per day (€)",
        "travel": "Travel cost per person (€)",
        "hardware": "VR headset cost (one-time, €)",
        "license": "Monthly license cost per headset (€)",
        "hosting": "Hosting cost per month (optional, €)",
        "duration": "VR training duration (months)",
        "years": "Evaluation period (years)",
        "group_size": "Learners per traditional training group",
        "results": "Results Comparison",
        "total_classic": "Total Traditional Cost",
        "total_vr": "Total VR Cost",
        "savings": "Savings over {years} Years",
        "cost_per_learner": "Cost per Learner (Total)",
        "chart_title1": "Cumulative Training Cost (ROI View)",
        "chart_title2": "Annual Training Costs Comparison - {anzahl} Learners/Year",
        "footer": "This analysis is based on standard training cost assumptions and simulates ROI at scale."
    },
    "Deutsch": {
        "title": "ecoTRN Szenario-Analyse",
        "intro": """
Willkommen bei unserer Szenario-Analyse für Trainingskosten! 👋

Hier können Sie Ihre aktuellen Trainingskosten mit klassischem Präsenztraining eingeben und mit unserer VR-Lösung von **ecoTRN** vergleichen.
Wir zeigen Ihnen auf einen Blick, wie viel Sie durch skalierbares, ortsunabhängiges Lernen mit Virtual Reality sparen können – sowohl **gesamt**, als auch **pro Teilnehmer:in**.

Diese Analyse richtet sich an Bildungseinrichtungen, Ministerien oder NGOs, die skalierbare Lösungen zur Aus- und Weiterbildung im Bereich erneuerbarer Energien benötigen.
""",
        "inputs": "Deine Eingaben",
        "participants": "Anzahl der Teilnehmer:innen pro Jahr",
        "days": "Anzahl Schulungstage (klassisch)",
        "trainer": "Tagessatz Trainer:in (EUR)",
        "room": "Raumkosten pro Tag (EUR)",
        "travel": "Reisekosten pro Person (EUR)",
        "hardware": "Hardwarekosten VR-Headset (einmalig, EUR)",
        "license": "Monatliche Lizenzkosten pro Headset (EUR)",
        "hosting": "Hostingkosten pro Monat (optional, EUR)",
        "duration": "Trainingsdauer in Monaten (VR)",
        "years": "Betrachtungszeitraum (Jahre)",
        "group_size": "Teilnehmer:innen pro Schulungsgruppe (klassisch)",
        "results": "Ergebnisse im Vergleich",
        "total_classic": "Gesamtkosten Klassisch",
        "total_vr": "Gesamtkosten VR",
        "savings": "Ersparnis in {years} Jahren",
        "cost_per_learner": "Kosten pro Teilnehmer:in (Gesamt)",
        "chart_title1": "Kumulative Trainingskosten (ROI-Sicht)",
        "chart_title2": "Jährlicher Kostenvergleich - {anzahl} Lernende/Jahr",
        "footer": "Diese Analyse basiert auf typischen Annahmen für Trainingskosten und simuliert ROI bei skalierter Nutzung."
    }
}

T = text[language]

# === Page title and intro ===
st.title(T["title"])
st.markdown(T["intro"])

# === Sidebar inputs ===
st.sidebar.header(T["inputs"])
num_learners = st.sidebar.number_input(T["participants"], min_value=1, value=100)
training_days = st.sidebar.number_input(T["days"], min_value=1, value=2)
trainer_rate = st.sidebar.number_input(T["trainer"], min_value=0.0, value=1000.0)
room_cost = st.sidebar.number_input(T["room"], min_value=0.0, value=300.0)
travel_cost = st.sidebar.number_input(T["travel"], min_value=0.0, value=100.0)

headset_cost = st.sidebar.number_input(T["hardware"], min_value=0.0, value=500.0)
monthly_license = st.sidebar.number_input(T["license"], min_value=0.0, value=65.0)
monthly_hosting = st.sidebar.number_input(T["hosting"], min_value=0.0, value=50.0)
vr_duration = st.sidebar.number_input(T["duration"], min_value=1, value=3)
evaluation_years = st.sidebar.number_input(T["years"], min_value=1, value=5)
group_size = st.sidebar.number_input(T["group_size"], min_value=1, value=10)

# === Cost calculations ===
num_groups = math.ceil(num_learners / group_size)
classic_annual_cost = ((trainer_rate + room_cost) * training_days * num_groups) + (travel_cost * num_learners)
classic_cumulative = [classic_annual_cost * (i + 1) for i in range(evaluation_years)]

hardware_total = headset_cost * num_learners
license_annual = monthly_license * num_learners * vr_duration
hosting_annual = monthly_hosting * vr_duration
vr_annual = license_annual + hosting_annual

# VR cumulative cost with hardware only in year 1
vr_cumulative = []
for i in range(1, evaluation_years + 1):
    if i == 1:
        total = hardware_total + vr_annual
    else:
        total = vr_cumulative[-1] + vr_annual
    vr_cumulative.append(total)

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
vr_annual_series = [hardware_total + vr_annual] + [vr_annual] * (evaluation_years - 1)
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
