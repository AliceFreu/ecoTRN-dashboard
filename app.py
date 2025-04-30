import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# === Titel und Einleitung ===
st.set_page_config(page_title="ecoTRN Szenario Analyse", layout="centered")
st.title("ecoTRN Szenario-Analyse")

st.markdown("""
Willkommen bei unserer Szenario-Analyse für Trainingskosten! 👋

Hier können Sie Ihre aktuellen Trainingskosten mit klassischem Präsenztraining eingeben und mit unserer VR-Lösung von **ecoTRN** vergleichen.
Wir zeigen Ihnen auf einen Blick, wie viel Sie durch skalierbares, ortsunabhängiges Lernen mit Virtual Reality sparen können – sowohl **gesamt**, als auch **pro Teilnehmer:in**.

Bitte geben Sie Ihre Daten im linken Bereich ein – das Dashboard aktualisiert sich automatisch.
""")

# === Seitenleiste für Eingaben ===
st.sidebar.header("Deine Eingaben")

anzahl_teilnehmer = st.sidebar.number_input("Anzahl der Teilnehmer:innen", min_value=1, value=10)
schulungstage = st.sidebar.number_input("Anzahl Schulungstage (klassisch)", min_value=1, value=2)
tagessatz_trainer = st.sidebar.number_input("Tagessatz Trainer:in (EUR)", min_value=0.0, value=1000.0, step=100.0)
raumkosten_pro_tag = st.sidebar.number_input("Raumkosten pro Tag (EUR)", min_value=0.0, value=300.0, step=50.0)
reisekosten_pro_person = st.sidebar.number_input("Reisekosten pro Person (klassisch, EUR)", min_value=0.0, value=100.0, step=10.0)

kosten_headset = st.sidebar.number_input("Hardwarekosten VR-Headset (einmalig, EUR)", min_value=0.0, value=500.0, step=50.0)
monatliche_softwarelizenz = st.sidebar.number_input("Monatliche Lizenzkosten pro Headset (EUR)", min_value=0.0, value=65.0, step=5.0)
hosting_kosten_pro_monat = st.sidebar.number_input("Hostingkosten pauschal/Monat (optional, EUR)", min_value=0.0, value=50.0, step=10.0)
trainingsdauer_monate = st.sidebar.number_input("Trainingsdauer in Monaten (VR)", min_value=1, value=3)

# === Kalkulation Klassisch ===
klassisch_trainer = tagessatz_trainer * schulungstage
klassisch_raum = raumkosten_pro_tag * schulungstage
klassisch_reise = reisekosten_pro_person * anzahl_teilnehmer
klassisch_gesamt = (klassisch_trainer + klassisch_raum) + klassisch_reise

# === Kalkulation ecoTRN ===
hardware = kosten_headset * anzahl_teilnehmer
software = monatliche_softwarelizenz * anzahl_teilnehmer * trainingsdauer_monate
hosting = hosting_kosten_pro_monat * trainingsdauer_monate
ecotrn_gesamt = hardware + software + hosting

# === Ersparnis und Vergleich ===
ersparnis = klassisch_gesamt - ecotrn_gesamt

st.header("Ergebnisse im Vergleich")

col1, col2, col3 = st.columns(3)
col1.metric("Klassische Trainingskosten", f"{klassisch_gesamt:,.0f} EUR")
col2.metric("ecoTRN Kosten (VR)", f"{ecotrn_gesamt:,.0f} EUR")

if ersparnis > 0:
    col3.metric("Ersparnis", f"{ersparnis:,.0f} EUR", delta=f"{ersparnis / klassisch_gesamt * 100:.1f}%")
else:
    col3.metric("Mehrkosten", f"{-ersparnis:,.0f} EUR", delta=f"{-ersparnis / klassisch_gesamt * 100:.1f}%")

# === Visualisierung ===
kategorien = ['Klassisch', 'ecoTRN']
kosten = [klassisch_gesamt, ecotrn_gesamt]
fig, ax = plt.subplots()
ax.bar(kategorien, kosten)
ax.set_ylabel('Kosten in EUR')
ax.set_title('Kostenvergleich: Klassisch vs. ecoTRN')
st.pyplot(fig)

# === Footer ===
st.caption("Diese Analyse basiert auf typischen Annahmen für Trainingskosten. Alle Eingaben können individuell angepasst werden.\n\n© 2025 ecoTRN")


# Footer
st.caption("ecoTRN Scenario Analysis Dashboard - 2025")
