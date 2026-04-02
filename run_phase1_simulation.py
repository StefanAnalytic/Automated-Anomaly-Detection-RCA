import os
import logging
import time  # <-- NEU: Importiert für den dynamischen Zufall
from datetime import date
from src.data_simulator import EcommerceDataSimulator

# Logging konfigurieren (Standard für Production-Skripte)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("--- Starte Phase 1: Data Simulation ---")
    
    # 1. Simulator initialisieren (3 Monate Daten)
    start_date = date(2023, 1, 1)
    end_date = date(2023, 3, 31)
    
    # NEU: Wir generieren einen echten Random Seed basierend auf der aktuellen Systemzeit
    current_seed = int(time.time())
    logger.info(f"Initialisiere Simulator mit echtem Zufall (Seed: {current_seed})")
    
    # Der Seed wird nun bei jedem Start neu gesetzt
    simulator = EcommerceDataSimulator(
        start_date=start_date, 
        end_date=end_date,
        random_state=current_seed 
    )
    
    # 2. Basisdaten generieren
    df = simulator.generate_baseline_data()
    
    # 3. Den "Ground Truth" Bug injizieren
    # Szenario: Ein fehlerhaftes Update zerstört den Safari-Checkout auf mobilen Geräten.
    anomaly_date = '2023-03-15'
    filters = {'device': 'Mobile', 'browser': 'Safari'}
    
    df_anomalous = simulator.inject_anomaly(
        df=df, 
        target_date=anomaly_date, 
        dimension_filters=filters, 
        cvr_drop_factor=0.85 # 85% Drop in der Conversion Rate für dieses exakte Segment
    )
    
    # 4. Validierung & Business Metriken berechnen
    normal_revenue = df[df['date'] == anomaly_date]['revenue'].sum()
    anomalous_revenue = df_anomalous[df_anomalous['date'] == anomaly_date]['revenue'].sum()
    revenue_loss = normal_revenue - anomalous_revenue
    
    logger.info("--- Sanity Check Ergebnisse ---")
    logger.info(f"Erwarteter Gesamtumsatz am {anomaly_date}: {normal_revenue:,.2f} EUR")
    logger.info(f"Tatsächlicher Umsatz am {anomaly_date} (mit Bug): {anomalous_revenue:,.2f} EUR")
    logger.info(f"Verursachter Umsatzverlust (Impact): {revenue_loss:,.2f} EUR")
    
    # 5. Speichern
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "data_simulated.csv")
    
    df_anomalous.to_csv(output_path, index=False)
    logger.info(f"Daten erfolgreich exportiert nach: {output_path}")
    logger.info("--- Phase 1 abgeschlossen ---")

if __name__ == "__main__":
    main()