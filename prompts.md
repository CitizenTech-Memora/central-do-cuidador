# Uso de inteligência artificial

Este arquivo documenta como as ferramentas de inteligência artificial foram usadas no desenvolvimento da Central do Cuidador em Python.

## 1. Ferramentas utilizadas e finalidades

| Ferramenta | Empresa | Para que usamos |
|------------|---------|-----------------|
| **ChatGPT** | OpenAI | Tirar dúvidas de Python, revisar trechos do código e encontrar erros |
| **Claude** | Anthropic | Revisar a lógica do programa e simplificar mensagens para o usuário |

## 2. Prompts utilizados

Abaixo estão os principais pedidos feitos às ferramentas durante o desenvolvimento:

1. **Exclusão de cadastros**
   > "No nosso programa em Python, como adicionar opções para excluir uma pessoa ou um remédio e atualizar o arquivo JSON, apagando também os registros ligados a eles?"

2. **Dados de exemplo**
   > "Crie uma opção 8 no menu que gere dados fictícios para teste: uma pessoa, um remédio com dois horários, dois contatos e registros dos últimos seis dias."

3. **Formato das datas**
   > "As datas estão aparecendo invertidas (AAAA-MM-DD). Como mostrar e pedir as datas no formato brasileiro DD/MM/AAAA, mas continuar salvando no JSON de forma organizada?"

4. **Revisão de erros**
   > "Identifique os erros e as situações em que este código pode quebrar ou salvar dados errados."

## 3. Funcionalidades desenvolvidas, sugeridas ou modificadas com auxílio da IA

- Proteção para não sobrescrever o `dados.json` quando ele estiver inválido.
- Opções para excluir pessoas e remédios com confirmação, apagando também os registros relacionados.
- Opção 8, que cria uma pessoa fictícia, um remédio e acontecimentos simulados para demonstração.
- Regras para evitar dois registros para a mesma dose e impedir a retirada quando o estoque está zerado.
- Verificação para não registrar acontecimentos em datas ou horários futuros.
- Resumo semanal que separa retiradas no horário, atrasos, faltas e doses sem registro.
- Exibição das datas no formato brasileiro (DD/MM/AAAA).

## 4. Como verificamos, testamos e ajustamos os resultados

Nenhuma sugestão da IA foi colada direto no projeto sem revisão. Para cada mudança, seguimos estes passos:

1. **Leitura e entendimento:** antes de usar um trecho sugerido, o grupo lia o código e conferia se entendia cada linha. O que usava recursos que não vimos na disciplina foi reescrito com estruturas mais simples ou descartado.
2. **Testes pelo menu:** executamos o programa e testamos cada opção, incluindo entradas erradas de propósito: letras no lugar de números, opções fora do menu, campos vazios, datas inválidas, datas futuras e horários em formato errado.
3. **Testes de regras:** tentamos registrar a mesma dose duas vezes, retirar remédio com estoque zerado e excluir cadastros, para confirmar que o programa bloqueava ou pedia confirmação.
4. **Testes do JSON:** fechamos e abrimos o programa para conferir se os dados continuavam salvos, e editamos o `dados.json` com um erro de propósito para ver se o programa avisava sem apagar as informações antigas.
5. **Conferência do relatório:** usamos a opção 8 para gerar os dados de exemplo e calculamos à mão a porcentagem de doses no horário, comparando com o resultado da opção 5.
6. **Ajustes:** quando encontrávamos um problema, corrigíamos o código e repetíamos os testes daquela opção.

## 5. Análise crítica

**Benefícios:** a IA ajudou a encontrar erros que tinham passado despercebidos, como registros duplicados da mesma dose e o risco de perder dados com um JSON inválido. Também acelerou a escrita da documentação e ajudou a deixar as mensagens do programa mais claras para quem não entende de tecnologia.

**Limitações:** algumas sugestões eram mais complexas do que o conteúdo visto na disciplina ou continham erros de lógica, então precisaram ser simplificadas ou corrigidas pelo grupo. A IA também não conhece o contexto do projeto por conta própria: foi preciso explicar várias vezes as regras do Memora, como a tolerância de 20 minutos.

**Dificuldades:** o maior desafio foi não depender da ferramenta. Aprendemos que a IA funciona melhor como revisora e professora de apoio do que como autora do código, e que o grupo precisa entender e testar tudo o que entra no projeto.
