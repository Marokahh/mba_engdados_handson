# ENEM: Quem não foi?

Análise de dados sobre a abstenção no Exame Nacional do Ensino Médio (ENEM), utilizando dados oficiais do INEP entre 2019 e 2023.

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

## Arquitetura

O projeto utiliza **Python/Pandas** para a extração e **PostgreSQL** para armazenamento, compilação e tratamento dos dados.

```text
Microdados ENEM 2019–2023
            │
            ▼
     Python + Pandas
            │
            ▼
       PostgreSQL
            │
      ┌─────┴─────┐
      ▼           ▼
  stg_enem     dw_enem
      │           │
      │      Dados tratados
      │           │
      └───────────┘
            │
            ▼
       Análises / BI
```

### Camadas do banco

**`stg_enem`**

Armazena os dados carregados a partir dos arquivos originais.

**`dw_enem`**

Concentra os dados compilados e tratados que serão utilizados nas análises.

## Estrutura do projeto

<img width="367" height="418" alt="image" src="https://github.com/user-attachments/assets/2dada451-9201-4207-9be1-f8729606a28c" />

### Principais arquivos

| Arquivo                  | Função                                        |
| ------------------------ | --------------------------------------------- |
| `src/config.py`          | Carrega as configurações do banco             |
| `src/database.py`        | Gerencia a conexão com o PostgreSQL           |
| `src/test_connection.py` | Testa a conexão com o banco                   |
| `src/extract.py`         | Realiza a extração e carga dos microdados     |
| `requirements.txt`       | Dependências Python                           |
| `.gitignore`             | Define arquivos que não devem ser versionados |

## Tecnologias

* **Python 3.11**
* **Pandas**
* **PostgreSQL**
* **psycopg2**
* **python-dotenv**
* **DBeaver**
* **SQL**
* **Git / GitHub**

# Como executar

## 1. Pré-requisitos

Instalou-se:

* Python 3.11 ou superior;
* PostgreSQL;
* DBeaver;
* Git.

## 2. Baixar os microdados

Baixamos os arquivos oficiais do INEP referentes aos anos 2019, 2020, 2021, 2022 e 2023.

Coloque-os em:

```text
mba_engdados_handson/dados/
```

A estrutura criada foi:

<img width="352" height="132" alt="image" src="https://github.com/user-attachments/assets/cb887ce8-597a-434f-9f2a-4c0298b17e88" />

## 3. Configuração do PostgreSQL

Criamos um banco chamado:

```text
enem
```

A conexão utilizada pelo projeto:

```text
Host: localhost
Porta: 5432
Usuário: postgres
Banco: enem
```

No banco, criou-se os schemas:

```sql
CREATE SCHEMA IF NOT EXISTS stg_enem;
CREATE SCHEMA IF NOT EXISTS dw_enem;
```

## 4. Configuração do DBeaver

Fizemos uma conexão PostgreSQL utilizando:

```text
Host: localhost
Port: 5432
Database: enem
Username: postgres
Password: SUA_SENHA
```

 **Test Connection** feito para verificar a conexão.

## 5. Instalar as dependências

Abrimos o terminal na pasta do projeto:

```powershell
cd mba_engdados_handson
```

Instalamos as dependências:

```powershell
python -m pip install -r requirements.txt
```

Validamos a instalação:

```powershell
python -c "import pandas; import psycopg2; print('Dependências OK')"
```

Resultado esperado:

```text
Dependências OK
```

## 6. Configurar o `.env`

