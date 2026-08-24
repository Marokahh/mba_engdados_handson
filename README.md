# ENEM: Quem não foi?

Análise de dados sobre a abstenção no Exame Nacional do Ensino Médio (ENEM), utilizando dados oficiais do INEP entre 2020 e 2025.

Projeto desenvolvido no **MBA em Engenharia de Dados do Universidade Presbiteriana Mackenzie**, nas disciplinas de **Hands-on**.

## Integrantes

- **Marina Soares de Souza** — RA 10106224
- **Paola Yêda Aude Gaudiello** — RA 10739716

### Professores

- Fabio Versolatto
- Gustavo Calixo

## Contextualização

O Exame Nacional do Ensino Médio (ENEM) é uma das principais avaliações educacionais do Brasil e possui um papel importante no acesso ao ensino superior.

Todos os anos, milhões de estudantes realizam sua inscrição para participar do exame. Porém, uma parcela desses candidatos não comparece aos dias de aplicação da prova.

Por trás de cada ausência existe um estudante que, por algum motivo, não chegou a realizar o exame. Compreender quem são esses candidatos e quais características estão presentes nesse grupo pode ajudar a entender melhor o fenômeno da abstenção.

Para isso, o projeto utilizará dados oficiais disponibilizados pelo **Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP)**, referentes às edições do ENEM entre **2020 e 2025**.

## O problema

Todos os anos, milhões de pessoas se inscrevem no ENEM pois muitos estudantes enxergam o exame não é apenas como uma avaliação, mas como a porta de entrada para uma universidade, para uma profissão e para novas oportunidades.

Porém uma parte dessas pessoas se inscreve e, por algum motivo, não chega a fazer a prova. E o que acontece depois?

Quando uma pessoa deixa de comparecer ao ENEM, não sabemos apenas que ela faltou a uma prova. Pode existir uma história por trás dessa ausência. Pode ser uma dificuldade financeira, uma questão relacionada ao local onde vive, às condições sociais, ao seu perfil demográfico, à situação da sua inscrição ou a alguma outra característica que ainda não conseguimos enxergar claramente nos dados.

E existe uma preocupação ainda maior: **será que essa ausência termina no dia da prova ou pode representar o abandono de um projeto de vida?**

Para alguns estudantes, perder uma edição do ENEM pode significar apenas tentar novamente no ano seguinte. Para outros, porém, pode significar adiar ou até desistir da ideia de cursar uma faculdade. Uma ausência que, olhando apenas para uma tabela, parece ser simplesmente um candidato que não compareceu, pode representar o fim de uma trajetória educacional que nem chegou a começar.

É justamente essa dimensão que torna o problema relevante.

O ENEM pode ser o início da carreira e de uma nova etapa na vida de muitas pessoas. Mas, para algumas delas, a ausência pode representar também o início de um afastamento dos estudos e, consequentemente, de oportunidades futuras.

## Questão central e Perguntas

Hoje sabemos quantas pessoas se inscrevem e quantas não comparecem, mas ainda precisamos entender **quem são essas pessoas**.

Será que existe um perfil de candidato mais propenso a não comparecer? A ausência está relacionada a questões financeiras? Existem diferenças entre gêneros, faixas etárias ou perfis socioeconômicos? Há regiões onde esse problema é mais frequente? A situação da inscrição ou do pagamento tem alguma relação com o comparecimento? Esses padrões se repetem ao longo dos anos ou mudam de acordo com cada edição?

Essas são algumas das perguntas que surgem quando deixamos de olhar para a abstenção apenas como um número e passamos a enxergá-la como um possível reflexo de desigualdades e dificuldades que atingem diferentes grupos de estudantes.

O grande problema, portanto, não é simplesmente **“quantas pessoas faltaram ao ENEM?”**.

É entender **quem são essas pessoas, o que existe em comum entre elas e se estamos diante de grupos que ainda não conseguimos identificar claramente**.

Por isso, este projeto parte da seguinte questão central:

> **Quem são os estudantes que se inscrevem no ENEM, mas não comparecem à prova, e quais características podem estar relacionadas a essa ausência?**

A partir dessa questão, a análise buscará responder:

