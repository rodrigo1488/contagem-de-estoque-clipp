from flask import Flask, request, jsonify, render_template, Blueprint
import fdb
import sqlite3
import os
import datetime
from databases import CAMINHO_DB_LOCAL
from databases import CAMINHO_ARQUIVO



Route_gerar_txt_bp = Blueprint('Route_gerar_txt_bp', __name__)



# Rota para gerar o arquivo TXT a partir do SQLite
@Route_gerar_txt_bp.route("/gerar-txt", methods=["GET"])
def gerar_txt():
    try:
        # Defina o diretório onde deseja salvar o arquivo
        diretorio = "C:/contagem_estoque"
        
        # Crie o diretório se ele não existir
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)

        # Caminho completo do arquivo
        CAMINHO_ARQUIVO = os.path.join(diretorio, "contagem_estoque.txt")

        # Conectando ao banco e buscando os dados
        conn = sqlite3.connect(CAMINHO_DB_LOCAL)
        cur = conn.cursor()
        cur.execute("SELECT codigo_barras, quantidade FROM contagem_estoque")
        produtos = cur.fetchall()
        conn.close()

        # Verificando se não há produtos
        if not produtos:
            return jsonify({"message": "Nenhum produto encontrado para exportação"}), 404

        # Gerando o arquivo
        with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as file:
            for codigo_barras, quantidade in produtos:
                file.write(f"{codigo_barras}|{quantidade}\n")

        return jsonify({"message": "Arquivo TXT gerado com sucesso", "arquivo": CAMINHO_ARQUIVO})
    
    except Exception as e:
        print(f"Erro ao gerar o arquivo no caminho: {CAMINHO_ARQUIVO}")
        print(f"Erro: {str(e)}")
        return jsonify({"message": "Erro ao gerar o arquivo TXT", "error": str(e)}), 500