Criação do arquivo `.env` na raiz do projeto:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=enem
DB_USER=postgres
DB_PASSWORD=NOSSA_SENHA
```

> O `.env` não foi enviado ao GitHub, pois contém credenciais.

## 7. Teste de conexão

Execução:

```powershell
python src/test_connection.py
```

Resultado esperado:

```text
Conexão com PostgreSQL realizada com sucesso!
Conexão encerrada.
```

## 8. Extração

Com os arquivos CSV em `dados/` e a conexão configurada, executou-se:

```powershell
python src/extract.py
```

O script utiliza **Pandas** para ler os arquivos e carregá-los no PostgreSQL.

Ao final, foram criadas cinco tabelas no schema `stg_enem`:

<img width="336" height="111" alt="image" src="https://github.com/user-attachments/assets/7757c99e-f6ae-41a1-b285-96583e7857a8" />

### Registros carregados

|       Ano |      Registros |
| --------: | -------------: |
|      2019 |      5.095.171 |
|      2020 |      5.783.109 |
|      2021 |      3.389.832 |
|      2022 |      3.476.105 |
|      2023 |      3.933.955 |
| **Total** | **21.678.172** |

## 9. Compilação os dados

Após a extração, os cinco anos foram reunidos em uma única tabela no `dw_enem`.

É utilizado `UNION ALL` para empilhar os registros das diferentes edições sem eliminar possíveis duplicidades.

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

Valide o total:

```sql
SELECT COUNT(*) AS total_registros
FROM dw_enem.microdados_enem_compilado_5_anos;
```

Resultado esperado:

```text
21.678.172
```

## 10. Validação dos dados por ano

```sql
SELECT
    "NU_ANO",
    COUNT(*) AS quantidade
FROM dw_enem.microdados_enem_compilado_5_anos
GROUP BY "NU_ANO"
ORDER BY "NU_ANO";
```

Resultado esperado:

<img width="253" height="122" alt="image" src="https://github.com/user-attachments/assets/d56d2466-63fe-427e-bb51-166707d8c6d9" />

## 11. Tratamento dos dados

A partir da análise do dicionário de variáveis, foram selecionadas as informações relevantes para os objetivos do projeto.

O tratamento inclui:

* Remoção de espaços extras com `TRIM()`;
* Conversão de valores vazios para `NULL`;
* Definição de tipos de dados;
* Seleção das variáveis relevantes;
* Exclusão das variáveis consideradas desnecessárias.

A criação da tabela tratada está documentada em:

```text
creations_sql.txt
```

## 12. Tabela tratada

A tabela final de análise é:

```text
dw_enem.microdados_enem_tratado
```

Ela reúne variáveis relacionadas principalmente a:

* Perfil do participante;
* Escola;
* Local de aplicação;
* Presença;
* Questionário socioeconômico.
Para recriar a tabela, utilize o SQL disponível em `creations_sql.txt`.

Valide a quantidade de registros:

```sql
SELECT COUNT(*) AS total_registros
FROM dw_enem.microdados_enem_tratado;
```

Resultado esperado:

```text
21.678.172
```

## Estrutura final do banco

<img width="382" height="218" alt="image" src="https://github.com/user-attachments/assets/2e4e0675-c566-43c1-8f76-5104e4a40c43" />

## Versionamento dos dados

Os arquivos CSV do ENEM não são armazenados no GitHub devido ao seu grande volume (~14 GB de dados).

O `.gitignore` contém:
```gitignore
dados/*.csv
```

O arquivo `.env` também não é versionado:
```gitignore
.env
```

Dessa forma, o repositório mantém apenas **código, scripts, configurações e documentação**, enquanto os dados brutos devem ser obtidos separadamente.

## Próximas etapas
Com a camada de dados estruturada, as próximas etapas do projeto serão voltadas à análise da abstenção, buscando:
* Identificar padrões de ausência;
* Comparar diferentes perfis de participantes;
* Investigar características socioeconômicas;
* Avaliar diferenças regionais;
* Comparar as edições do ENEM;
* Identificar grupos com maiores taxas de ausência;
* Transformar os resultados em insights e possíveis práticas para aumentar o comparecimento.

> **Da inscrição à ausência: o objetivo é entender quem não chegou até a prova — e o que os dados podem revelar sobre isso.**

## Fonte dos dados
**Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira — INEP**
Os microdados utilizados neste projeto são oficiais e devem ser obtidos diretamente das fontes disponibilizadas pelo INEP (https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem).
