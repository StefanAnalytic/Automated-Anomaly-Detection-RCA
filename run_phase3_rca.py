import os
import pandas as pd
import logging
from src.rca import RootCauseAnalyzer

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("--- Starte Phase 3: Root Cause Analysis ---")
    
    # 1. Daten laden
    data_path = os.path.join("data", "data_simulated.csv")
    macro_path = os.path.join("data", "macro_detection_results.csv")
    
    if not os.path.exists(data_path) or not os.path.exists(macro_path):
        logger.error("Daten fehlen. Bitte erst Phase 1 und Phase 2 ausführen!")
        return
        
    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['date'])
    
    macro_results = pd.read_csv(macro_path)
    
    # 2. Finde die Daten, die in Phase 2 als Anomalie markiert wurden
    anomalous_dates = macro_results[macro_results['is_macro_anomaly'] == 1]['date'].tolist()
    
    if not anomalous_dates:
        logger.info("Keine Anomalien in den Makro-Daten gefunden. RCA nicht notwendig.")
        return
        
    # 3. RCA Engine initialisieren
    rca = RootCauseAnalyzer(baseline_days=14)
    
    # 4. Drill-down für jeden anomalen Tag
    for date_str in anomalous_dates:
        logger.info(f"Untersuche Ursachen für Umsatzabfall am {date_str}...")
        
        # Algorithmus ausführen
        rca_results = rca.analyze(df, date_str)
        
        if not rca_results.empty:
            logger.info("🎯 ROOT CAUSE GEFUNDEN. Top 3 Segmente nach Revenue Impact:")
            
            # Top 3 extrahieren
            top_3 = rca_results.head(3)
            
            print("\n" + "="*80)
            print(f" RCA BERICHT FÜR {date_str}")
            print("="*80)
            
            for i, (_, row) in enumerate(top_3.iterrows(), 1):
                cvr_drop = (row['expected_cvr'] - row['actual_cvr']) / row['expected_cvr'] * 100
                print(f"#{i} Segment: {row['segment']}")
                print(f"   - Level: {row['level']}")
                print(f"   - Expected CVR: {row['expected_cvr']:.2%}")
                print(f"   - Actual CVR:   {row['actual_cvr']:.2%} (Drop: {cvr_drop:.1f}%)")
                print(f"   - Traffic (Sessions): {row['actual_sessions']:,.0f}")
                print(f"   => ESTIMATED REVENUE LOSS: {row['revenue_impact_eur']:,.2f} EUR")
                print("-" * 80)
            print("\n")
            
            # Speichern für das Streamlit Dashboard (Phase 4)
            output_path = os.path.join("data", f"rca_results_{date_str[:10]}.csv")
            rca_results.to_csv(output_path, index=False)
            logger.info(f"Detaillierte RCA-Ergebnisse exportiert nach {output_path}")

    logger.info("--- Phase 3 abgeschlossen ---")

if __name__ == "__main__":
    main()