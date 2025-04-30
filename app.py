import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="ecoTRN Scenario Analysis", layout="centered")

# === Spracheinstellung ===
language = st.sidebar.selectbox("Sprache / Language", ["Deutsch", "English"])

# === Übersetzungen ===
text = {
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
        "travel": "Reisekosten pro Person (klassisch, EUR)",
        "hardware": "Hardwarekosten VR-Headset (einmalig, EUR)",
        "license": "Monatliche Lizenzkosten pro Headset (EUR)",
        "hosting": "Hostingkosten pauschal/Monat (optional, EUR)",
        "duration": "Trainingsdauer in Monaten (VR)",
        "years": "Betrachtungszeitraum (Jahre)",
        "results": "Ergebnisse im Vergleich",
        "total_classic": "Gesamtkosten Klassisch",
        "total_vr": "Gesamtkosten VR",
        "savings": "Ersparnis in {years} Jahren",
        "chart_title1": "Kumulative Trainingskosten (ROI-Sicht)",
        "chart_title2": "Jährlicher Kostenvergleich - {anzahl} Lernende/Jahr",
        "footer": "Diese Analyse basiert auf typischen Annahmen für Trainingskosten und simuliert ROI bei skalierter Nutzung."
    },
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
        "results": "Results Comparison",
        "total_classic": "Total Traditional Cost",
        "total_vr": "Total VR Cost",
        "savings": "Savings over {years} Years",
        "chart_title1": "Cumulative Training Cost (ROI View)",
        "chart_title2": "Annual Training Costs Comparison - {anzahl} Learners/Year",
        "footer": "This analysis is based on standard training cost assumptions and simulates ROI at scale."
    }
}

T = text[language]  # shortcut

# === App Titel und Einleitung ===
st.title(T["title"])
st.markdown(T["intro"])

# === Seitenleiste für Eingaben ===
st.sidebar.header(T["inputs"])
anzahl_teilnehmer = st.sidebar.number_input(T["participants"], min_value=1, value=100)
schulungstage = st.sidebar.number_input(T["days"], min_value=1, value=2)
tagessatz_trainer = st.sidebar.number_input(T["trainer"], min_value=0.0, value=1000.0, step=100.0)
raumkosten_pro_tag = st.sidebar.number_input(T["room"], min_value=0.0, value=300.0, step=50.0)
reisekosten_pro_person = st.sidebar.number_input(T["travel"], min_value=0.0, value=100.0, step=10.0)

kosten_headset = st.sidebar.number_input(T["hardware"], min_value=0.0, value=500.0, step=50.0)
monatliche_softwarelizenz = st.sidebar.number_input(T["license"], min_value=0.0, value=65.0, step=5.0)
hosting_kosten_pro_monat = st.sidebar.number_input(T["hosting"], min_value=0.0, value=50.0, step=10.0)
trainingsdauer_monate = st.sidebar.number_input(T["duration"], min_value=1, value=3)
laufzeit_jahre = st.sidebar.number_input(T["years"], min_value=1, value=5)

# === Kalkulation ===
klassisch_jährlich = ((tagessatz_trainer + raumkosten_pro_tag) * schulungstage) + (reisekosten_pro_person * anzahl_teilnehmer)
klassisch_kumuliert = [klassisch_jährlich * (i+1) for i in range(laufzeit_jahre)]

hardware_kosten = kosten_headset * anzahl_teilnehmer
lizenz_kosten_jährlich = monatliche_softwarelizenz * anzahl_teilnehmer * 12
hosting_kosten_jährlich = hosting_kosten_pro_monat * 12
vr_jährlich = lizenz_kosten_jährlich + hosting_kosten_jährlich
vr_kumuliert = [hardware_kosten + vr_jährlich * i for i in range(1, laufzeit_jahre + 1)]

# === Ergebnisse ===
st.header(T["results"])

total_klassisch = klassisch_kumuliert[-1]
total_vr = vr_kumuliert[-1]
ersparnis_total = total_klassisch - total_vr

col1, col2, col3 = st.columns(3)
col1.metric(T["total_classic"], f"{total_klassisch:,.0f} EUR")
col2.metric(T["total_vr"], f"{total_vr:,.0f} EUR")
col3.metric(T["savings"].format(years=laufzeit_jahre), f"{ersparnis_total:,.0f} EUR", delta=f"{ersparnis_total / total_klassisch * 100:.1f}%")

# === Diagramm: Kumulierte Kostenentwicklung ===
jahre = list(range(1, laufzeit_jahre + 1))
fig1, ax1 = plt.subplots()
ax1.plot(jahre, vr_kumuliert, label='Cumulative VR Cost (€)')
ax1.plot(jahre, klassisch_kumuliert, label='Cumulative Traditional Cost (€)')
ax1.set_xlabel('Year')
ax1.set_ylabel('Cumulative Cost (€)')
ax1.set_title(T["chart_title1"])
ax1.legend()
st.pyplot(fig1)

# === Diagramm: Jährliche Kostenvergleich ===
fig2, ax2 = plt.subplots()
ax2.bar(jahre, [klassisch_jährlich]*laufzeit_jahre, label='Traditional Costs (€)')
ax2.bar(jahre, [vr_jährlich]*laufzeit_jahre, label='VR Costs (€)', width=0.5)
ax2.set_xlabel('Year')
ax2.set_ylabel('Cost (€)')
ax2.set_title(T["chart_title2"].format(anzahl=anzahl_teilnehmer))
ax2.legend()
st.pyplot(fig2)

# === Footer ===
st.caption(T["footer"] + "\n\n© 2025 ecoTRN")
