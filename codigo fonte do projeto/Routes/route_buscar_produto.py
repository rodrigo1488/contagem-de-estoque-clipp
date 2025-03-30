from flask import Blueprint, request, jsonify
from databases import conectar_firebird  # Importando do databases.py
from databases import CAMINHO_DB_LOCAL
import datetime
import os

Route_buscar_produto_bp = Blueprint('Route_buscar_produto_bp', __name__)

# Rota para buscar produto no Firebird
@Route_buscar_produto_bp.route("/produto/<codigo_barras>", methods=["GET"])
def buscar_produto(codigo_barras):
    try:
        codigo_barras = codigo_barras.strip()
        conn = conectar_firebird()  # Chama a função do databases.py
        cur = conn.cursor()
        
        query = """
            SELECT e.DESCRICAO, p.QTD_ATUAL
            FROM TB_EST_PRODUTO p
            JOIN TB_EST_IDENTIFICADOR i ON p.ID_IDENTIFICADOR = i.ID_IDENTIFICADOR
            JOIN TB_ESTOQUE e ON i.ID_ESTOQUE = e.ID_ESTOQUE
            WHERE p.COD_BARRA = ?
        """
        
        cur.execute(query, (codigo_barras,))
        produto = cur.fetchone()
        
        conn.close()
        
        if produto:
            return jsonify({
                "Descricao": produto[0],
                "Quantidade": produto[1]
            })
        else:
            return jsonify({"erro": "Produto não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500



