import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import STL
import logging
from typing import Tuple, List

logger = logging.getLogger(__name__)

class MacroAnomalyDetector:
    """
    Erkennt Ausreißer auf aggregierten Zeitreihen (Makro-Ebene).
    Nutzt STL-Dekomposition, um Saisonalität und Trend zu entfernen,
    und bewertet die Residuen mithilfe des robusten Z-Scores (MAD).
    """
    
    def __init__(self, metric: str = 'revenue', threshold_z: float = 3.5):
        """
        Args:
            metric: Die zu überwachende Metrik (z.B. 'revenue' oder 'conversions').
            threshold_z: Der Schwellenwert für den robusten Z-Score (Standard: 3.5).
        """
        self.metric = metric
        self.threshold_z = threshold_z
        self.stl_results = None

    def _aggregate_to_daily(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aggregiert den multidimensionalen OLAP-Cube auf Tagesebene."""
        # INTERVIEW-TIPP: Erkläre hier, warum wir für die Makro-Erkennung aggregieren.
        # "Wir führen keine Root Cause Analysis für jeden Tag aus - das ist extrem 
        # rechenintensiv. Wir nutzen die Makro-Ebene als 'Trigger'. Nur wenn hier ein 
        # signifikanter Ausreißer gefunden wird, aktivieren wir die teure RCA-Engine."
        
        daily_df = df.groupby('date')[self.metric].sum().reset_index()
        daily_df = daily_df.sort_values('date').set_index('date')
        
        # Sicherstellen, dass der Index eine Frequenz hat (wichtig für statsmodels)
        daily_df = daily_df.asfreq('D') 
        return daily_df

    def _calculate_robust_z_score(self, series: pd.Series) -> pd.Series:
        """
        Berechnet den robusten Z-Score basierend auf der Median Absolute Deviation (MAD).
        Viel robuster gegen Ausreißer als die klassische Standardabweichung.
        """
        # INTERVIEW-TIPP: Das ist ein absolutes Senior-Detail!
        # Der klassische Mean und die Standardabweichung werden von dem Ausreißer selbst 
        # beeinflusst. Der Median und die MAD bleiben stabil, selbst wenn 10% der Daten 
        # massive Anomalien sind.
        
        median = series.median()
        mad = np.median(np.abs(series - median))
        
        # Konstante 0.6745 wandelt MAD in eine Skala um, die mit der 
        # Standardabweichung einer Normalverteilung vergleichbar ist.
        if mad == 0:
            return pd.Series(0, index=series.index)
            
        robust_z = 0.6745 * (series - median) / mad
        return robust_z

    def detect(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Führt die End-to-End Detektion durch.
        
        Returns:
            Ein DataFrame mit den täglichen Metriken, STL-Komponenten 
            und einem 'is_macro_anomaly' Flag.
        """
        logger.info(f"Starte Makro-Anomalie-Erkennung für Metrik: {self.metric}...")
        
        daily_df = self._aggregate_to_daily(df)
        
        # 1. STL Dekomposition (Period=7 für wöchentliche Saisonalität in E-Commerce Daten)
        stl = STL(daily_df[self.metric], period=7, robust=True)
        self.stl_results = stl.fit()
        
        daily_df['trend'] = self.stl_results.trend
        daily_df['seasonality'] = self.stl_results.seasonal
        daily_df['residual'] = self.stl_results.resid
        
        # 2. Robuste Fehlerbewertung auf den Residuen
        daily_df['robust_z_score'] = self._calculate_robust_z_score(daily_df['residual'])
        
        # 3. Anomalien flaggen (absoluter Z-Score größer als Schwellenwert)
        daily_df['is_macro_anomaly'] = (daily_df['robust_z_score'].abs() > self.threshold_z).astype(int)
        
        anomalies_found = daily_df['is_macro_anomaly'].sum()
        logger.info(f"Detektion abgeschlossen. {anomalies_found} Anomalie(n) auf Makro-Ebene gefunden.")
        
        return daily_df.reset_index()

    def get_anomalous_dates(self, results_df: pd.DataFrame) -> List[str]:
        """Gibt eine Liste der Daten zurück, an denen Anomalien aufgetreten sind."""
        anomalies = results_df[results_df['is_macro_anomaly'] == 1]
        return anomalies['date'].dt.strftime('%Y-%m-%d').tolist()