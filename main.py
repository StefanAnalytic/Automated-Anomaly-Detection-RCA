import subprocess
import sys
import logging
import time

# Logging für unseren Pipeline-Orchestrator
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - ⚙️ ORCHESTRATOR - %(message)s'
)
logger = logging.getLogger(__name__)

def run_step(script_name: str, description: str):
    """
    Führt ein Python-Skript als Subprozess aus und bricht bei Fehlern sauber ab.
    sys.executable stellt sicher, dass exakt dein aktuelles venv genutzt wird.
    """
    logger.info(f"🚀 STARTE SCHRITT: {description} ({script_name})")
    
    result = subprocess.run([sys.executable, script_name])
    
    if result.returncode != 0:
        logger.error(f"❌ FEHLER in {script_name}. Pipeline abgebrochen.")
        sys.exit(1)
        
    logger.info(f"✅ SCHRITT ABGESCHLOSSEN: {description}\n")
    time.sleep(1) # Kurze Pause für saubere Logs im Terminal

def main():
    print("\n" + "="*70)
    print(" 🛡️ THE BUSINESS GUARDIAN - AUTOMATED END-TO-END PIPELINE 🛡️")
    print("="*70 + "\n")
    
    # 1. Pipeline-Schritte nacheinander ausführen
    run_step("run_phase1_simulation.py", "Phase 1 - Data Simulation & Bug Injection")
    run_step("run_phase2_detection.py", "Phase 2 - Macro Anomaly Detection (STL)")
    run_step("run_phase3_rca.py", "Phase 3 - Multidimensional Root Cause Analysis")
    
    # 2. Dashboard starten
    logger.info("🚀 STARTE COMMAND CENTER (Streamlit Dashboard)...")
    logger.info("Das Dashboard öffnet sich gleich in deinem Browser. (Abbruch im Terminal mit CTRL+C)")
    print("="*70 + "\n")
    
    # Streamlit wird als Modul aufgerufen, damit es sauber im venv läuft
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app/dashboard.py"])

if __name__ == "__main__":
    main()