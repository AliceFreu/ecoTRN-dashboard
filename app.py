import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Titel und Einleitung
st.title("ecoTRN Scenario Analysis")
st.subheader("Vergleiche die Kosten von klassischem Training vs. ecoTRN VR-Training")

# Eingabefelder für Nutzer
st.sidebar.header("Deine Eingaben")

anzahl_teilnehmer = st.sidebar.number_input("Anzahl der Teilnehmer", min_value=1, value=10)
kosten_klassisch_pro_person = st.sidebar.number_input("Kosten klassisches Training pro Person (EUR)", min_value=0.0, value=2500.0, step=100.0)

kosten_headset = st.sidebar.number_input("Hardwarekosten VR-Headset (einmalig pro Headset)", min_value=0.0, value=500.0, step=50.0)
monatliche_softwarelizenz = st.sidebar.number_input("Monatliche Lizenzkosten pro Headset (EUR)", min_value=0.0, value=65.0, step=5.0)
trainingsdauer_monate = st.sidebar.number_input("Trainingsdauer (Monate)", min_value=1, value=3)

# Kostenberechnung
klassische_gesamtkosten = anzahl_teilnehmer * kosten_klassisch_pro_person

# Annahme: ein Headset pro Teilnehmer
hardware_gesamtkosten = anzahl_teilnehmer * kosten_headset
software_gesamtkosten = anzahl_teilnehmer * monatliche_softwarelizenz * trainingsdauer_monate

ecotrn_gesamtkosten = hardware_gesamtkosten + software_gesamtkosten

# Ersparnis
ersparnis = klassische_gesamtkosten - ecotrn_gesamtkosten

# Ergebnisse anzeigen
st.header("Ergebnisse")

st.metric("Kosten klassisches Training", f"{klassische_gesamtkosten:,.0f} EUR")
st.metric("Kosten ecoTRN Training", f"{ecotrn_gesamtkosten:,.0f} EUR")

if ersparnis > 0:
    st.success(f"Ersparnis: {ersparnis:,.0f} EUR")
else:
    st.error(f"ecoTRN verursacht Mehrkosten von {-ersparnis:,.0f} EUR")

# Grafische Darstellung
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
kategorien = ['Klassisch', 'ecoTRN']
kosten = [klassische_gesamtkosten, ecotrn_gesamtkosten]
ax.bar(kategorien, kosten)
ax.set_ylabel('Kosten in EUR')
ax.set_title('Kostenvergleich Training')

st.pyplot(fig)

# Footer
st.caption("ecoTRN Scenario Analysis Dashboard - 2025")
