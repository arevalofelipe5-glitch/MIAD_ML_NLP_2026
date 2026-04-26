import joblib
import os
import pandas as pd
import sys


# Usamos __file__ para que Python sepa automáticamente dónde está este archivo
ruta_actual = os.path.dirname(os.path.abspath(__file__))
if ruta_actual not in sys.path:
    sys.path.append(ruta_actual)

from custom_transformers import AgregadosPorGrupo

def predict(data_dict):
    path = os.path.join(os.path.dirname(__file__), 'popularidad.pkl')
    modeloxgb = joblib.load(path)
    
    df = pd.DataFrame([data_dict])
    
    # Asegúrate de que las columnas coincidan con las del entrenamiento
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype('category')
            
    p1 = modeloxgb.predict(df)[0]
    return float(p1)