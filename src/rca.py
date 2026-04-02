import pandas as pd
import numpy as np
import logging
from typing import List, Dict, Tuple
from itertools import combinations

logger = logging.getLogger(__name__)

class RootCauseAnalyzer:
    """
    Multidimensionale Root Cause Analysis Engine.
    Isoliert die Dimensionen (oder Dimensions-Paare), die den größten 
    negativen Einfluss auf die Zielmetrik am Tag einer Anomalie hatten.
    """
    
    def __init__(self, baseline_days: int = 14, base_aov: float = 120.0):
        """
        Args:
            baseline_days: Anzahl der Tage vor der Anomalie, die als Vergleich dienen.
            base_aov: Average Order Value zur groben Berechnung des Umsatzverlustes.
        """
        self.baseline_days = baseline_days
        self.base_aov = base_aov
        # Die Dimensionen aus unserem Datenmodell
        self.dimensions = ['country', 'device', 'browser', 'channel']

    def _get_combinations(self) -> List[Tuple[str, ...]]:
        """Erzeugt 1-dimensionale (z.B. nur 'browser') und 2-dimensionale (z.B. 'country'+'browser') Slices."""
        combos = []
        # 1D Segmente (z.B. "Was ist, wenn der gesamte Safari-Traffic crasht?")
        for dim in self.dimensions:
            combos.append((dim,))
        
        # 2D Segmente (z.B. "Was ist, wenn Safari nur in Frankreich crasht?")
        for pair in combinations(self.dimensions, 2):
            combos.append(pair)
            
        return combos

    def analyze(self, df: pd.DataFrame, anomaly_date: str) -> pd.DataFrame:
        """
        Führt die RCA für ein spezifisches Datum durch.
        """
        target_date = pd.to_datetime(anomaly_date)
        start_baseline = target_date - pd.Timedelta(days=self.baseline_days)
        
        # Datensatz splitten: Historie vs. Anomalie-Tag
        df_baseline = df[(df['date'] >= start_baseline) & (df['date'] < target_date)]
        df_anomaly = df[df['date'] == target_date]
        
        if df_baseline.empty or df_anomaly.empty:
            logger.error(f"Nicht genügend Daten für RCA am {anomaly_date}.")
            return pd.DataFrame()

        results = []
        combos = self._get_combinations()
        
        logger.info(f"Starte Drill-down für {anomaly_date} über {len(combos)} Dimensions-Ebenen...")

        for combo in combos:
            combo_list = list(combo)
            
            # Baseline Metriken für dieses Segment berechnen
            base_agg = df_baseline.groupby(combo_list)[['sessions', 'conversions']].sum().reset_index()
            # Erwartete CVR (historischer Durchschnitt des Segments)
            base_agg['expected_cvr'] = base_agg['conversions'] / base_agg['sessions'].replace(0, np.nan)
            
            # Actual Metriken am Tag der Anomalie
            anom_agg = df_anomaly.groupby(combo_list)[['sessions', 'conversions']].sum().reset_index()
            anom_agg = anom_agg.rename(columns={'sessions': 'actual_sessions', 'conversions': 'actual_conversions'})
            
            # Zusammenführen
            merged = pd.merge(anom_agg, base_agg[combo_list + ['expected_cvr']], on=combo_list, how='left')
            
            # Berechnen des Impacts (The "Surprise")
            merged['actual_cvr'] = merged['actual_conversions'] / merged['actual_sessions'].replace(0, np.nan)
            merged['expected_conversions'] = merged['actual_sessions'] * merged['expected_cvr']
            
            # Wie viele Conversions fehlen uns?
            merged['lost_conversions'] = merged['expected_conversions'] - merged['actual_conversions']
            
            # Business Value Translation: Was kostet uns das in Euro?
            merged['revenue_impact'] = merged['lost_conversions'] * self.base_aov
            
            # Formatieren für den Output
            for _, row in merged.iterrows():
                # Wir interessieren uns nur für Segmente mit signifikantem Verlust
                if row['revenue_impact'] > 0:
                    segment_name = " & ".join([f"{col}={row[col]}" for col in combo_list])
                    results.append({
                        'segment': segment_name,
                        'level': f"{len(combo_list)}D",
                        'actual_sessions': row['actual_sessions'],
                        'expected_cvr': row['expected_cvr'],
                        'actual_cvr': row['actual_cvr'],
                        'lost_conversions': row['lost_conversions'],
                        'revenue_impact_eur': row['revenue_impact']
                    })

        results_df = pd.DataFrame(results)
        
        if not results_df.empty:
            # Sortieren nach dem größten finanziellen Impact
            results_df = results_df.sort_values('revenue_impact_eur', ascending=False)
            
        return results_df