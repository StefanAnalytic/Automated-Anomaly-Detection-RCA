🛡️ The Business Guardian: Automated Anomaly Detection & RCA
Ein End-to-End System zur Überwachung von Business-Metriken und automatisierter Ursachenanalyse (Root Cause Analysis) im E-Commerce.

📌 Das Problem
In großen Tech-Konzernen führen kleine technische Fehler (z.B. ein Bug nur bei Safari-Nutzern auf dem Handy) oft zu massiven Umsatzverlusten. Die manuelle Suche nach der Ursache in Milliarden von Datenpunkten dauert Stunden. "The Business Guardian" löst dies vollautomatisch.

💡 Die Lösung
Das System arbeitet in zwei intelligenten Schritten:

Makro-Detektion (Wann brennt es?): Mittels STL-Dekomposition (Zeitreihenanalyse) trennt der Algorithmus normales Rauschen und Saisonalität (z.B. starke Wochenenden) vom echten Trend. Er schlägt nur Alarm, wenn das Residuum (der unerklärliche Rest) statistisch signifikant abweicht.

Root Cause Analysis (Warum brennt es?): Sobald ein Fehler erkannt wird, bohrt sich die RCA-Engine durch alle Daten-Dimensionen (Land, Gerät, Browser). Sie vergleicht die aktuelle Performance mit dem 14-Tage-Schnitt und berechnet den exakten Revenue Impact in Euro.

🏗️ Architektur & Tech-Stack
Backend: Python (Pandas, Numpy, Statsmodels für die Mathematik).

Algorithmus: STL-Decomposition & Multidimensionaler Drill-down.

Frontend: Interaktives Streamlit Dashboard mit Plotly-Visualisierungen.

Orchestrierung: Modulare Struktur mit einer main.py als One-Click-Pipeline.


Getty Images
Explore
🚀 Quick Start (One-Click)
Abhängigkeiten installieren:

Bash
pip install streamlit pandas numpy statsmodels plotly
Pipeline & Dashboard starten:

Bash
python main.py
Dieser Befehl generiert synthetische Daten, injiziert einen versteckten Bug, führt die Analyse aus und öffnet das Dashboard.