* Quem são os candidatos que mais deixam de comparecer ao ENEM?
* Existe um perfil predominante entre os ausentes?
* A situação financeira ou a condição de pagamento da inscrição está relacionada à ausência?
* Existem diferenças de abstenção entre gêneros?
* A idade influencia o comparecimento?
* O perfil socioeconômico está relacionado à decisão de comparecer ou não?
* Existem regiões ou grupos específicos em que a ausência é maior?
* A situação da inscrição apresenta diferenças entre quem comparece e quem não comparece?
* Esses padrões permanecem ao longo dos anos ou mudam de uma edição para outra?
* Existem grupos que apresentam taxas de ausência consistentemente maiores?
* E, principalmente, **estamos conseguindo enxergar nos dados algum grupo de estudantes que pode estar encontrando maiores dificuldades para chegar até o ENEM?**

## Objetivo

Identificar padrões e características relacionadas à ausência dos participantes, buscando compreender os diferentes perfis envolvidos e utilizar esses insights para **propor práticas que contribuam para o aumento do comparecimento ao exame**.

## Dados

São utilizados os microdados oficiais do ENEM disponibilizados pelo INEP para os anos:

Ano	Arquivo
2019	MICRODADOS_ENEM_2019.csv
2020	MICRODADOS_ENEM_2020.csv
2021	MICRODADOS_ENEM_2021.csv
2022	MICRODADOS_ENEM_2022.csv
2023	MICRODADOS_ENEM_2023.csv

Cada arquivo contém informações dos participantes da respectiva edição do exame.

Entre as informações utilizadas na etapa de tratamento estão:

Dados demográficos;
Dados relacionados à escola;
Dados relacionados ao local de aplicação;
Informações de presença;
Informações socioeconômicas;
Informações sobre características familiares e domiciliares.

## Estrutura do projeto

A estrutura utilizada no projeto é:

ProjetoMBA_QuemNaoFoi/
│
└── mba_engdados_handson/
    │
    ├── dados/
    │   ├── MICRODADOS_ENEM_2019.csv
    │   ├── MICRODADOS_ENEM_2020.csv
    │   ├── MICRODADOS_ENEM_2021.csv
    │   ├── MICRODADOS_ENEM_2022.csv
    │   └── MICRODADOS_ENEM_2023.csv
    │
    ├── src/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── database.py
    │   ├── extract.py
    │   └── test_connection.py
    │
    ├── .env
    ├── .gitignore
    ├── requirements.txt
    └── README.md

Importante: os microdados devem estar dentro da pasta dados/ para que o extract.py consiga localizá-los.

## Pré-requisitos

Para reproduzir o projeto, é necessário instalar:

Python 3.11 ou superior;
PostgreSQL;
DBeaver;
Git, caso o projeto seja clonado do GitHub.

O projeto utiliza as seguintes bibliotecas Python:

pandas
psycopg2-binary
python-dotenv


# 1. Obter os microdados do ENEM

Os arquivos utilizados são os microdados oficiais do ENEM disponibilizados pelo INEP.

É necessário baixar os arquivos correspondentes aos anos 2019, 2020, 2021, 2022 e 2023.

Após o download, os arquivos devem ser colocados dentro da pasta:

mba_engdados_handson/dados/

A pasta deverá ficar assim:

dados/
├── MICRODADOS_ENEM_2019.csv
├── MICRODADOS_ENEM_2020.csv
├── MICRODADOS_ENEM_2021.csv
├── MICRODADOS_ENEM_2022.csv
└── MICRODADOS_ENEM_2023.csv

Os arquivos são grandes. Por isso, é importante verificar se o download foi concluído corretamente antes de iniciar a extração.

# 2. Instalar e configurar o PostgreSQL

Instale o PostgreSQL na máquina.

Durante a instalação, será definido o usuário administrador do banco, utilizado neste projeto como:

Usuário: postgres
Porta: 5432
Host: localhost

Também será definida uma senha para o usuário postgres.

Criar o banco de dados

No PostgreSQL, crie um banco chamado:

enem

O banco utilizado pelo projeto possui os seguintes schemas:

enem
├── dw_enem
├── public
└── stg_enem

Os schemas stg_enem e dw_enem serão utilizados para organizar as diferentes etapas do projeto.

# 3. Configurar o banco no DBeaver

Abra o DBeaver e crie uma nova conexão.

Selecione:

PostgreSQL

Preencha:

Host: localhost
Port: 5432
Database: enem
Username: postgres
Password: SUA_SENHA

Clique em:

Test Connection

Se as informações estiverem corretas, o DBeaver deverá informar que a conexão foi estabelecida com sucesso.

Depois de conectar ao banco enem, crie os schemas:

CREATE SCHEMA IF NOT EXISTS stg_enem;

CREATE SCHEMA IF NOT EXISTS dw_enem;

