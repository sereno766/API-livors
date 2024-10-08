from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def inicializar_banco_de_dados():
    conn = sqlite3.connect('livros.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS  livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL
        )
    ''') 
    conn.commit()
    conn.close()

def conectar_banco():
    conn = sqlite3.connect('livros.db')
    return conn

inicializar_banco_de_dados()

@app.route('/livros',methods=['GET'])
def obter_livro():
    conn= conectar_banco()
    cursor= conn.cursor()
    cursor.execute('SELECT * FROM livros')
    livros = cursor.fetchall()
    conn.close()

    livros_json = [{'id': row[0], 'titulo': row[1], 'autor': row[2]} for row in livros]
    if not livros_json:
        return jsonify({'mensagem':'não há livros',}), 404
    
    return jsonify(livros_json)
@app.route('/livros/<int:id>',methods=['GET'])
def obter_livors_por_id(id):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('SELEC * FROM livros WHERE id = ?', (id,))
    livro = cursor.fetchone()
    conn.close()
    if livro:
        return jsonify({'id':livro[0],'titulo':livro[1],'autor':livro[2]})
    return jsonify({'error':'livro não encontrado'}),404

@app.route('/livros', methods=['POST'])
def adicionar_livro():
    novo_livro = request.get_json()
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO livros (titulo, autor) VALUES (?, ?)',(novo_livro['titulo'], novo_livro['autor']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Livro adicionado com sucesso!'})

@app.route('/livros/<int:id>', methods=['PUT'])
def editra_livro_por_id(id):
    livro_alterado = request.get_json()
    conn = conectar_banco()
    cursor =conn.cursor()
    


app.run(port=5000,host='localhost',debug=True)
# --------codigo antigo sem o uso de banco de datos -------------
'''
@app.route('/livros',methods=['GET'])
def obter_livros():
    return jsonify(livros)

@app.route('/livros/<int:id>',methods=['GET'])
def obeter_livro_por_id(id):
    for livro in livros:
        if livro.get('id') == id:
            return jsonify(livro)
    return jsonify('error livro não encontrado')

@app.route('/livros/<int:id>',methods=['PUT'])
def editar_livro_por_id(id):
    livro_alterado = request.get_json()
    for indice,livro in enumerate(livros):
        if livro.get('id') == id:
            livros[indice].update(livro_alterado)
            return jsonify(livros[indice])

@app.route('/livros',methods=['POST'])
def adicionar_novo_livro():
    novo_livro = request.get_json()
    livros.append(novo_livro)
    return jsonify(livros)

@app.route('/livros/<int:id>',methods=['DELETE'])
def remove_livro(id):
    for indice,livro in enumerate(livros):
        if livro.get('id') == id:
            del livros[indice]
            return jsonify(livros)
    return jsonify('error livro não encontrado')
'''
