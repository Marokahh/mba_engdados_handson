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

## Dados utilizados

O projeto utiliza os **microdados oficiais do ENEM disponibilizados pelo INEP**, considerando as edições de:

| Ano  | Arquivo                    |
| ---- | -------------------------- |
| 2019 | `MICRODADOS_ENEM_2019.csv` |
| 2020 | `MICRODADOS_ENEM_2020.csv` |
| 2021 | `MICRODADOS_ENEM_2021.csv` |
| 2022 | `MICRODADOS_ENEM_2022.csv` |
| 2023 | `MICRODADOS_ENEM_2023.csv` |

Cada arquivo representa uma edição do exame e contém informações dos participantes.

### Principais grupos de informações utilizados

* Dados demográficos
* Dados relacionados à escola
* Local de aplicação da prova
* Informações de presença
* Informações socioeconômicas
* Características familiares e domiciliares
* Informações relacionadas à inscrição

> **Observação:** os arquivos originais possuem grande volume de dados e, por isso, não são armazenados no GitHub. Eles devem ser baixados e disponibilizados localmente na pasta `dados/`.

# Arquitetura do projeto

O projeto foi estruturado seguindo uma separação entre **dados de origem (staging)** e **dados tratados para análise (data warehouse)**.

```text
                    ┌──────────────────────┐
                    │   Microdados ENEM    │
                    │      INEP 2019-2023  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       Python         │
                    │      Pandas          │
                    │      extract.py      │
                    └──────────┬───────────┘
                               │
                               ▼
                 ┌────────────────────────────┐
                 │        PostgreSQL          │
                 │                            │
                 │        stg_enem            │
                 │   Dados carregados         │
                 └────────────┬───────────────┘
                              │
                              ▼
                 ┌────────────────────────────┐
                 │        PostgreSQL          │
                 │                            │
                 │         dw_enem            │
                 │ Dados compilados/tratados  │
                 └────────────┬───────────────┘
                              │
                              ▼
                    ┌──────────────────────┐
                    │      Análises        │
                    │      e Insights      │
                    └──────────────────────┘
```

## Estrutura do projeto

```text
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
    ├── creations_sql.txt
    ├── requirements.txt
    └── README.md
```

### Principais arquivos

| Arquivo                  | Descrição                                                                   |
| ------------------------ | --------------------------------------------------------------------------- |
| `src/config.py`          | Carrega as configurações do banco a partir do `.env`                        |
| `src/database.py`        | Gerencia a conexão com o PostgreSQL                                         |
| `src/test_connection.py` | Testa a conexão entre Python e PostgreSQL                                   |
| `src/extract.py`         | Realiza a leitura e carga dos microdados                                    |
| `requirements.txt`       | Dependências Python do projeto                                              |
| `.gitignore`             | Impede o envio de arquivos sensíveis e dos grandes microdados para o GitHub |


## Tecnologias utilizadas

* **Python 3.11**
* **Pandas**
* **PostgreSQL**
* **psycopg2**
* **python-dotenv**
* **DBeaver**
* **SQL**
* **Git**
* **GitHub**

# Como executar o projeto

## 1. Pré-requisitos

Antes de iniciar, certifique-se de possuir:

* Python 3.11 ou superior
* PostgreSQL
* DBeaver
* Git

## 2. Obter os microdados do ENEM

Os microdados devem ser obtidos diretamente das fontes oficiais do INEP.
Faça o download dos arquivos correspondentes aos anos:

```text
2019
2020
2021
2022
2023
```
Após o download, coloque os arquivos dentro de:
```text
mba_engdados_handson/dados/
```
A estrutura esperada é:
```text
dados/
├── MICRODADOS_ENEM_2019.csv
├── MICRODADOS_ENEM_2020.csv
├── MICRODADOS_ENEM_2021.csv
├── MICRODADOS_ENEM_2022.csv
└── MICRODADOS_ENEM_2023.csv
```
> Os arquivos são grandes. Verifique se cada download foi concluído corretamente antes de iniciar a extração.