Após executar, clique em Refresh no banco.

O resultado esperado é:

enem
├── dw_enem
├── public
└── stg_enem

# 4. Configurar o ambiente Python

Abra o terminal na pasta do projeto:

cd mba_engdados_handson

Instale as dependências:

python -m pip install -r requirements.txt

Para verificar se as principais bibliotecas foram instaladas:

python -c "import pandas; import psycopg2; print('Dependências OK')"

O resultado esperado é:

Dependências OK

# 5. Configurar o arquivo .env

Na raiz de mba_engdados_handson, crie o arquivo:

.env

Ele deverá conter as informações de conexão com o PostgreSQL:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=enem
DB_USER=postgres
DB_PASSWORD=SUA_SENHA

Substitua SUA_SENHA pela senha definida para o usuário postgres.

Importante: o arquivo .env não deve ser enviado para o GitHub. Ele deve estar listado no .gitignore.

# 6. Testar a conexão com o banco

Antes de executar a extração, é importante verificar se o Python consegue acessar o PostgreSQL.

Execute:

python src/test_connection.py

Se tudo estiver configurado corretamente, o resultado será semelhante a:

Conexão com PostgreSQL realizada com sucesso!
Conexão encerrada.

Caso apareça um erro nessa etapa, a extração não deve ser iniciada. Primeiro deve ser corrigida a configuração da conexão.

# 7. Executar a extração dos microdados

Com:

PostgreSQL configurado;
banco enem criado;
schemas criados;
.env configurado;
dependências instaladas;
arquivos CSV dentro de dados/;
conexão testada;

podemos executar:

python src/extract.py

O script processará os cinco arquivos:

2019
2020
2021
2022
2023

Durante a execução, o script utiliza o Pandas para:

localizar o arquivo;
ler o CSV;
identificar as colunas;
apresentar as primeiras linhas;
apresentar os tipos identificados;
criar a tabela correspondente no PostgreSQL;
carregar os registros para o banco.

# 8. Tabelas geradas pela extração

Ao final da execução, serão criadas cinco tabelas no schema stg_enem:

stg_enem
├── microdados_enem_2019
├── microdados_enem_2020
├── microdados_enem_2021
├── microdados_enem_2022
└── microdados_enem_2023

A quantidade de registros obtida durante a execução foi:

Ano	Registros
2019	5.095.171
2020	5.783.109
2021	3.389.832
2022	3.476.105
2023	3.933.955
Total	21.678.172

A execução pode levar algum tempo devido ao tamanho dos arquivos.

# 9. Validação das tabelas de origem

Após executar o extract.py, abra o DBeaver e atualize o schema:

stg_enem

As cinco tabelas devem estar disponíveis.

Também é possível validar diretamente pelo SQL.

Por exemplo:

SELECT COUNT(*)
FROM stg_enem.microdados_enem_2019;

O resultado esperado é:

5.095.171

O mesmo procedimento pode ser realizado para os demais anos.

# 10. Compilação dos cinco anos

Depois que todas as tabelas foram carregadas no PostgreSQL, os cinco arquivos podem ser unidos em uma única tabela.

Como cada tabela representa uma edição diferente do ENEM, utilizamos UNION ALL.

Por que UNION ALL?

Não queremos que o PostgreSQL tente eliminar registros considerados duplicados.

Nosso objetivo é simplesmente empilhar os registros dos cinco anos.

Execute:

CREATE TABLE dw_enem.microdados_enem_compilado_5_anos AS

SELECT *
FROM stg_enem.microdados_enem_2019

UNION ALL

SELECT *
FROM stg_enem.microdados_enem_2020

UNION ALL

SELECT *
FROM stg_enem.microdados_enem_2021

UNION ALL

SELECT *
FROM stg_enem.microdados_enem_2022

UNION ALL

SELECT *
FROM stg_enem.microdados_enem_2023;

# 11. Validar a tabela compilada

Depois da criação, execute:

SELECT COUNT(*) AS total_registros
FROM dw_enem.microdados_enem_compilado_5_anos;

O resultado esperado é:

21.678.172

Esse número corresponde à soma dos cinco arquivos:

5.095.171
+ 5.783.109
+ 3.389.832
+ 3.476.105
+ 3.933.955
----------------
21.678.172

# 12. Validar os registros por ano

Para verificar se os cinco anos foram realmente carregados:

SELECT 
    "NU_ANO",
    COUNT(*) AS quantidade
