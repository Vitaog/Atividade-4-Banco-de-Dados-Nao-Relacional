import uuid
from datetime import date

def criar_vendedor(session):
    nome_vendedor = input("Digite o nome do vendedor: ")
    data_cadastro = date.today().isoformat()

    vendedor_id = uuid.uuid4()
    query = """
        INSERT INTO Vendedor (ID, nomeVendedor, data_cadastro)
        VALUES (%s, %s, %s)
    """
    session.execute(query, (vendedor_id, nome_vendedor, data_cadastro))
    print("Vendedor criado com sucesso!")

def listar_vendedores(session):
    query_vendedores = "SELECT ID, nomeVendedor, data_cadastro FROM mercado_livre_cassandra.Vendedor"

    result_vendedores = list(session.execute(query_vendedores))  

    print("Lista de Vendedores:")
    for i, row_vendedor in enumerate(result_vendedores, start=1):
        print(f"{i}. Nome: {row_vendedor.nomevendedor}")

    selected_index = int(input("Digite o ID do vendedor para obter mais informações (0 para sair): "))

    if selected_index == 0:
        return

    vendedor_selecionado = result_vendedores[selected_index - 1]

    print("\nDetalhes do Vendedor:")
    print(f"ID: {vendedor_selecionado.id}")
    print(f"Nome: {vendedor_selecionado.nomevendedor}")
    print(f"Data de Cadastro: {vendedor_selecionado.data_cadastro}")

    query_produtos = "SELECT nomeProduto, preco, quantidadeDisponivel FROM mercado_livre_cassandra.VendedorProduto WHERE ID_vendedor = %s ALLOW FILTERING"
    produtos = list(session.execute(query_produtos, [vendedor_selecionado.id]))

    if produtos:
        print("\nProdutos Associados:")
        for produto in produtos:
            print(f"   - Produto: {produto.nomeproduto}, Preço: {produto.preco}, Quantidade Disponível: {produto.quantidadedisponivel}")
    else:
        print("\nEste vendedor não possui produtos cadastrados.")


def editar_vendedor(session):
    query = "SELECT ID, nomeVendedor, data_cadastro FROM Vendedor"

    result = list(session.execute(query))  

    print("Lista de Vendedores para Edição:")
    for i, row in enumerate(result, start=1):
        print(f"{i}. {row.nomevendedor}")

    selected_id = int(input("Digite o ID do vendedor para editar (0 para sair): "))

    if selected_id == 0:
        return

    selected_vendedor = result[selected_id - 1]

    novo_nome = input(f"Digite o novo nome para '{selected_vendedor.nomevendedor}' (pressione Enter para manter o mesmo): ")
    if not novo_nome:
        novo_nome = selected_vendedor.nomevendedor  

    query_atualizar = """
        UPDATE Vendedor SET nomeVendedor = %s WHERE ID = %s
    """
    session.execute(query_atualizar, (novo_nome, selected_vendedor.id))

    print("Vendedor atualizado com sucesso!")

