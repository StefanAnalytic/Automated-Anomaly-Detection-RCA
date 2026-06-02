<div align="center">

# 🛡️ The Business Guardian: Anomaly Detection & RCA

[![Python](https://img.shields.io/badge/Language-Python_3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Statsmodels](https://img.shields.io/badge/Math-Statsmodels-8CAAE6?style=for-the-badge)](https://www.statsmodels.org/)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Status](https://img.shields.io/badge/Status-Production_Ready-2ea44f?style=for-the-badge)](#)

**Ein professionelles End-to-End System zur Überwachung von E-Commerce-Metriken und vollautomatisierter Ursachenanalyse (Root Cause Analysis).**

*Ersetzt die manuelle, stundenlange Fehlersuche in Big-Data-Umgebungen durch intelligente, multidimensionale Algorithmen, die Umsatzverluste in Echtzeit detektieren und isolieren.*

---
</div>

## 💼 Business Value & Problem Statement

In komplexen E-Commerce-Umgebungen führen kleine technische Fehler (z.B. *ein defekter Checkout-Button nur für Safari-Nutzer auf iOS in Deutschland*) oft unbemerkt zu massiven Umsatzverlusten. **The Business Guardian** löst dieses Problem vollautomatisch in zwei Stufen:

| Phase | Technischer Algorithmus | Business Impact |
| :--- | :--- | :--- |
| **🚨 1. Makro-Detektion** | **STL-Decomposition** (Seasonal-Trend Decomposition). Trennt normales Rauschen und Saisonalität (z.B. hohe Wochenend-Umsätze) vom echten Signal. Schlägt nur Alarm, wenn das *Residuum* (der unerklärliche Rest) statistisch signifikant abweicht (Keine False-Positives). | Beantwortet die Frage:<br>**"Wann brennt es?"** |
| **🔍 2. Root Cause Analysis** | Multidimensionaler Drill-Down. Sobald ein Alarm triggert, iteriert die RCA-Engine durch alle Daten-Dimensionen (Land, Gerät, Browser), vergleicht die aktuelle Metrik mit dem 14-Tage-Schnitt und isoliert exakt das Sub-Segment mit dem höchsten **Revenue Impact**. | Beantwortet die Frage:<br>**"Warum brennt es?"** |

---

## 🏗️ Systemarchitektur & Tech-Stack

Die Pipeline ist modular aufgebaut und trennt die stochastische Detektion sauber von der Visualisierung:

* 🧠 **Backend & Engine:** `Python` (`Pandas`, `NumPy`, `Statsmodels`) für hochperformante Zeitreihenanalyse und Datenverarbeitung.
* 📊 **Frontend & Visualisierung:** Interaktives **Streamlit Dashboard** gepaart mit `Plotly`, um die Anomalien und den Root-Cause direkt für das Management visuell greifbar zu machen.
* ⚙️ **Orchestrierung:** Zentrale `main.py` zur nahtlosen End-to-End Ausführung (Daten-Generierung $\rightarrow$ Fehler-Injektion $\rightarrow$ Analyse $\rightarrow$ Dashboard).

---

## 🚀 Quick Start (Lokales Setup & Simulation)

<details>
<summary><b>🛠️ Installation & Ausführung (Hier klicken zum Aufklappen)</b></summary>

Das System beinhaltet einen integrierten Simulator, der synthetische E-Commerce-Daten erzeugt, einen **zufälligen Bug** injiziert und die Pipeline darauf ansetzt.

### 1. Abhängigkeiten installieren
```bash
pip install streamlit pandas numpy statsmodels plotly
