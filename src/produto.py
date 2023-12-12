import uuid
from datetime import date

def criar_produto(session):
    nome_produto = input("Digite o nome do produto: ")
    descricao = input("Digite a descrição do produto: ")
    data_cadastro = date.today().isoformat()

    produto_id = uuid.uuid4()
    query = """
        INSERT INTO Produto (ID, nomeProduto, descricao, data_cadastro)
        VALUES (%s, %s, %s, %s)
    """
    session.execute(query, (produto_id, nome_produto, descricao, data_cadastro))
    print("Produto criado com sucesso!")


def listar_produtos(session):
    query = "SELECT ID, nomeProduto, descricao, data_cadastro FROM Produto"

    result = list(session.execute(query))  # Converte o ResultSet para uma lista

    print("Lista de Produtos:")
    for i, row in enumerate(result, start=1):
        print(f"{i}. {row.nomeproduto}")

    selected_id = int(input("Digite o ID do produto para obter mais informações (0 para sair): "))

    if selected_id == 0:
        return

    selected_product = result[selected_id - 1]

    print("\nDetalhes do Produto:")
    print(f"ID do produto: {selected_product.id}")
    print(f"Nome: {selected_product.nomeproduto}")
    print(f"Descrição: {selected_product.descricao}")
    print(f"Data de Cadastro: {selected_product.data_cadastro}")

def editar_produto(session):
    query = "SELECT ID, nomeProduto, descricao, data_cadastro FROM Produto"

    result = list(session.execute(query))  

    print("Lista de Produtos para Edição:")
    for i, row in enumerate(result, start=1):
        print(f"{i}. {row.nomeproduto}")

    selected_id = int(input("Digite o ID do produto para editar (0 para sair): "))

    if selected_id == 0:
        return

    selected_product = result[selected_id - 1]

    novo_nome = input(f"Digite o novo nome para '{selected_product.nomeproduto}' (pressione Enter para manter o mesmo): ")
    if not novo_nome:
        novo_nome = selected_product.nomeproduto  

    nova_descricao = input(f"Digite a nova descrição para '{selected_product.descricao}' (pressione Enter para manter a mesma): ")
    if not nova_descricao:
        nova_descricao = selected_product.descricao  

    query_atualizar = """
        UPDATE Produto SET nomeProduto = %s, descricao = %s WHERE ID = %s
    """
    session.execute(query_atualizar, (novo_nome, nova_descricao, selected_product.id))

    print("Produto atualizado com sucesso!")

def deletar_produto(session):
    query = "SELECT ID, nomeProduto, descricao, data_cadastro FROM Produto"

    # Executa a consulta
    result = list(session.execute(query))  # Converte o ResultSet para uma lista

    # Exibe a lista de produtos para deleção
    print("Lista de Produtos para Deleção:")
    for i, row in enumerate(result, start=1):
        print(f"{i}. {row.nomeproduto}")

    # Solicita ao usuário selecionar um produto pelo ID para deleção
    selected_id = int(input("Digite o ID do produto para deletar (0 para sair): "))

    # Se o usuário inserir 0, sai da função
    if selected_id == 0:
        return

    # Obtém o produto selecionado pelo ID para deleção
    selected_product = result[selected_id - 1]

    # Confirmação do usuário
    confirmacao = input(f"Tem certeza que deseja deletar '{selected_product.nomeproduto}'? (S para confirmar): ")

    if confirmacao.upper() == 'S':
        # Deleta o produto do banco de dados
        query_deletar = "DELETE FROM Produto WHERE ID = %s"
        session.execute(query_deletar, (selected_product.id,))
        print("Produto deletado com sucesso!")
    else:
        print("Operação de deleção cancelada.")

