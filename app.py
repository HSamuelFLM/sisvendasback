import database as db

def menu_principal():
    print("\n===== SISTEMA DE VENDAS =====")
    print("1 - Login")
    print("2 - Registrar")
    print("0 - Sair")
    return input("Escolha: ")

def menu_vendas():
    print("\n===== MENU PRINCIPAL =====")
    print("1 - Cadastrar Cliente")
    print("2 - Listar Clientes")
    print("3 - Cadastrar Produto")
    print("4 - Listar Produtos")
    print("5 - Registrar Venda")
    print("6 - Listar Vendas")
    print("0 - Sair")
    return input("Escolha: ")

def cadastrar_cliente():
    nome = input("Nome do cliente: ")
    email = input("E-mail: ")
    telefone = input("Telefone: ")
    db.cadastrar_cliente(nome, email, telefone)
    print("Cliente cadastrado com sucesso!")

def listar_clientes():
    clientes = db.listar_clientes()
    if not clientes:
        print("Nenhum cliente cadastrado.")
    else:
        print("\n--- Clientes ---")
        for c in clientes:
            print(f"ID: {c[0]} | Nome: {c[1]} | Email: {c[2]} | Telefone: {c[3]}")

def cadastrar_produto():
    nome = input("Nome do produto: ")
    preco = float(input("Preço: R$ "))
    estoque = int(input("Estoque inicial: "))
    db.cadastrar_produto(nome, preco, estoque)
    print("Produto cadastrado com sucesso!")

def listar_produtos():
    produtos = db.listar_produtos()
    if not produtos:
        print("Nenhum produto cadastrado.")
    else:
        print("\n--- Produtos ---")
        for p in produtos:
            print(f"ID: {p[0]} | Nome: {p[1]} | Preço: R${p[2]:.2f} | Estoque: {p[3]}")

def registrar_venda():
    listar_clientes()
    cliente_id = int(input("ID do cliente: "))
    listar_produtos()
    produto_id = int(input("ID do produto: "))
    quantidade = int(input("Quantidade: "))
    if db.registrar_venda(cliente_id, produto_id, quantidade):
        print("Venda registrada com sucesso!")
    else:
        print("Erro: produto não encontrado.")

def listar_vendas():
    vendas = db.listar_vendas()
    if not vendas:
        print("Nenhuma venda registrada.")
    else:
        print("\n--- Vendas realizadas ---")
        for v in vendas:
            print(f"Venda ID: {v[0]} | Cliente: {v[1]} | Produto: {v[2]} | Qtd: {v[3]} | Total: R${v[4]:.2f} | Data: {v[5]}")

def main():
    db.criar_tabelas()

    while True:
        opcao = menu_principal()
        if opcao == '1':
            login = input("Login: ")
            senha = input("Senha: ")
            if db.autenticar_usuario(login, senha):
                print(f"Bem-vindo, {login}!")
                while True:
                    sub_opcao = menu_vendas()
                    if sub_opcao == '1':
                        cadastrar_cliente()
                    elif sub_opcao == '2':
                        listar_clientes()
                    elif sub_opcao == '3':
                        cadastrar_produto()
                    elif sub_opcao == '4':
                        listar_produtos()
                    elif sub_opcao == '5':
                        registrar_venda()
                    elif sub_opcao == '6':
                        listar_vendas()
                    elif sub_opcao == '0':
                        print("Saindo...")
                        break
                    else:
                        print("Opção inválida!")
            else:
                print("Login ou senha incorretos!")
        elif opcao == '2':
            nome = input("Nome completo: ")
            login = input("Escolha um login: ")
            senha = input("Escolha uma senha: ")
            if db.registrar_usuario(nome, login, senha):
                print("Usuário registrado com sucesso!")
            else:
                print("Login já existe. Tente outro.")
        elif opcao == '0':
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
