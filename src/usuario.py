import uuid

def criar_usuario(session):
    nome = input("Digite o nome do usuário: ")
    cpf = input("Digite o CPF do usuário: ")
    rua = input("Digite o nome da rua: ")
    num = input("Digite o número do endereço: ")
    bairro = input("Digite o bairro: ")
    cidade = input("Digite a cidade: ")
    estado = input("Digite o estado: ")
    cep = input("Digite o CEP: ")

    usuario_id = uuid.uuid4()
    query = """
        INSERT INTO Usuario (ID, Nome, CPF, Rua, Num, Bairro, Cidade, Estado, Cep)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    session.execute(query, (usuario_id, nome, cpf, rua, num, bairro, cidade, estado, cep))
    print("Usuário criado com sucesso!")

def listar_usuarios(session):
    query_usuarios = "SELECT ID, Nome FROM Usuario"

    result_usuarios = list(session.execute(query_usuarios))

    print("Lista de Usuários:")
    for i, row_usuario in enumerate(result_usuarios, start=1):
        print(f"{i}. Nome: {row_usuario.nome}")

    selected_index = int(input("Digite o ID do usuário para obter mais informações (0 para sair): "))

    if selected_index == 0:
        return

    usuario_selecionado = result_usuarios[selected_index - 1]

    print("\nDetalhes do Usuário:")
    print(f"ID: {usuario_selecionado.id}")
    print(f"Nome: {usuario_selecionado.nome}")
    
    query_endereco = """
        SELECT Rua, Num, Bairro, Cidade, Estado, Cep, Cpf
        FROM Usuario
        WHERE ID = %s
    """
    endereco_usuario = session.execute(query_endereco, [usuario_selecionado.id]).one()
    
    print(f"CPF: {endereco_usuario.cpf}")

    print("Endereço:")
    print(f"Rua: {endereco_usuario.rua}")
    print(f"Número: {endereco_usuario.num}")
    print(f"Bairro: {endereco_usuario.bairro}")
    print(f"Cidade: {endereco_usuario.cidade}")
    print(f"Estado: {endereco_usuario.estado}")
    print(f"CEP: {endereco_usuario.cep}")

def editar_usuario(session):
    query_usuarios = "SELECT * FROM Usuario"

    result_usuarios = list(session.execute(query_usuarios))

    print("Lista de Usuários para Edição:")
    for i, row_usuario in enumerate(result_usuarios, start=1):
        print(f"{i}. Nome: {row_usuario.nome}")

    selected_id = int(input("Digite o ID do usuário para editar (0 para sair): "))

    if selected_id == 0:
        return

    selected_usuario = result_usuarios[selected_id - 1]

    novo_nome = input(f"Digite o novo nome para '{selected_usuario.nome}' (pressione Enter para manter o mesmo): ")
    if not novo_nome:
        novo_nome = selected_usuario.nome

    novo_rua = input(f"Digite a nova rua para '{selected_usuario.rua}' (pressione Enter para manter o mesmo): ")
    if not novo_rua:
        novo_rua = selected_usuario.rua

    novo_num = input(f"Digite o novo número para '{selected_usuario.num}' (pressione Enter para manter o mesmo): ")
    if not novo_num:
        novo_num = selected_usuario.num

    novo_bairro = input(f"Digite o novo bairro para '{selected_usuario.bairro}' (pressione Enter para manter o mesmo): ")
    if not novo_bairro:
        novo_bairro = selected_usuario.bairro

    nova_cidade = input(f"Digite a nova cidade para '{selected_usuario.cidade}' (pressione Enter para manter o mesmo): ")
    if not nova_cidade:
        nova_cidade = selected_usuario.cidade

    novo_estado = input(f"Digite o novo estado para '{selected_usuario.estado}' (pressione Enter para manter o mesmo): ")
    if not novo_estado:
        novo_estado = selected_usuario.estado

    novo_cep = input(f"Digite o novo CEP para '{selected_usuario.cep}' (pressione Enter para manter o mesmo): ")
    if not novo_cep:
        novo_cep = selected_usuario.cep

    query_atualizar = """
        UPDATE Usuario
        SET Nome = %s, Rua = %s, Num = %s, Bairro = %s, Cidade = %s, Estado = %s, Cep = %s
        WHERE ID = %s
    """
    session.execute(query_atualizar, (novo_nome, novo_rua, novo_num, novo_bairro, nova_cidade, novo_estado, novo_cep, selected_usuario.id))

    print("Usuário atualizado com sucesso!")


import uuid
from datetime import date

def adicionar_favoritos(session):
    # Listar usuários
    query_usuarios = "SELECT ID, Nome FROM Usuario"
    result_usuarios = list(session.execute(query_usuarios))

    print("Lista de Usuários:")
    for i, row_usuario in enumerate(result_usuarios, start=1):
        print(f"{i}. Nome: {row_usuario.nome}")

    try:
        index_usuario = int(input("Digite o número do usuário desejado: "))
        usuario_selecionado = result_usuarios[index_usuario - 1]
    except (ValueError, IndexError):
        print("Seleção inválida.")
        return

    # Listar produtos
    query_produtos = "SELECT * FROM Produto"
    produtos = list(session.execute(query_produtos))

    print("\nLista de Produtos:")
    for i, produto in enumerate(produtos, start=1):
        print(f"{i}. {produto.nomeproduto}")

    try:
        index_produto = int(input("Digite o número do produto desejado: "))
        produto_selecionado = produtos[index_produto - 1]
    except (ValueError, IndexError):
        print("Seleção inválida.")
        return

    # Listar vendedores com o produto associado
    query_vendedores = "SELECT * FROM VendedorProduto WHERE ID_Produto = %s ALLOW FILTERING"
    vendedores = list(session.execute(query_vendedores, [produto_selecionado.id]))

    if not vendedores:
        print("Nenhum vendedor encontrado com o produto selecionado.")
        return

    print("\nLista de Vendedores com o Produto Associado:")
    for i, vendedor in enumerate(vendedores, start=1):
        print(f"{i}. {vendedor.nomevendedor}")

    try:
        index_vendedor = int(input("Digite o número do vendedor desejado: "))
        vendedor_selecionado = vendedores[index_vendedor - 1]
    except (ValueError, IndexError):
        print("Seleção inválida.")
        return

    # Adicionar aos Favoritos
    favorito_id = uuid.uuid4()
    data_atual = date.today().isoformat()

    query_adicionar_favorito = """
        INSERT INTO Favoritos (ID, nomeProduto, preco, nomeVendedor, descricaoProduto, IdUsuario, data)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    session.execute(query_adicionar_favorito, (
        favorito_id,
        produto_selecionado.nomeproduto,
        vendedor_selecionado.preco,
        vendedor_selecionado.nomevendedor,
        vendedor_selecionado.descricaoproduto,
        usuario_selecionado.id,
        data_atual
    ))

    print("Produto adicionado aos favoritos com sucesso!")

