from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Estacoes(db.Model):
    id_estacao = db.Column(db.Integer, primary_key=True)
    nome_estacao = db.Column(db.String(100))
    codigo_wmo = db.Column(db.String(100))
    uf = db.Column(db.String(100))
    data_fundacao = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    altitude = db.Column(db.Float)


    def __init__(self, nome_aeroporto, codigo_wmo, uf, data_fundacao, latitude, longitude, altitude):
        self.nome_aeroporto = nome_aeroporto
        self.codigo_wmo = codigo_wmo
        self.uf = uf
        self.data_fundacao = data_fundacao
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

class EstacoesSchema(ma.Schema):
    class Meta:
        fields = ('id_estacao', 'nome_estacao', 'codigo_wmo', 'uf', 'data_fundacao', 'latitude', 'longitude', 'altitude')

estacoes_schema = EstacoesSchema()
estacoes_all_schema = EstacoesSchema(many=True)

@app.route('/estacoes', methods=['POST'])
def add_estacao():
    nome_estacao = request.json['nome_estacao']
    codigo_wmo = request.json['codigo_wmo']
    uf = request.json['uf']
    data_fundacao = request.json['data_fundacao']
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    altitude = request.json['altitude']

    nova_estacao = Estacoes(nome_estacao, codigo_wmo, uf, data_fundacao, latitude, longitude, altitude)
    db.session.add(nova_estacao)
    db.session.commit()

    return estacoes_schema.jsonify(nova_estacao)

@app.route('/estacoes', methods=['GET'])
def get_all_estacoes():
    all_estacoes = Estacoes.query.all()
    result = estacoes_all_schema.dump(all_estacoes)
    return jsonify(result)

@app.route('/estacoes/<id_estacao>', methods=['GET'])
def get_estacoes(id_estacao):
    estacao = Estacoes.query.get(id_estacao)
    return estacoes_schema.jsonify(estacao)

@app.route('/estacoes/<id_estacao>', methods=['PUT'])
def update_estacoes(id_estacao):
    estacao = Estacoes.query.get(id_estacao)
    nome_estacao = request.json['nome_estacao']
    codigo_wmo = request.json['codigo_wmo']
    uf = request.json['uf']
    data_fundacao = request.json['data_fundacao']
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    altitude = request.json['altitude']

    estacao.nome_estacao = nome_estacao
    estacao.codigo_wmo = codigo_wmo
    estacao.uf = uf
    estacao.data_fundacao = data_fundacao
    estacao.latitude = latitude
    estacao.longitude = longitude
    estacao.altitude = altitude

    db.session.commit()

    return estacoes_schema.jsonify(estacao)

@app.route('/estacoes/<id_estacao>', methods=['DELETE'])
def delete_estacoes(id_estacao):
    estacao = Estacoes.query.get(id_estacao)
    db.session.delete(estacao)
    db.session.commit()
    return estacoes_schema.jsonify(estacao)


if __name__ == '__main__':
    app.run(debug=True)