## 3. Configurar o PostgreSQL

Instale e configure o PostgreSQL.

Neste projeto, a conexão utiliza:

```text
Host: localhost
Porta: 5432
Usuário: postgres
Banco: enem
```
A senha deve ser a definida durante a instalação/configuração do PostgreSQL.

## 4. Criar o banco de dados
Crie um banco chamado:
```text
enem
```
Depois de criado, o banco utilizará os seguintes schemas:
```text
enem
├── dw_enem
├── public
└── stg_enem
```
Os schemas `stg_enem` e `dw_enem` representam diferentes etapas do fluxo de dados.

## 5. Configurar o DBeaver
Abra o DBeaver e crie uma nova conexão PostgreSQL.
Utilize:
```text
Host: localhost
Port: 5432
Database: enem
Username: postgres
Password: SUA_SENHA
```
Clique em **Test Connection**.
Se as configurações estiverem corretas, a conexão deverá ser estabelecida com sucesso.
Depois, crie os schemas:
```sql
CREATE SCHEMA IF NOT EXISTS stg_enem;

CREATE SCHEMA IF NOT EXISTS dw_enem;
```
Atualize o banco utilizando **Refresh**.
A estrutura esperada é:
```text
enem
├── dw_enem
├── public
└── stg_enem
```

## 6. Configurar o ambiente Python
Abra o terminal na pasta do projeto:
```powershell
cd mba_engdados_handson
```
Instale as dependências:
```powershell
python -m pip install -r requirements.txt
```
Para validar a instalação:
```powershell
python -c "import pandas; import psycopg2; print('Dependências OK')"
```
Resultado esperado:
```text
Dependências OK
```

## 7. Configurar o `.env`
Na raiz do projeto, crie um arquivo chamado:
```text
.env
```
Preencha com as informações da conexão:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=enem
DB_USER=postgres
DB_PASSWORD=SUA_SENHA
```
Substitua `SUA_SENHA` pela senha configurada no PostgreSQL.
> **Importante:** o arquivo `.env` contém informações sensíveis e não deve ser enviado ao GitHub.
O `.gitignore` do projeto já possui a regra:
```gitignore
.env
```
## 8. Testar a conexão com o banco
Antes de executar a extração, teste a conexão entre Python e PostgreSQL:
```powershell
python src/test_connection.py
```
Resultado esperado:
```text
Conexão com PostgreSQL realizada com sucesso!
Conexão encerrada.
```
Caso ocorra algum erro nessa etapa, corrija a configuração do banco antes de continuar.

## 9. Executar a extração
Com todos os requisitos configurados:
* PostgreSQL instalado;
* banco `enem` criado;
* schemas criados;
* `.env` configurado;
* dependências instaladas;
* microdados disponíveis em `dados/`;
* conexão testada;
Execute:
```powershell
python src/extract.py
```
O script processará os arquivos:
```text
2019
2020
2021
2022
2023
```
Durante a execução, o processo realiza:
1. Localização dos arquivos;
2. Leitura dos CSVs utilizando Pandas;
3. Identificação das colunas;
4. Inspeção inicial dos dados;
5. Criação das tabelas no PostgreSQL;
6. Carga dos registros no banco.

## 10. Tabelas geradas pela extração

Ao final da extração, serão criadas cinco tabelas no schema `stg_enem`:

```text
stg_enem
├── microdados_enem_2019
├── microdados_enem_2020
├── microdados_enem_2021
├── microdados_enem_2022
└── microdados_enem_2023
```

### Quantidade de registros

|       Ano |      Registros |
| --------: | -------------: |
|      2019 |      5.095.171 |
|      2020 |      5.783.109 |
|      2021 |      3.389.832 |
|      2022 |      3.476.105 |
|      2023 |      3.933.955 |
| **Total** | **21.678.172** |

> ⏱️ A execução pode levar algum tempo devido ao tamanho dos arquivos.

---

# 🔎 11. Validar as tabelas de origem

Após executar o `extract.py`, atualize o schema:

```text
stg_enem
```

As cinco tabelas deverão estar disponíveis.

Para validar a quantidade de registros de uma edição:

```sql
SELECT COUNT(*)
FROM stg_enem.microdados_enem_2019;
```

Resultado esperado:

```text
5.095.171
```

O mesmo procedimento pode ser realizado para os demais anos.

#  12. Compilar os cinco anos

Após o carregamento das cinco edições, os dados podem ser reunidos em uma única tabela.

Para isso, utilizamos `UNION ALL`.

### Por que `UNION ALL`?

O objetivo é **empilhar os registros das diferentes edições**, sem solicitar ao PostgreSQL que tente eliminar registros considerados duplicados.

Execute:

```sql
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
```

#  13. Validar a tabela compilada

Execute:

```sql
SELECT COUNT(*) AS total_registros
FROM dw_enem.microdados_enem_compilado_5_anos;
```

Resultado esperado:

```text
21.678.172
```

Esse total corresponde à soma dos registros das cinco edições:

```text
5.095.171
+ 5.783.109
+ 3.389.832
+ 3.476.105
+ 3.933.955
-----------
21.678.172
```


#  14. Validar os registros por ano

Também é importante garantir que os registros de cada edição foram carregados corretamente.

Execute:

```sql
SELECT
    "NU_ANO",
    COUNT(*) AS quantidade
