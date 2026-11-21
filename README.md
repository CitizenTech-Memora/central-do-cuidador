<div align="center">

# 💊 Memora · Central do Cuidador

**Onde a família acompanha, pelo terminal, os remédios de uma pessoa idosa com Alzheimer**

Cadastro de remédios e horários, registro de cada retirada, resumo da semana, aviso de estoque baixo e rede de contatos, com os dados salvos em JSON.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![JSON](https://img.shields.io/badge/dados-JSON-555555?style=flat-square&logo=json&logoColor=white)
![Sem dependências](https://img.shields.io/badge/depend%C3%AAncias-nenhuma-2E7D32?style=flat-square)

<sub>Computational Thinking with Python · Global Solution 2026.2 · CitizenTech · FIAP</sub>

</div>

---

## Sobre o projeto

Para quem cuida de alguém com Alzheimer, uma das perguntas mais repetidas do dia é: *"será que ela tomou o remédio?"*. A pessoa idosa nem sempre lembra se já tomou, e a família, muitas vezes longe, fica sem ter certeza.
 
O **Memora** nasceu para responder a essa pergunta. A solução completa reúne uma caixa de remédios inteligente, que lembra a pessoa na hora certa, e a **Central do Cuidador**, onde a família acompanha o que aconteceu com cada dose.
 
Este repositório traz a **Central do Cuidador em Python**, com um menu no terminal. Nela, o cuidador cadastra a pessoa acompanhada, os remédios e os horários, registra cada retirada e consulta um resumo da semana: quantas doses foram retiradas no horário, quantas atrasaram e quantas ficaram para trás. A Central também avisa quando o remédio está acabando e guarda a rede de contatos da família, em ordem de prioridade.
 
O objetivo é simples: trocar a dúvida por informação, para que a família saiba quando está tudo bem e perceba rápido quando algo precisa de atenção.

## Como o Memora funciona

O funcionamento começa com o cadastro da pessoa acompanhada. Depois, o cuidador informa os medicamentos, a dosagem, os horários previstos, a quantidade disponível e a data de início do acompanhamento.

A partir desses cadastros, o programa permite registrar o que aconteceu com cada dose:

- **Retirada no horário:** quando o medicamento foi retirado com até 20 minutos de atraso.
- **Retirada com atraso:** quando a retirada ocorreu depois desse período.
- **Não retirada:** quando o cuidador registra que a dose não foi retirada.
- **Tentativa fora do horário:** registro simulado de uma tentativa de acesso em outro horário.

Essas informações são usadas para mostrar as doses do dia e produzir um resumo dos últimos sete dias. O sistema também acompanha a quantidade de medicamentos disponível e mantém uma lista de contatos de familiares e cuidadores.

> **Importante:** nesta versão, os acontecimentos são informados manualmente. O programa registra a *retirada* do medicamento, não confirma que ele foi ingerido.

## Funcionalidades

| Opção | Funcionalidade |
|-------|----------------|
| [1] | Cadastrar pessoa que será acompanhada |
| [2] | Cadastrar remédio e horários: nome, dosagem, horários, estoque e início do acompanhamento |
| [3] | Registrar retirada ou falta de retirada de uma dose |
| [4] | Ver os remédios de hoje e a situação de cada dose |
| [5] | Ver resumo dos últimos 7 dias, com porcentagem de retiradas no horário e opção de exportar |
| [6] | Ver remédios que estão acabando (estoque estimado de cinco dias ou menos) |
| [7] | Ver ou cadastrar contatos, organizados por ordem de prioridade |
| [8] | Criar exemplo para testar, com uma pessoa e registros fictícios |
| [9] | Apagar pessoa cadastrada e seus dados relacionados, após confirmação |
| [10] | Apagar remédio cadastrado e seus registros, após confirmação |
| [11] | Atualizar a quantidade de remédios disponível |
| [0] | Sair do programa |

O menu é dividido em **Cadastros**, **Acompanhamento** e **Outras opções** para facilitar a navegação.

## Exemplo de utilização

Imagine que uma cuidadora acompanha Dona Lurdes, que possui um medicamento programado para **08:00 e 14:00**.

1. A cuidadora cadastra Dona Lurdes na opção **[1]**.
2. Na opção **[2]**, cadastra o medicamento, seus horários e a quantidade disponível.
3. Ao longo do dia, usa a opção **[3]** para registrar se cada dose foi retirada, retirada com atraso ou não retirada.
4. Na opção **[4]**, consulta quais doses já foram registradas e quais ainda estão pendentes.
5. Na opção **[5]**, acompanha o resumo dos últimos sete dias.
6. Na opção **[6]**, verifica se está chegando a hora de repor o medicamento.

Para uma apresentação rápida, a **opção [8]** cria automaticamente um exemplo com **Dona Lurdes**, o **Remédio A**, dois contatos e registros fictícios dos seis dias anteriores. Assim, é possível consultar o relatório sem fazer todos os cadastros manualmente. O exemplo não é duplicado se já existir.

## Como executar

### Pré-requisitos

- Python 3.10 ou superior instalado
  Verifique com: `python --version` ou `python3 --version`
- Não é necessário instalar bibliotecas externas.

### Pelo terminal

```bash
# Clone o repositório
git clone https://github.com/CitizenTech-Memora/central-do-cuidador.git

# Entre na pasta
cd central-do-cuidador

# Execute
python Memora.py    # Windows (ou: py Memora.py)
python3 Memora.py   # Linux / Mac
```

<details>
<summary><b>Pelo PyCharm</b></summary>

1. Abra o PyCharm e clique em **File > Open**
2. Selecione a pasta do projeto (central-do-cuidador)
3. Aguarde o PyCharm indexar os arquivos
4. No painel lateral, clique com o botão direito em `Memora.py`
5. Clique em **Run 'Memora'**
6. O terminal integrado abrirá na parte inferior com o programa rodando

</details>

<details>
<summary><b>Pelo VS Code</b></summary>

1. Abra o VS Code e clique em **File > Open Folder**
2. Selecione a pasta do projeto (central-do-cuidador)
3. Instale a extensão Python da Microsoft, se ainda não tiver
   (Extensões > pesquisar "Python" > instalar)
4. Abra o arquivo `Memora.py`
5. Clique no botão **▶ Run Python File** no canto superior direito ou use o atalho `Ctrl + F5`
6. O terminal integrado abrirá na parte inferior com o programa rodando

</details>

Para selecionar uma funcionalidade, basta digitar o número da opção e pressionar **Enter**. As datas seguem o formato brasileiro **DD/MM/AAAA**; quando o programa oferece essa possibilidade, pressionar **Enter** utiliza a data de hoje.

## Estrutura

```
central-do-cuidador/
├── Memora.py            ← Arquivo principal com todo o código
├── README.md            ← Este arquivo
└── prompts.md           ← Uso de inteligência artificial no projeto
```

## Organização interna do código

<details>
<summary><b>Ver as funções do <code>Memora.py</code></b></summary>

```
Memora.py
│
├── Configuração
│   ├── ARQUIVO_DADOS ← caminho do dados.json
│   ├── ARQUIVO_RELATORIO ← caminho do relatorio.json
│   ├── TOLERANCIA_MINUTOS ← 20 minutos para considerar a dose no horário
│   └── MENU_OPCOES ← tupla com as opções do menu
│
├── Persistência de dados
│   ├── dados_vazios() ← estrutura inicial com pessoas, remédios, eventos e contatos
│   ├── carregar_dados() ← lê e valida o dados.json ao iniciar o programa
│   └── salvar_dados() ← grava as alterações com segurança no dados.json
│
├── Entradas do usuário
│   ├── pedir_texto() ← não deixa o texto ficar vazio
│   ├── pedir_numero() ← valida um número dentro de um intervalo
│   ├── pedir_confirmacao() ← pede confirmação (s/n) antes de ações irreversíveis
│   ├── pedir_data() ← valida datas no formato DD/MM/AAAA e bloqueia datas futuras
│   └── pedir_lista_horarios() ← lê e valida os horários no formato HH:MM
│
├── Funções auxiliares
│   ├── formatar_data() ← converte a data para o formato brasileiro
│   ├── validar_horario() ← confere se o horário é válido
│   ├── gerar_novo_id() ← cria o próximo número de cadastro
│   ├── escolher_item() ← lista e devolve a pessoa ou o remédio escolhido
│   └── verificar_evento_existente() ← impede dois registros para a mesma dose
│
├── Funcionalidades do menu
│   ├── cadastrar_pessoa()
│   ├── cadastrar_remedio()
│   ├── registrar_evento() ← retirada, atraso, falta ou tentativa fora do horário
│   ├── mostrar_doses_hoje()
│   ├── gerar_relatorio() ← resumo dos últimos 7 dias e exportação
│   ├── verificar_estoque() ← avisa quando o remédio está acabando
│   ├── gerenciar_contatos() ← rede de cuidado por ordem de prioridade
│   ├── criar_exemplo() ← dados fictícios para demonstração
│   ├── excluir_pessoa()
│   ├── excluir_remedio()
│   └── atualizar_estoque()
│
└── main() ← loop principal do programa
```

</details>

## Dados salvos

O Memora utiliza arquivos **JSON** para guardar as informações entre uma execução e outra:

- **`dados.json`:** armazena pessoas, medicamentos, horários, estoque, registros de doses e contatos. É criado automaticamente após a primeira alteração salva.
- **`relatorio.json`:** é criado quando o usuário escolhe exportar o resumo da opção [5].

Esses arquivos ficam na **mesma pasta do `Memora.py`**. Ao iniciar, o programa lê os cadastros já existentes. Após alterações, salva as novas informações para que continuem disponíveis quando o programa for aberto novamente.

O sistema valida números, datas e horários, impede registros duplicados da mesma dose e solicita confirmação antes de excluir cadastros. Se o arquivo de dados estiver inválido, o programa interrompe a execução para evitar sobrescrever as informações antigas.

> **Atenção:** excluir uma pessoa ou um medicamento também apaga seus registros relacionados. É recomendável fazer uma cópia do `dados.json` antes de testar exclusões.

## Limitações desta versão

A Central do Cuidador é um **protótipo acadêmico executado no terminal**. Nesta versão:

- Não existe comunicação automática com a caixa física ou com o ESP32.
- Os eventos de retirada são registrados manualmente pelo cuidador.
- Os contatos ficam cadastrados, mas o programa não envia mensagens ou alertas automaticamente.
- A estimativa de estoque considera uma unidade por horário cadastrado.
- O sistema não confirma a ingestão do medicamento e não substitui acompanhamento médico.

## Tecnologias utilizadas

- **Python 3.10+:** funcionamento do programa e menu interativo.
- **JSON:** armazenamento dos cadastros e relatórios.
- **Bibliotecas padrão `json`, `os` e `datetime`:** arquivos, datas e horários.

## Equipe

| Nome | RM |
|---|---|
| Eric Kang | 572575 |
| Guilherme Tomé Nogueira | 570144 |
| Lucas de Andrade Astorini | 569119 |
| Sabrina Lopes da Silva | 571870 |
| Sofia Satomi Hagio | 569120 |
