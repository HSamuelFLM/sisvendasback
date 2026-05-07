import sqlite3

DB_NAME = 'vendas.db'

def conectar():
    return sqlite3.connect(DB_NAME)

def criar_tabelas():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                login TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT,
                telefone TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL,
                estoque INTEGER NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                produto_id INTEGER,
                quantidade INTEGER,
                total REAL,
                data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id),
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
            )
        ''')
        conn.commit()

# ----- USUÁRIOS -----
def registrar_usuario(nome, login, senha):
    with conectar() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (nome, login, senha) VALUES (?, ?, ?)",
                           (nome, login, senha))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

def autenticar_usuario(login, senha):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE login = ? AND senha = ?", (login, senha))
        return cursor.fetchone() is not None

# ----- CLIENTES -----
def cadastrar_cliente(nome, email, telefone):
    with conectar() as conn:
        cursor = conn.cutor()
        cursor.execute("INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)",
                       (nome, email, telefone))
        conn.commit()

def listar_clientes():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, email, telefone FROM clientes")
        return cursor.fetchall()

# ----- PRODUTOS -----
def cadastrar_produto(nome, preco, estoque):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO produtos (nome, preco, estoque) VALUES (?, ?, ?)",
                       (nome, preco, estoque))
        conn.commit()

def listar_produtos():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, preco, estoque FROM produtos")
        return cursor.fetchall()

def atualizar_estoque(produto_id, quantidade_vendida):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
                       (quantidade_vendida, produto_id))
        conn.commit()

def obter_preco_produto(produto_id):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT preco FROM produtos WHERE id = ?", (produto_id,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None

# ----- VENDAS -----
def registrar_venda(cliente_id, produto_id, quantidade):
    preco = obter_preco_produto(produto_id)
    if preco is None:
        return False
    total = preco * quantidade
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO vendas (cliente_id, produto_id, quantidade, total)
            VALUES (?, ?, ?, ?)
        ''', (cliente_id, produto_id, quantidade, total))
        conn.commit()
        atualizar_estoque(produto_id, quantidade)
    return True

def listar_vendas():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT v.id, c.nome, p.nome, v.quantidade, v.total, v.data_venda
            FROM vendas v
            JOIN clientes c ON v.cliente_id = c.id
            JOIN produtos p ON v.produto_id = p.id
        ''')
        return cursor.fetchall()
