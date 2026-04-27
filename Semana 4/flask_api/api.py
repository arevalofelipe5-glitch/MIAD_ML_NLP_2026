#!/usr/bin/python
from flask import Flask
from flask_restx import Api, Resource, fields
import os
from prediction import predict 

from flask import Flask
from flask_restx import Api, Resource, fields
import joblib
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
import sys

app = Flask(__name__)

api = Api(
    app,
    version='1.0',
    title='API Predicción de popularidad de canciones en Spotify',
    description='API para predecir popularidad utilizando XGBoost Regressor')

ns = api.namespace('predict', description='Predicción de popularidad')

# Parser para capturar los 16 argumentos
parser = api.parser()
parser.add_argument('album_name', type=str, required=True, location='args')
parser.add_argument('danceability', type=float, required=True, location='args')
parser.add_argument('energy', type=float, required=True, location='args')
parser.add_argument('loudness', type=float, required=True, location='args')
parser.add_argument('speechiness', type=float, required=True, location='args')
parser.add_argument('acousticness', type=float, required=True, location='args')
parser.add_argument('instrumentalness', type=float, required=True, location='args')
parser.add_argument('liveness', type=float, required=True, location='args')
parser.add_argument('valence', type=float, required=True, location='args')
parser.add_argument('tempo', type=float, required=True, location='args')
parser.add_argument('track_genre', type=str, required=True, location='args')
parser.add_argument('energy_danceability', type=float, required=True, location='args')
parser.add_argument('valence_energy', type=float, required=True, location='args')
parser.add_argument('acousticness_energy', type=float, required=True, location='args')
parser.add_argument('main_artist', type=str, required=True, location='args') # Cambiado a str
parser.add_argument('duration_min', type=float, required=True, location='args')

resource_fields = api.model('Resource', {
    'result': fields.Float,
})

@ns.route('/')
class PopularidadApi(Resource):

    @api.doc(parser=parser)
    @api.marshal_with(resource_fields)
    def get(self):
        # Obtener los argumentos de la solicitud
        args = parser.parse_args()

        # Llamar a la función predict pasando todo el diccionario
        score = predict(args)

        # Retornar el resultado numérico
        return {
         "result": float(score)
        }, 200

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)