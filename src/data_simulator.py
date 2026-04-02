import pandas as pd
import numpy as np
from datetime import timedelta, date
from typing import List, Dict
import itertools
import logging

# Logger Setup für dieses Modul
logger = logging.getLogger(__name__)

class EcommerceDataSimulator:
    """
    Generiert synthetische, multidimensionale E-Commerce-Daten als OLAP-Cube.
    Erzeugt Baselines mit Saisonalität und erlaubt die gezielte Injektion von Anomalien.
    """
    
    def __init__(self, start_date: date, end_date: date, random_state: int = 42):
        self.start_date = start_date
        self.end_date = end_date
        self.random_state = random_state
        np.random.seed(self.random_state)
        
        # INTERVIEW-TIPP: Marktanteile als Gewichte. 
        # Das macht den späteren Drill-Down anspruchsvoll, da kleine Segmente
        # (z.B. Tablet + Firefox + Referral) weniger Rauschen tolerieren.
        self.dimensions = {
            'country': {'DE': 0.4, 'FR': 0.25, 'UK': 0.2, 'US': 0.15},
            'device': {'Mobile': 0.6, 'Desktop': 0.35, 'Tablet': 0.05},
            'browser': {'Chrome': 0.5, 'Safari': 0.35, 'Firefox': 0.15},
            'channel': {'Organic': 0.4, 'Paid': 0.3, 'Direct': 0.2, 'Referral': 0.1}
        }
        
        self.base_sessions_per_day = 100000
        self.base_cvr = 0.03  
        self.base_aov = 120.0 

    def _generate_date_range(self) -> List[date]:
        """Erzeugt eine kontinuierliche Liste von Datums-Objekten."""
        days = (self.end_date - self.start_date).days
        return [self.start_date + timedelta(days=i) for i in range(days + 1)]

    def _get_seasonality_factor(self, current_date: date) -> float:
        """Modelliert Wochenend- und Montags-Peaks."""
        weekday = current_date.weekday()
        if weekday in [5, 6]:  
            return 1.25 
        elif weekday == 0:     
            return 1.10
        return 1.0

    def generate_baseline_data(self) -> pd.DataFrame:
        """
        Generiert den sauberen Datenstamm ohne systematische Fehler.
        Jede Zeile entspricht einer einzigartigen Kombination der Dimensionen pro Tag.
        """
        logger.info(f"Starte Datengenerierung von {self.start_date} bis {self.end_date}.")
        dates = self._generate_date_range()
        
        dim_names = list(self.dimensions.keys())
        dim_values = [list(self.dimensions[d].keys()) for d in dim_names]
        combinations = list(itertools.product(*dim_values))
        
        records = []
        
        for d in dates:
            seasonality = self._get_seasonality_factor(d)
            daily_sessions = int(self.base_sessions_per_day * seasonality * np.random.normal(1.0, 0.05))
            
            for combo in combinations:
                prob = 1.0
                for i, dim_name in enumerate(dim_names):
                    prob *= self.dimensions[dim_name][combo[i]]
                
                segment_sessions = int(daily_sessions * prob * np.random.normal(1.0, 0.02))
                segment_cvr = max(0.001, self.base_cvr * np.random.normal(1.0, 0.05))
                segment_conversions = np.random.binomial(segment_sessions, segment_cvr)
                segment_aov = self.base_aov * np.random.normal(1.0, 0.05)
                segment_revenue = segment_conversions * segment_aov
                
                records.append({
                    'date': pd.to_datetime(d),
                    'country': combo[0],
                    'device': combo[1],
                    'browser': combo[2],
                    'channel': combo[3],
                    'sessions': segment_sessions,
                    'conversions': segment_conversions,
                    'revenue': round(segment_revenue, 2),
                    'is_anomaly': 0 # Target Variable für unsere Evaluierung
                })
                
        df = pd.DataFrame(records)
        logger.info(f"Basisdaten generiert. Gesamtzeilen: {len(df)}.")
        return df

    def inject_anomaly(
        self, 
        df: pd.DataFrame, 
        target_date: str, 
        dimension_filters: Dict[str, str], 
        cvr_drop_factor: float = 0.5
    ) -> pd.DataFrame:
        """
        Injiziert einen Fehler in ein spezifisches Segment an einem bestimmten Tag.
        Sessions bleiben konstant, aber Conversions und Umsatz brechen ein.
        """
        logger.info(f"Injiziere Anomalie am {target_date} für Segment {dimension_filters} mit {cvr_drop_factor*100}% CVR Drop.")
        df_out = df.copy()
        
        mask = (df_out['date'] == pd.to_datetime(target_date))
        for col, val in dimension_filters.items():
            mask &= (df_out[col] == val)
            
        impacted_rows = df_out[mask].copy()
        
        if impacted_rows.empty:
            logger.warning("Warnung: Filterkombination existiert nicht in den Daten. Keine Anomalie injiziert.")
            return df_out
            
        impacted_rows['conversions'] = (impacted_rows['conversions'] * (1 - cvr_drop_factor)).astype(int)
        impacted_rows['revenue'] = round(impacted_rows['conversions'] * self.base_aov * np.random.normal(1.0, 0.05), 2)
        impacted_rows['is_anomaly'] = 1 
        
        df_out.update(impacted_rows)
        df_out['is_anomaly'] = df_out['is_anomaly'].astype(int)
        
        return df_out