FROM dw_enem.microdados_enem_compilado_5_anos
GROUP BY "NU_ANO"
ORDER BY "NU_ANO";

O resultado esperado é:

NU_ANO	Quantidade
2019	5.095.171
2020	5.783.109
2021	3.389.832
2022	3.476.105
2023	3.933.955

# 13. Tratamento dos dados

Após a análise do dicionário de variáveis, foi definido quais informações possuem maior valor para o projeto.

As variáveis consideradas desnecessárias para esta etapa foram removidas, enquanto as demais foram mantidas.

O tratamento realizado nesta etapa consiste em:

remover espaços extras com TRIM();
transformar valores vazios em NULL;
atribuir tipos de dados coerentes;
manter as variáveis consideradas relevantes;
eliminar as variáveis marcadas como não necessárias.

Os valores das categorias não são alterados.

As notas, quando presentes nas etapas anteriores, são tratadas como valores numéricos, porém as variáveis classificadas como não necessárias no dicionário não fazem parte da tabela tratada.

# 14. Criar a tabela tratada

No DBeaver:

DROP TABLE IF EXISTS dw_enem.microdados_enem_tratado;

CREATE TABLE dw_enem.microdados_enem_tratado AS
SELECT
    -- DADOS DO PARTICIPANTE
    TRIM("NU_INSCRICAO")::VARCHAR(20) AS "NU_INSCRICAO",
    NULLIF(TRIM("NU_ANO"), '')::INTEGER AS "NU_ANO",
    NULLIF(TRIM("TP_FAIXA_ETARIA"), '')::INTEGER AS "TP_FAIXA_ETARIA",
    NULLIF(TRIM("TP_SEXO"), '')::VARCHAR(1) AS "TP_SEXO",
    NULLIF(TRIM("TP_ESTADO_CIVIL"), '')::INTEGER AS "TP_ESTADO_CIVIL",
    NULLIF(TRIM("TP_COR_RACA"), '')::INTEGER AS "TP_COR_RACA",
    NULLIF(TRIM("TP_NACIONALIDADE"), '')::INTEGER AS "TP_NACIONALIDADE",
    NULLIF(TRIM("TP_ST_CONCLUSAO"), '')::INTEGER AS "TP_ST_CONCLUSAO",
    NULLIF(TRIM("TP_ANO_CONCLUIU"), '')::INTEGER AS "TP_ANO_CONCLUIU",
    NULLIF(TRIM("TP_ESCOLA"), '')::INTEGER AS "TP_ESCOLA",
    NULLIF(TRIM("TP_ENSINO"), '')::INTEGER AS "TP_ENSINO",
    NULLIF(TRIM("IN_TREINEIRO"), '')::INTEGER AS "IN_TREINEIRO",

    -- DADOS DA ESCOLA
    NULLIF(TRIM("CO_MUNICIPIO_ESC"), '')::VARCHAR(10) AS "CO_MUNICIPIO_ESC",
    NULLIF(TRIM("NO_MUNICIPIO_ESC"), '')::VARCHAR(150) AS "NO_MUNICIPIO_ESC",
    NULLIF(TRIM("CO_UF_ESC"), '')::INTEGER AS "CO_UF_ESC",
    NULLIF(TRIM("SG_UF_ESC"), '')::VARCHAR(2) AS "SG_UF_ESC",
    NULLIF(TRIM("TP_DEPENDENCIA_ADM_ESC"), '')::INTEGER AS "TP_DEPENDENCIA_ADM_ESC",
    NULLIF(TRIM("TP_LOCALIZACAO_ESC"), '')::INTEGER AS "TP_LOCALIZACAO_ESC",
    NULLIF(TRIM("TP_SIT_FUNC_ESC"), '')::INTEGER AS "TP_SIT_FUNC_ESC",

    -- LOCAL DE APLICAÇÃO DA PROVA
    NULLIF(TRIM("CO_MUNICIPIO_PROVA"), '')::VARCHAR(10) AS "CO_MUNICIPIO_PROVA",
    NULLIF(TRIM("NO_MUNICIPIO_PROVA"), '')::VARCHAR(150) AS "NO_MUNICIPIO_PROVA",
    NULLIF(TRIM("CO_UF_PROVA"), '')::INTEGER AS "CO_UF_PROVA",
    NULLIF(TRIM("SG_UF_PROVA"), '')::VARCHAR(2) AS "SG_UF_PROVA",

    -- PRESENÇA
    NULLIF(TRIM("TP_PRESENCA_CN"), '')::INTEGER AS "TP_PRESENCA_CN",
    NULLIF(TRIM("TP_PRESENCA_CH"), '')::INTEGER AS "TP_PRESENCA_CH",
    NULLIF(TRIM("TP_PRESENCA_LC"), '')::INTEGER AS "TP_PRESENCA_LC",
    NULLIF(TRIM("TP_PRESENCA_MT"), '')::INTEGER AS "TP_PRESENCA_MT",

    -- QUESTIONÁRIO SOCIOECONÔMICO
    NULLIF(TRIM("Q001"), '')::VARCHAR(2) AS "Q001",
    NULLIF(TRIM("Q002"), '')::VARCHAR(2) AS "Q002",
    NULLIF(TRIM("Q003"), '')::VARCHAR(2) AS "Q003",
    NULLIF(TRIM("Q004"), '')::VARCHAR(2) AS "Q004",
    NULLIF(TRIM("Q005"), '')::INTEGER AS "Q005",
    NULLIF(TRIM("Q006"), '')::VARCHAR(2) AS "Q006",
    NULLIF(TRIM("Q007"), '')::VARCHAR(2) AS "Q007",
    NULLIF(TRIM("Q008"), '')::VARCHAR(2) AS "Q008",
    NULLIF(TRIM("Q009"), '')::VARCHAR(2) AS "Q009",
    NULLIF(TRIM("Q010"), '')::VARCHAR(2) AS "Q010",
    NULLIF(TRIM("Q011"), '')::VARCHAR(2) AS "Q011",
    NULLIF(TRIM("Q012"), '')::VARCHAR(2) AS "Q012",
    NULLIF(TRIM("Q013"), '')::VARCHAR(2) AS "Q013",
    NULLIF(TRIM("Q014"), '')::VARCHAR(2) AS "Q014",
    NULLIF(TRIM("Q015"), '')::VARCHAR(2) AS "Q015",
    NULLIF(TRIM("Q016"), '')::VARCHAR(2) AS "Q016",
    NULLIF(TRIM("Q017"), '')::VARCHAR(2) AS "Q017",
    NULLIF(TRIM("Q018"), '')::VARCHAR(2) AS "Q018",
    NULLIF(TRIM("Q019"), '')::VARCHAR(2) AS "Q019",
    NULLIF(TRIM("Q020"), '')::VARCHAR(2) AS "Q020",
    NULLIF(TRIM("Q021"), '')::VARCHAR(2) AS "Q021",
    NULLIF(TRIM("Q022"), '')::VARCHAR(2) AS "Q022",
    NULLIF(TRIM("Q023"), '')::VARCHAR(2) AS "Q023",
    NULLIF(TRIM("Q024"), '')::VARCHAR(2) AS "Q024",
    NULLIF(TRIM("Q025"), '')::VARCHAR(2) AS "Q025"