def remover_favoritos(session):
    query_usuarios = "SELECT ID, Nome FROM Usuario"
    result_usuarios = list(session.execute(query_usuarios))

    print("Lista de Usuários:")
    for i, row_usuario in enumerate(result_usuarios, start=1):
        print(f"{i}. Nome: {row_usuario.nome}")

    try:
        index_usuario = int(input("Digite o número do usuário desejado: "))
        usuario_selecionado = result_usuarios[index_usuario - 1]
    except (ValueError, IndexError):
        print("Seleção inválida.")
        return

    query_favoritos = "SELECT ID, nomeProduto, preco, nomeVendedor, descricaoProduto FROM Favoritos WHERE IdUsuario = %s ALLOW FILTERING"
    favoritos = list(session.execute(query_favoritos, [usuario_selecionado.id]))

    if not favoritos:
        print("Este usuário não possui favoritos.")
        return

    print("\nLista de Favoritos:")
    for i, favorito in enumerate(favoritos, start=1):
        print(f"{i}. Produto: {favorito.nomeproduto}, Preço: {favorito.preco}, Vendedor: {favorito.nomevendedor}")

    try:
        index_favorito = int(input("Digite o número do favorito desejado para remover (0 para sair): "))
        if index_favorito == 0:
            return
        favorito_selecionado = favoritos[index_favorito - 1]
    except (ValueError, IndexError):
        print("Seleção inválida.")
        return

    query_remover_favorito = "DELETE FROM Favoritos WHERE ID = %s"
    session.execute(query_remover_favorito, [favorito_selecionado.id])

    print("Favorito removido com sucesso!")