FROM dw_enem.microdados_enem_compilado_5_anos
GROUP BY "NU_ANO"
ORDER BY "NU_ANO";
```

Resultado esperado:

| NU_ANO | Quantidade |
| -----: | ---------: |
|   2019 |  5.095.171 |
|   2020 |  5.783.109 |
|   2021 |  3.389.832 |
|   2022 |  3.476.105 |
|   2023 |  3.933.955 |


#  15. Tratamento dos dados

Após a análise do dicionário de variáveis, foram selecionadas as informações consideradas relevantes para os objetivos do projeto.

O tratamento dos dados contempla:

* Remoção de espaços extras utilizando `TRIM()`;
* Conversão de valores vazios para `NULL`;
* Definição de tipos de dados coerentes;
* Seleção das variáveis relevantes para a análise;
* Exclusão das variáveis consideradas desnecessárias nesta etapa.

Os valores das categorias são mantidos conforme a codificação original dos microdados.

As variáveis numéricas são convertidas para tipos numéricos no PostgreSQL, enquanto variáveis categóricas permanecem como texto.

---

# 16. Criar a tabela tratada

A tabela tratada é criada no schema `dw_enem`.

Primeiro, remova uma versão anterior, caso exista:

```sql
DROP TABLE IF EXISTS dw_enem.microdados_enem_tratado;
```

Em seguida, execute o SQL disponível no arquivo:

```text
creations_sql.txt
```

A tabela tratada considera grupos de variáveis relacionados a:

### Participante

```text
NU_INSCRICAO
NU_ANO
TP_FAIXA_ETARIA
TP_SEXO
TP_ESTADO_CIVIL
TP_COR_RACA
TP_NACIONALIDADE
TP_ST_CONCLUSAO
TP_ANO_CONCLUIU
TP_ESCOLA
TP_ENSINO
IN_TREINEIRO
```

###  Escola

```text
CO_MUNICIPIO_ESC
NO_MUNICIPIO_ESC
CO_UF_ESC
SG_UF_ESC
TP_DEPENDENCIA_ADM_ESC
TP_LOCALIZACAO_ESC
TP_SIT_FUNC_ESC
```

###  Local de aplicação

```text
CO_MUNICIPIO_PROVA
NO_MUNICIPIO_PROVA
CO_UF_PROVA
SG_UF_PROVA
```

###  Presença

```text
TP_PRESENCA_CN
TP_PRESENCA_CH
TP_PRESENCA_LC
TP_PRESENCA_MT
```

### 📝 Questionário socioeconômico

```text
Q001
Q002
Q003
Q004
Q005
Q006
...
Q025
```

> O detalhamento completo da criação da tabela e dos tipos atribuídos às colunas está disponível em `creations_sql.txt`.


#  17. Validar a tabela tratada

Após a criação da tabela, valide a quantidade de registros:

```sql
SELECT COUNT(*) AS total_registros
FROM dw_enem.microdados_enem_tratado;
```

Resultado esperado:

```text
21.678.172
```

A quantidade de participantes deve permanecer a mesma após o tratamento.


#  18. Validar os tipos das colunas

No DBeaver, acesse:

```text
dw_enem
└── microdados_enem_tratado
    └── Columns
