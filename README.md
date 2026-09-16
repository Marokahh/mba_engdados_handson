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

<img width="1324" height="609" alt="arquitetura_tecnica_v2" src="https://github.com/user-attachments/assets/6aaab208-557e-489e-996a-aedba6b79d4e" />


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


### Tecnologias

- **Python 3.11**
- **PostgreSQL**
- **DBeaver**
- **Git / GitHub**
- **SQL**

### Bibliotecas Python

As bibliotecas utilizadas no projeto estão centralizadas no arquivo `requirements.txt`:

- **Pandas** — leitura, tratamento e análise dos dados;
- **psycopg2** — conexão entre Python e PostgreSQL;
- **python-dotenv** — carregamento das variáveis de ambiente do `.env`;
- **scikit-learn** — preparação dos dados, divisão treino/teste e métricas dos modelos;
- **XGBoost** — treinamento do modelo XGBoost;
- **Matplotlib** — geração das visualizações;
- **Seaborn** — geração das visualizações estatísticas.

# Como executar

## 1. Pré-requisitos

Antes de executar o projeto, é necessário ter instalado:

- Python 3.11 ou superior;
- PostgreSQL;
- DBeaver;
- Git.

As bibliotecas Python são instaladas posteriormente pelo arquivo `requirements.txt`.

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

Os arquivos CSV do ENEM não são armazenados no GitHub devido ao seu grande volume (~3 GB de dados - ~600 MB por ano).

O `.gitignore` contém:
```gitignore
dados/*.csv
```

O arquivo `.env` também não é versionado:
```gitignore
.env
```

Dessa forma, o repositório mantém apenas **código, scripts, configurações e documentação**, enquanto os dados brutos devem ser obtidos separadamente.

## Fonte dos dados
**Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira — INEP**
Os microdados utilizados neste projeto são oficiais e devem ser obtidos diretamente das fontes disponibilizadas pelo INEP (https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem).

## Análise Exploratória - Etapa 2

A análise exploratória foi realizada para entender o comportamento da ausência no ENEM entre 2019 e 2023.

Foram analisados:

- Presença e ausência por ano e por dia de prova;
- Perfil dos participantes, considerando sexo, faixa etária, renda, UF e tipo de escola;
- Estatísticas descritivas, incluindo média, mediana, desvio padrão, quartis, mínimo e máximo;
- bDistribuição da faixa etária, incluindo mediana e moda;
- Matriz de correlação de Spearman entre variáveis ordinais e a ausência;
- Análise temporal, observando a variação da ausência entre os anos;
- Identificação de possíveis anomalias nas taxas de ausência.

### Principais insights

- **2020 foi o ano com maior ausência**, chegando a **55,06%** em Ciências da Natureza.
- A taxa de ausência caiu bastante após 2020, chegando a **31,50% em 2023**.
- A ausência foi **maior no 1º dia de prova** do que no 2º dia em todos os anos analisados.
- As taxas de ausência entre **homens e mulheres foram muito próximas**.
- A **faixa etária apresentou diferenças importantes**. As maiores taxas apareceram nas faixas intermediárias, chegando a **59,07%**. Foram observadas diferenças relevantes por faixa etária, renda, UF e tipo de escola.
- A **renda familiar apresentou uma relação clara com a ausência**: as menores faixas de renda tiveram taxas maiores de ausência.
- Também foram encontradas **diferenças entre os estados**, com o Amazonas apresentando a maior taxa de ausência (**52,15%**).
- O **tipo de escola também apresentou diferenças relevantes**, com taxas de ausência de 41,75%, 30,64% e 8,44% entre os grupos analisados.
- A análise de correlação indicou associações entre faixa etária, ano de conclusão e ausência.
- A análise temporal mostrou uma forte variação da ausência em 2020, seguida de redução nos anos posteriores.
- Não foram identificadas anomalias pelo critério de z-score utilizado.

Esses resultados ajudam a identificar quais grupos apresentam maior ausência e levantam hipóteses para análises futuras, principalmente relacionadas à **renda, idade, localização e perfil escolar**.

### Script da análise

O arquivo **analise_exploratoria.py** reúne as consultas e cálculos da etapa, permitindo reproduzir os resultados diretamente a partir da tabela **dw_enem.microdados_enem_tratado**.

### Como executar

Com o ambiente virtual ativado, estando dentro de mba_engdados_handson e as dependências instaladas, execute:

```bash
python src/analise_exploratoria.py 
```

## Visualizações em gráficos
<img width="893" height="489" alt="image" src="https://github.com/user-attachments/assets/776e2c3c-1753-457b-9676-e14ff145887e" />
<img width="941" height="536" alt="image" src="https://github.com/user-attachments/assets/6415bdbc-20b7-43ba-ad29-e02de985ae5c" />
<img width="641" height="490" alt="image" src="https://github.com/user-attachments/assets/7c615cbc-3b3f-4cf4-a240-4245c3b59172" />
<img width="989" height="837" alt="image" src="https://github.com/user-attachments/assets/334dd98e-6da5-4825-b476-a70db29703a7" />
<img width="990" height="540" alt="image" src="https://github.com/user-attachments/assets/1244751f-00cc-43b0-a5d8-cfcf2a790ef5" />
<img width="1191" height="886" alt="image" src="https://github.com/user-attachments/assets/5ab385bb-b5d4-474a-a491-295d17ce56ca" />
<img width="988" height="987" alt="image" src="https://github.com/user-attachments/assets/837cd3fc-4ad8-4663-946f-002c4b581852" />
<img width="738" height="486" alt="image" src="https://github.com/user-attachments/assets/ba98d425-2ba3-4d9c-8dd8-b61febdf5b8f" />

