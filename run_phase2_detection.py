import os
import pandas as pd
import logging
from src.detection import MacroAnomalyDetector

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("--- Starte Phase 2: Macro Anomaly Detection ---")
    
    # 1. Daten laden (Output aus Phase 1)
    input_path = os.path.join("data", "data_simulated.csv")
    if not os.path.exists(input_path):
        logger.error(f"Datei nicht gefunden: {input_path}. Bitte erst Phase 1 ausführen!")
        return
        
    df = pd.read_csv(input_path)
    # Wichtig: Datum als datetime parsen
    df['date'] = pd.to_datetime(df['date']) 
    
    # 2. Detektor initialisieren (Wir überwachen den Umsatz)
    # Wir nutzen threshold=3.5, was einem sehr konservativen Alarm-Level entspricht (weniger False Positives)
    detector = MacroAnomalyDetector(metric='revenue', threshold_z=3.5)
    
    # 3. Detektion ausführen
    results_df = detector.detect(df)
    
    # 4. Ergebnisse auswerten und für Phase 3 bereitstellen
    anomalous_dates = detector.get_anomalous_dates(results_df)
    
    logger.info("--- Detektions-Bericht ---")
    if anomalous_dates:
        for date_str in anomalous_dates:
            row = results_df[results_df['date'] == pd.to_datetime(date_str)].iloc[0]
            logger.warning(f"🚨 ANOMALIE GEFUNDEN am {date_str}!")
            logger.warning(f"   Umsatz: {row['revenue']:,.2f} EUR")
            logger.warning(f"   Erwartet (Trend + Saisonalität): {(row['trend'] + row['seasonality']):,.2f} EUR")
            logger.warning(f"   Z-Score: {row['robust_z_score']:.2f}")
    else:
        logger.info("Keine Makro-Anomalien gefunden.")
        
    # 5. Speichern der Makro-Ergebnisse (Später fürs Dashboard nützlich)
    output_path = os.path.join("data", "macro_detection_results.csv")
    results_df.to_csv(output_path, index=False)
    logger.info(f"Makro-Ergebnisse exportiert nach: {output_path}")
    logger.info("--- Phase 2 abgeschlossen ---")

if __name__ == "__main__":
    main()