```

Alguns exemplos de tipos esperados:

| Coluna             | Tipo      |
| ------------------ | --------- |
| `NU_ANO`           | `INTEGER` |
| `TP_FAIXA_ETARIA`  | `INTEGER` |
| `TP_SEXO`          | `VARCHAR` |
| `TP_COR_RACA`      | `INTEGER` |
| `CO_MUNICIPIO_ESC` | `VARCHAR` |
| `SG_UF_ESC`        | `VARCHAR` |
| `Q001`             | `VARCHAR` |
| `Q005`             | `INTEGER` |

---

# Estrutura final do banco

Ao final desta etapa, o banco estará organizado da seguinte forma:

```text
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
```

### `stg_enem`

Armazena os dados carregados a partir dos arquivos originais, mantendo uma camada de staging para o processo de transformação.

### `dw_enem`

Concentra os dados compilados e tratados que serão utilizados nas próximas etapas de análise.


# Fluxo do ETL

O fluxo desenvolvido até o momento pode ser resumido em:

```text
        MICRODADOS ENEM
             │
             ▼
        ┌───────────┐
        │  EXTRACT  │
        │  Python   │
        │  Pandas   │
        └─────┬─────┘
              │
              ▼
        ┌───────────┐
        │   STAGE   │
        │ stg_enem  │
        └─────┬─────┘
              │
              ▼
        ┌───────────┐
        │ TRANSFORM │
        │    SQL    │
        └─────┬─────┘
              │
              ▼
        ┌───────────┐
        │    DW     │
        │ dw_enem   │
        └─────┬─────┘
              │
              ▼
        ┌───────────┐
        │  ANÁLISE  │
        │  / BI     │
        └───────────┘
```

# Próximas etapas

Com a camada de dados estruturada, o projeto poderá avançar para a etapa analítica, buscando:

* Identificar os principais padrões de abstenção;
* Comparar presença e ausência entre diferentes perfis;
* Analisar diferenças por gênero e faixa etária;
* Investigar características socioeconômicas;
* Avaliar diferenças regionais;
* Comparar os padrões entre as edições;
* Identificar grupos com taxas de ausência mais elevadas;
* Gerar indicadores para apoiar a interpretação do fenômeno;
* Propor práticas que possam contribuir para o aumento do comparecimento ao ENEM.

O objetivo final é transformar os dados em **insights capazes de ajudar a entender onde e para quem a abstenção é mais frequente**.


# Referências de dados

Os dados utilizados neste projeto são os **microdados oficiais do Exame Nacional do Ensino Médio (ENEM)** disponibilizados pelo **Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP)**.

Os arquivos devem ser obtidos diretamente das fontes oficiais e armazenados localmente na pasta `dados/`.

# Observações sobre os arquivos de dados

Os microdados do ENEM possuem grande volume e, por isso, **não são versionados no GitHub**.

O `.gitignore` contém:

```gitignore
dados/*.csv
```

Dessa forma:

* os arquivos permanecem disponíveis localmente para execução do projeto;
* os arquivos não são enviados ao repositório;
* o código e a documentação permanecem versionados;
* novos colaboradores devem baixar os microdados separadamente.

O arquivo `.env` também não é versionado, pois contém as credenciais de acesso ao banco de dados.