FROM dw_enem.microdados_enem_compilado_5_anos;

# 15. Validar a tabela tratada

Depois de executar o SQL, confira a quantidade de registros:

SELECT COUNT(*) AS total_registros
FROM dw_enem.microdados_enem_tratado;

O resultado esperado continua sendo:

21.678.172

Isso é importante porque a etapa de limpeza não deve alterar a quantidade de participantes.

# 16. Conferir os tipos das colunas

No DBeaver:

dw_enem
└── microdados_enem_tratado
    └── Columns

Confira se os tipos das colunas correspondem aos definidos no SQL.

Exemplos:

NU_ANO              INTEGER
TP_FAIXA_ETARIA     INTEGER
TP_SEXO             VARCHAR
TP_COR_RACA         INTEGER
CO_MUNICIPIO_ESC    VARCHAR
SG_UF_ESC           VARCHAR
Q001                VARCHAR
Q005                INTEGER

# Estrutura final do banco

Ao final desta etapa, o banco estará organizado aproximadamente da seguinte maneira:

enem
│
├── stg_enem
│   ├── microdados_enem_2019
│   ├── microdados_enem_2020
│   ├── microdados_enem_2021
│   ├── microdados_enem_2022
│   └── microdados_enem_2023
│
└── dw_enem
    ├── microdados_enem_compilado_5_anos
    └── microdados_enem_tratado

A camada stg_enem mantém os dados carregados a partir dos arquivos originais.

A camada dw_enem concentra os dados compilados e tratados que serão utilizados nas próximas etapas do projeto.

# Tecnologias utilizadas
Python 3.11
Pandas
PostgreSQL
psycopg2
python-dotenv
DBeaver
SQL
Git / GitHub