def adicionar_compra(session):
    # Listar usuários
    query_usuarios = "SELECT ID, Nome FROM Usuario"
    result_usuarios = list(session.execute(query_usuarios))

    print("Lista de Usuários:")
    for i, row_usuario in enumerate(result_usuarios, start=1):
        print(f"{i}. Nome: {row_usuario.nome}")

    try:
        index_usuario = int(input("Digite o número do usuário desejado: "))
        usuario_selecionado = result_usuarios[index_usuario - 1]
    except (ValueError, IndexError):
        print("Seleção inválida.")
        return

    # Listar produtos
    query_produtos = "SELECT * FROM Produto"
    produtos = list(session.execute(query_produtos))

    print("\nLista de Produtos:")
    for i, produto in enumerate(produtos, start=1):
        print(f"{i}. {produto.nomeproduto}")

    try:
        index_produto = int(input("Digite o número do produto desejado: "))
        produto_selecionado = produtos[index_produto - 1]
    except (ValueError, IndexError):
        print("Seleção inválida.")
        return

    # Listar vendedores com o produto associado
    query_vendedores = "SELECT * FROM VendedorProduto WHERE ID_Produto = %s ALLOW FILTERING"
    vendedores = list(session.execute(query_vendedores, [produto_selecionado.id]))

    if not vendedores:
        print("Nenhum vendedor encontrado com o produto selecionado.")
        return

    print("\nLista de Vendedores com o Produto Associado:")
    for i, vendedor in enumerate(vendedores, start=1):
        print(f"{i}. {vendedor.nomevendedor}")

    try:
        index_vendedor = int(input("Digite o número do vendedor desejado: "))
        vendedor_selecionado = vendedores[index_vendedor - 1]
    except (ValueError, IndexError):
        print("Seleção inválida.")
        return

    # Perguntar sobre a quantidade
    try:
        quantidade = int(input(f"Digite a quantidade desejada do produto '{produto_selecionado.nomeproduto}' (0 para cancelar): "))
        if quantidade == 0:
            return
    except ValueError:
        print("Quantidade inválida.")
        return

    # Calcular subtotal
    subtotal = quantidade * vendedor_selecionado.preco

    # Adicionar à tabela Compra
    compra_id = uuid.uuid4()
    total_compra = subtotal
    data_compra = date.today().isoformat()

    query_adicionar_compra = """
        INSERT INTO Compra (ID, total_compra, data_compra)
        VALUES (%s, %s, %s)
    """
    session.execute(query_adicionar_compra, (compra_id, total_compra, data_compra))

    # Adicionar à tabela CompraProduto
    compra_produto_id = uuid.uuid4()

    query_adicionar_compra_produto = """
        INSERT INTO CompraProduto (ID, nomeProduto, nomeVendedor, descricaoProduto, precoUnitario, quantidade, subtotal, ID_Produto, ID_Vendedor, ID_Compra)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    session.execute(query_adicionar_compra_produto, (
        compra_produto_id,
        produto_selecionado.nomeproduto,
        vendedor_selecionado.nomevendedor,
        vendedor_selecionado.descricaoproduto,
        vendedor_selecionado.preco,
        quantidade,
        subtotal,
        produto_selecionado.id,
        vendedor_selecionado.id,
        compra_id
    ))

    print("Compra adicionada com sucesso!")
