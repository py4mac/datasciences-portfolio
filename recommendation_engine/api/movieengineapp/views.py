from __future__ import print_function
import sys

from flask import Flask, render_template, url_for, request, jsonify
import json
import numpy as np

app = Flask(__name__)

app.config.from_object('config')

from .utils import MovieEngine, MyEncoder

myEngine = MovieEngine()

@app.route('/recommend/', methods = ['GET'])
def recommend():
    id_film = request.args.get('id', "")
    sequel = request.args.get('sequel', "")
    if sequel == "True":
        sequel = True
    else:
        sequel = False
    result = []
    if id_film != "":
        result = myEngine.lookSimilarById(int(id_film), sequel)
    return jsonify(_results=json.dumps(result, cls=MyEncoder))

@app.route('/films/', methods = ['GET'])
def films():
    result = myEngine.getListFilmWithIndex()
    return jsonify(_results=json.dumps(result, cls=MyEncoder))