# 🛡️ The Business Guardian: Automated Anomaly Detection & RCA

**Ein professionelles End-to-End System zur Überwachung von E-Commerce-Metriken und automatisierter Ursachenanalyse (Root Cause Analysis).**

---

### 🚀 Das Problem
In komplexen Tech-Konzernen führen kleine technische Fehler (z.B. ein Bug nur bei Safari-Nutzern auf dem Handy) oft zu massiven Umsatzverlusten. Die manuelle Suche nach der Ursache in Milliarden von Datenpunkten dauert Stunden. **The Business Guardian** löst dies vollautomatisch.

### 💡 Die Lösung
Das System arbeitet in zwei intelligenten Schritten:

1. **Makro-Detektion (Wann brennt es?):** Mittels **STL-Dekomposition** (Zeitreihenanalyse) trennt der Algorithmus normales Rauschen und Saisonalität (z.B. starke Wochenenden) vom echten Trend. Er schlägt nur Alarm, wenn das **Residuum** (der unerklärliche Rest) statistisch signifikant abweicht.

2. **Root Cause Analysis (Warum brennt es?):** Sobald ein Fehler erkannt wird, bohrt sich die **RCA-Engine** durch alle Daten-Dimensionen (Land, Gerät, Browser). Sie vergleicht die aktuelle Performance mit dem 14-Tage-Schnitt und isoliert das Segment mit dem höchsten **Revenue Impact**.

---

### 🏗️ Architektur & Tech-Stack
* **Backend:** Python (Pandas, Numpy, Statsmodels).
* **Algorithmus:** STL-Decomposition & Multidimensionaler Drill-down.
* **Frontend:** Interaktives **Streamlit Dashboard** mit Plotly-Visualisierungen.
* **Orchestrierung:** Modulare Struktur mit einer `main.py` als One-Click-Pipeline.

---

### 🛠️ Installation & Quick Start

**1. Abhängigkeiten installieren:**
```bash
pip install streamlit pandas numpy statsmodels plotly

python main.py (Dieser Befehl generiert neue Daten, injiziert einen zufälligen Bug, führt die Analyse aus und öffnet direkt das Dashboard).