# Modelagem - Etapa 3

## 1. Objetivo da modelagem

Nesta etapa, o objetivo foi desenvolver modelos capazes de identificar participantes que não compareceram ao ENEM.

A variável utilizada como alvo foi `TP_PRESENCA_CN`, considerando:

- `0 = Presente`
- `1 = Ausente`

A classe de maior interesse é **Ausente**, pois a proposta do projeto é identificar padrões relacionados à ausência dos participantes.

## 2. Estratégia de modelagem
Foram utilizados três tipos de abordagem:
- **Baseline:** modelo de referência, que sempre prevê a classe mais frequente.
- **Random Forest:** modelo baseado em várias árvores de decisão, utilizado para identificar relações entre as características dos participantes e a ausência.
- **XGBoost:** modelo de árvores com treinamento sequencial, utilizado como segunda abordagem de Machine Learning.

Foram desenvolvidas duas versões dos modelos de Machine Learning:
- **V1:** amostra de 200.000 registros.
- **V2:** amostra de 2.100.000 registros, aproximadamente 10% da base.

A divisão dos dados foi feita em:
- 80% para treinamento;
- 20% para teste;
- divisão estratificada;
- `random_state = 42`.

As variáveis utilizadas foram:
- `TP_SEXO`
- `TP_COR_RACA`
- `TP_ESTADO_CIVIL`
- `TP_NACIONALIDADE`
- `TP_ESCOLA`
- `TP_ENSINO`
- `IN_TREINEIRO`
- `TP_ST_CONCLUSAO`
- `TP_ANO_CONCLUIU`
- `TP_LOCALIZACAO_ESC`
- `TP_DEPENDENCIA_ADM_ESC`
- `TP_SIT_FUNC_ESC`


## 3. Decisões tomadas

* Uso do Baseline: O Baseline foi utilizado como referência para verificar o quanto os modelos de Machine Learning conseguem avançar em relação a uma estratégia simples de previsão.
* Uso de duas amostras: A V1 utiliza 200.000 registros para permitir uma primeira avaliação dos modelos com menor custo computacional.
* Na V2, a amostra foi aumentada para 2.100.000 registros para verificar se o aumento da quantidade de dados produziria uma melhora relevante no desempenho.
* Foco na classe Ausente.
* Como o objetivo do projeto é identificar participantes ausentes, foram analisadas principalmente as métricas:
    - **Precision:** entre as previsões de ausência, quantas realmente eram ausentes;
    - **Recall:** entre os participantes realmente ausentes, quantos foram identificados;
    - **F1-score:** equilíbrio entre Precision e Recall;
    - **Balanced Accuracy:** desempenho considerando as duas classes.

## 4. Resultados

| Modelo | Registros | Accuracy | Precision | Recall | F1-score | Balanced Accuracy |
|---|---:|---:|---:|---:|---:|---:|
| Baseline | 21.669.596 | 62,77% | 0,00% | 0,00% | 0,00% | 50,00% |
| Random Forest V1 | 200.000 | 63,50% | 85,31% | 63,61% | 72,88% | 63,36% |
| Random Forest V2 | 2.100.000 | 62,56% | 84,85% | 61,54% | 71,34% | 63,63% |
| XGBoost V1 | 200.000 | 63,41% | 85,73% | 63,04% | 72,65% | 63,86% |
| XGBoost V2 | 2.100.000 | 62,39% | 84,97% | 61,15% | 71,12% | 63,70% |

> As métricas de Precision, Recall e F1-score consideram **Ausente como classe positiva (`1`)**.


## 5. Insights dos resultados

Os resultados mostram que os modelos de Machine Learning apresentaram desempenho superior ao Baseline principalmente na capacidade de identificar a classe **Ausente**.

O Baseline apresenta Accuracy de **62,77%**, porém não identifica os participantes ausentes. Isso acontece porque sua estratégia consiste em sempre prever a classe mais frequente.

Nos modelos de Machine Learning, o **Recall da classe Ausente ficou próximo de 61% a 64%**, indicando que uma parcela relevante dos participantes que realmente estavam ausentes foi identificada pelo modelo.

Outro ponto observado é que o aumento da amostra de **200 mil para 2,1 milhões de registros não trouxe ganho direto de Accuracy, Recall ou F1-score**. Tanto Random Forest quanto XGBoost apresentaram resultados ligeiramente menores na V2 nessas métricas.

Por outro lado, a **Balanced Accuracy permaneceu próxima de 64% nas quatro versões**, indicando que o desempenho entre as classes ficou relativamente estável mesmo com o aumento da quantidade de dados.


## 6. Conclusão

A modelagem mostrou que as características disponíveis dos participantes possuem capacidade de contribuir para a identificação de ausências no ENEM.

Os modelos de Random Forest e XGBoost conseguiram identificar participantes ausentes, apresentando Recall acima de 60%, enquanto o Baseline não identifica essa classe.

O aumento da quantidade de dados utilizado na V2 não resultou em uma melhora direta nas principais métricas. Esse resultado indica que, para as variáveis utilizadas nesta etapa, aumentar a quantidade de registros por si só não foi suficiente para melhorar o desempenho.

A partir desses resultados, novas etapas podem explorar outras variáveis e ajustes dos modelos para buscar uma melhor identificação dos participantes ausentes.


