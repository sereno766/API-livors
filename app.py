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
def editar_livro_por_id(id):
    livro_alterado = request.get_json()
    conn = conectar_banco()
    cursor =conn.cursor()
    cursor.execute('UPDATE livros Set titulo = ?, autor = ? WHERE id = ?', (livro_alterado['titulo'], livro_alterado['autor'], id ))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify ({'error': 'livro não encontrado'}), 404
    return jsonify({'message': 'livro atualizado com sucesso'})

@app.route('/livros/<int:id>', methods=['DELETE'])
def remove_livro(id):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM livros WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({'error': 'Livro não encontrado'}), 404
    return jsonify({'message': 'Livro removido com sucesso!'})

app.run(port=5000,host='localhost',debug=True)
