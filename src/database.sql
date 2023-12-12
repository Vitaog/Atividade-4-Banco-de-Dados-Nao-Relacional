use mercado_livre_cassandra;

CREATE TABLE IF NOT EXISTS Usuario (
    ID UUID PRIMARY KEY,
    Nome TEXT,
    CPF TEXT,
    Rua TEXT,
    Num TEXT,
    Bairro TEXT,
    Cidade TEXT,
    Estado TEXT,
    Cep TEXT
);


CREATE TABLE IF NOT EXISTS Favoritos (
    ID UUID PRIMARY KEY,
    nomeProduto TEXT,
    preco FLOAT,
    nomeVendedor TEXT,
    descricaoProduto TEXT,
    IdUsuario UUID,
    data DATE
);


CREATE TABLE IF NOT EXISTS Produto (
    ID UUID PRIMARY KEY,
    nomeProduto TEXT,
    descricao TEXT,
    data_cadastro DATE
);


CREATE TABLE IF NOT EXISTS Vendedor (
    ID UUID PRIMARY KEY,
    nomeVendedor TEXT,
    data_cadastro DATE
);


CREATE TABLE IF NOT EXISTS VendedorProduto (
    ID UUID PRIMARY KEY,
    nomeProduto TEXT,
    nomeVendedor TEXT,
    descricaoProduto TEXT,
    preco FLOAT,
    quantidadeDisponivel INT,
    ID_vendedor UUID,
    ID_Produto UUID
);


CREATE TABLE IF NOT EXISTS Compra (
    ID UUID PRIMARY KEY,
    total_compra FLOAT,
    data_compra DATE,
    ID_Usuario UUID
);


CREATE TABLE IF NOT EXISTS CompraProduto (
    ID UUID PRIMARY KEY,
    nomeProduto TEXT,
    nomeVendedor TEXT,
    descricaoProduto TEXT,
    precoUnitario FLOAT,
    quantidade INT,
    subtotal FLOAT,
    ID_Produto UUID,
    ID_Vendedor UUID,
    ID_Compra UUID,
    ID_Usuario UUID
);

