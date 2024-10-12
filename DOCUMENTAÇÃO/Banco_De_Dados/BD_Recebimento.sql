-- Criação do Enum de filiais
CREATE TYPE enum_filiais AS ENUM (
    'Jundiaí',
    'Belo Horizonte',
    'Ribeirão Preto',
    'Cuiabá',
    'Rio de Janeiro',
    'Tocantins',
    'Brasília',
    'Goiânia',
    'Curitiba'
);

-- Tabela tb_responsavel
CREATE TABLE tb_responsavel (
    id_responsavel SERIAL PRIMARY KEY,
    nome_responsavel VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    id_azure_ad VARCHAR(255) UNIQUE NOT NULL,
    permissao BOOLEAN DEFAULT FALSE,
    status BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_alteracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabela tb_responsavel_filial
CREATE TABLE tb_responsavel_filial (
    id_responsavel_filial SERIAL PRIMARY KEY,
    id_responsavel INT REFERENCES tb_responsavel(id_responsavel),
    filial enum_filiais NOT NULL,
    data_vinculacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_alteracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE (id_responsavel, filial) -- Garante que um responsável não possa ser associado mais de uma vez à mesma filial
);

-- Tabela tb_nota_fiscal
CREATE TABLE tb_nota_fiscal (
    id_nota_fiscal SERIAL PRIMARY KEY,
    chave_acesso VARCHAR(44) UNIQUE NOT NULL,
    codigo_cte VARCHAR(20),
    volumes INT CHECK (volumes >= 0 AND volumes <= 999),
    filial enum_filiais NOT NULL,
    nome_centro VARCHAR(4) NOT NULL, -- Referência ao centro como texto, não mais uma FK
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_alteracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabela tb_registro
CREATE TABLE tb_registro (
    id_registro SERIAL PRIMARY KEY,
    id_nota_fiscal INT REFERENCES tb_nota_fiscal(id_nota_fiscal),
    data_recebimento TIMESTAMP NOT NULL,
    status_registro VARCHAR(50) NOT NULL,
    data_guarda TIMESTAMP,
    prioridade BOOLEAN DEFAULT FALSE,
    id_responsavel INT REFERENCES tb_responsavel(id_responsavel),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Associações e consultas solicitadas
-- Ver registros por nota fiscal
CREATE INDEX idx_registro_nota_fiscal ON tb_registro(id_nota_fiscal);

-- Ver registros por responsável
CREATE INDEX idx_registro_responsavel ON tb_registro(id_responsavel);

-- Ver registros por filial (através da tabela de nota fiscal)
CREATE INDEX idx_nota_fiscal_filial ON tb_nota_fiscal(filial);

-- Ver notas fiscais por empresa (filial)
CREATE INDEX idx_nota_fiscal_centro ON tb_nota_fiscal(nome_centro);

-- Ver notas fiscais por responsável (associado por registros)
CREATE INDEX idx_nota_fiscal_responsavel ON tb_registro(id_responsavel);

-- Ver todas as notas fiscais por filial
CREATE INDEX idx_nota_fiscal_por_filial ON tb_nota_fiscal(filial);