def adicionar_produto(session):
    query_produtos = "SELECT ID, nomeproduto, descricao FROM Produto"
    produtos = list(session.execute(query_produtos))

    print("Lista de Produtos:")
    for i, produto in enumerate(produtos, start=1):
        print(f"{i}. {produto.nomeproduto}")

    try:
        index_produto = int(input("Digite o número do produto desejado: "))
        produto_selecionado = produtos[index_produto - 1]
    except (ValueError, IndexError):
        print("Opção inválida.")
        return

    query_vendedores = "SELECT ID, nomevendedor FROM Vendedor"
    vendedores = list(session.execute(query_vendedores))

    print("\nLista de Vendedores:")
    for i, vendedor in enumerate(vendedores, start=1):
        print(f"{i}. {vendedor.nomevendedor}")

    try:
        index_vendedor = int(input("Digite o número do vendedor desejado: "))
        vendedor_selecionado = vendedores[index_vendedor - 1]
    except (ValueError, IndexError):
        print("Opção inválida.")
        return

    descricao_produto = produto_selecionado.descricao

    preco = float(input("Digite o preço do produto: "))
    quantidade_disponivel = int(input("Digite a quantidade disponível do produto: "))

    query_inserir = """
        INSERT INTO VendedorProduto (ID, nomeproduto, nomevendedor, descricaoproduto, preco, quantidadedisponivel, id_vendedor, id_produto)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    session.execute(query_inserir, (uuid.uuid4(), produto_selecionado.nomeproduto, vendedor_selecionado.nomevendedor,
                                    descricao_produto, preco, quantidade_disponivel, vendedor_selecionado.id, produto_selecionado.id))

    print("Produto adicionado com sucesso!")

def remover_produto(session):
    query_vendedores = "SELECT ID, nomevendedor FROM Vendedor"
    vendedores = list(session.execute(query_vendedores))

    print("Lista de Vendedores:")
    for i, vendedor in enumerate(vendedores, start=1):
        print(f"{i}. {vendedor.nomevendedor}")

    index_vendedor = int(input("Digite o índice do vendedor desejado: "))
    if 1 <= index_vendedor <= len(vendedores):
        vendedor_selecionado = vendedores[index_vendedor - 1]
        id_vendedor = vendedor_selecionado.id

        query_produtos = "SELECT ID, nomeproduto FROM mercado_livre_cassandra.VendedorProduto WHERE ID_vendedor = %s ALLOW FILTERING"
        produtos = list(session.execute(query_produtos, [id_vendedor]))

        print("\nLista de Produtos do Vendedor:")
        for i, produto in enumerate(produtos, start=1):
            print(f"{i}. {produto.nomeproduto}")

        index_produto = int(input("Digite o índice do produto desejado para excluir: "))
        if 1 <= index_produto <= len(produtos):
            produto_selecionado = produtos[index_produto - 1]

            query_deletar = "DELETE FROM VendedorProduto WHERE ID = %s"
            session.execute(query_deletar, [produto_selecionado.id])

            print("Produto excluído com sucesso!")
        else:
            print("Índice de produto inválido.")
    else:
        print("Índice de vendedor inválido.")
        
def atualizar_produto(session):
    query_vendedores = "SELECT ID, nomevendedor FROM Vendedor"
    vendedores = list(session.execute(query_vendedores))

    print("Lista de Vendedores:")
    for i, vendedor in enumerate(vendedores, start=1):
        print(f"{i}. {vendedor.nomevendedor}")

    try:
        indice_vendedor = int(input("Digite o número do vendedor desejado: "))
        vendedor_selecionado = vendedores[indice_vendedor - 1]
        if not vendedor_selecionado:
            print("Vendedor não encontrado.")
            return
    except (ValueError, IndexError):
        print("Seleção inválida.")
        return

    query_produtos = "SELECT ID, nomeproduto, preco, quantidadedisponivel FROM VendedorProduto WHERE ID_vendedor = %s ALLOW FILTERING"
    produtos = list(session.execute(query_produtos, [vendedor_selecionado.id]))

    if not produtos:
        print("Este vendedor não possui produtos associados.")
        return

    print("\nLista de Produtos do Vendedor:")
    for i, produto in enumerate(produtos, start=1):
        print(f"{i}. ID: {produto.id}, Produto: {produto.nomeproduto}, Preço: {produto.preco}, Quantidade Disponível: {produto.quantidadedisponivel}")

    try:
        indice_produto = int(input("Digite o número do produto desejado para atualizar (0 para sair): "))
        if indice_produto == 0:
            return
        produto_selecionado = produtos[indice_produto - 1]
        if not produto_selecionado:
            print("Produto não encontrado.")
            return
    except (ValueError, IndexError):
        print("Seleção inválida.")
        return

    novo_preco = float(input("Digite o novo preço do produto: "))
    nova_quantidade = int(input("Digite a nova quantidade disponível do produto:"))

    query_atualizar = """
    UPDATE VendedorProduto
    SET preco = %s, quantidadedisponivel = %s
    WHERE ID = %s
    """
    session.execute(query_atualizar, (novo_preco, nova_quantidade, produto_selecionado.id))
    print("Produto atualizado com sucesso!")

def deletar_vendedor(session):
    query_vendedores = "SELECT ID, nomevendedor FROM Vendedor"
    vendedores = list(session.execute(query_vendedores))

    print("Lista de Vendedores:")
    for i, vendedor in enumerate(vendedores, start=1):
        print(f"{i}. {vendedor.nomevendedor}")

    try:
        indice_vendedor = int(input("Digite o número do vendedor desejado para excluir (0 para sair): "))
        if indice_vendedor == 0:
            return
        vendedor_selecionado = vendedores[indice_vendedor - 1]
        if not vendedor_selecionado:
            print("Vendedor não encontrado.")
            return
    except (ValueError, IndexError):
        print("Seleção inválida.")
        return

    # Selecionar os IDs dos produtos associados ao vendedor
    query_selecionar_produtos = "SELECT ID FROM VendedorProduto WHERE ID_vendedor = %s ALLOW FILTERING"
    produtos_associados = list(session.execute(query_selecionar_produtos, [vendedor_selecionado.id]))

    # Remover os produtos associados
    for produto in produtos_associados:
        query_deletar_produto = "DELETE FROM VendedorProduto WHERE ID = %s"
        session.execute(query_deletar_produto, [produto.id])

    # Depois de remover os produtos, remova o vendedor
    query_deletar_vendedor = "DELETE FROM Vendedor WHERE ID = %s"
    session.execute(query_deletar_vendedor, [vendedor_selecionado.id])

    print("Vendedor e seus produtos associados excluídos com sucesso!")
