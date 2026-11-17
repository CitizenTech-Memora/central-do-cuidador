import json
import os
from datetime import date, datetime, timedelta

PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_DADOS = os.path.join(PASTA, 'dados.json')
ARQUIVO_RELATORIO = os.path.join(PASTA, 'relatorio.json')
TOLERANCIA_MINUTOS = 20

MENU_OPCOES = (
    "1 - Cadastrar pessoa",
    "2 - Cadastrar remédio e horários",
    "3 - Registrar retirada ou falta de retirada",
    "4 - Ver os remédios de hoje",
    "5 - Ver resumo dos últimos 7 dias",
    "6 - Ver remédios que estão acabando",
    "7 - Ver ou cadastrar contatos",
    "8 - Criar exemplo para testar",
    "9 - Apagar pessoa cadastrada",
    "10 - Apagar remédio cadastrado",
    "11 - Atualizar quantidade de remédios",
    "0 - Sair"
)



def dados_vazios():
    return {'pessoas': [], 'remedios': [], 'eventos': [], 'contatos': []}


def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        return dados_vazios()

    try:
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)

        if not isinstance(dados, dict):
            raise ValueError('O arquivo não contém um cadastro válido.')
        for nome in dados_vazios():
            if nome not in dados or not isinstance(dados[nome], list):
                raise ValueError(f'A lista {nome} está ausente ou inválida.')

        campos = {
            'pessoas': ('id', 'nome'),
            'remedios': ('id', 'pessoa_id', 'nome', 'dosagem', 'horarios', 'estoque'),
            'eventos': ('remedio_id', 'data', 'horario', 'tipo'),
            'contatos': ('pessoa_id', 'nome', 'relacao', 'ordem')
        }
        for nome in campos:
            for item in dados[nome]:
                if not isinstance(item, dict):
                    raise ValueError(f'Existe um registro inválido em {nome}.')
                for campo in campos[nome]:
                    if campo not in item:
                        raise ValueError(f'Falta o campo {campo} em {nome}.')
        return dados
    except (OSError, ValueError, json.JSONDecodeError) as erro:
        print('Não foi possível abrir o dados.json:', erro)
        print('O programa será encerrado para não apagar seus dados antigos.')
        return None


def salvar_dados(dados):
    temporario = ARQUIVO_DADOS + '.tmp'
    try:
        with open(temporario, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        os.replace(temporario, ARQUIVO_DADOS)
        return True
    except (OSError, TypeError, ValueError) as erro:
        print('Não foi possível salvar os dados:', erro)
        return False

def pedir_texto(mensagem):
    while True:
        resposta = input(mensagem).strip()
        if resposta != "":
            return resposta
        print("Atenção: Esse campo não pode ficar vazio.")

def pedir_numero(mensagem, minimo=0, maximo=100000):
    while True:
        try:
            valor = int(input(mensagem))
            if minimo <= valor <= maximo:
                return valor
            else:
                print(f"Por favor, digite um número entre {minimo} e {maximo}.")
        except ValueError:
            print("Entrada inválida. Digite apenas números inteiros.")

def pedir_confirmacao(mensagem):
    while True:
        resposta = input(mensagem + ' (s/n): ').strip().lower()
        if resposta == 's':
            return True
        if resposta == 'n':
            return False
        print('Digite s para sim ou n para não.')

def formatar_data(data_iso):
    return datetime.strptime(data_iso, '%Y-%m-%d').strftime('%d/%m/%Y')

def pedir_data(mensagem):
    while True:
        entrada = input(mensagem + ' (DD/MM/AAAA) ou aperte Enter para hoje: ').strip()
        if entrada == "":
            return date.today().isoformat()
        try:
            dia = datetime.strptime(entrada, '%d/%m/%Y').date()
            if dia <= date.today():
                return dia.isoformat()
            else:
                print("Não é possível registrar datas no futuro.")
        except ValueError:
            print("Data inválida. Use o formato dia/mês/ano (ex: 15/11/2026).")

def validar_horario(horario):
    try:
        datetime.strptime(horario, '%H:%M')
        return len(horario) == 5
    except ValueError:
        return False

def pedir_lista_horarios():
    while True:
        entrada = input('Digite os horários separados por vírgula (ex: 08:00, 20:00): ')
        lista = []
        partes = entrada.split(',')
        
        for p in partes:
            h = p.strip()
            if h != "" and h not in lista:
                lista.append(h)
                
        if len(lista) > 0 and all(validar_horario(h) for h in lista):
            lista.sort()
            return lista
        print("Por favor, digite horários válidos no formato HH:MM.")

def gerar_novo_id(lista):
    maior = 0
    for item in lista:
        if item['id'] > maior:
            maior = item['id']
    return maior + 1



def escolher_item(lista, titulo):
    if len(lista) == 0:
        print("Nenhum cadastro encontrado.")
        return None
    
    print(f"\n{titulo}")
    for item in lista:
        print(f"[{item['id']}] - {item['nome']}")
        
    escolha = pedir_numero('Digite o número do cadastro (0 para cancelar): ')
    
    for item in lista:
        if item['id'] == escolha:
            return item
    if escolha == 0:
        print('Operação cancelada.')
    else:
        print('Número não encontrado. Confira a lista.')
    return None

def cadastrar_pessoa(dados):
    nome = pedir_texto('Nome da pessoa acompanhada: ')
    novo_id = gerar_novo_id(dados['pessoas'])
    dados['pessoas'].append({'id': novo_id, 'nome': nome})
    print("Pessoa cadastrada com sucesso!")
    return True

def cadastrar_remedio(dados):
    pessoa = escolher_item(dados['pessoas'], 'Pessoas cadastradas:')
    if not pessoa:
        return False
        
    nome = pedir_texto('Nome do medicamento (ex: Remédio A): ')
    dosagem = pedir_texto('Dosagem (ex: 1 comprimido): ')
    lista_horarios = pedir_lista_horarios()
    estoque = pedir_numero('Quantidade atual em estoque: ', 0, 10000)
    inicio = pedir_data('Data de início do acompanhamento')
    
    dados['remedios'].append({
        'id': gerar_novo_id(dados['remedios']), 
        'pessoa_id': pessoa['id'],
        'nome': nome, 
        'dosagem': dosagem, 
        'horarios': lista_horarios,
        'estoque': estoque, 
        'inicio': inicio
    })
    print("Medicamento cadastrado com sucesso!")
    return True

def verificar_evento_existente(dados, remedio_id, dia, horario):
    for evento in dados['eventos']:
        if (evento['remedio_id'] == remedio_id and 
            evento['data'] == dia and 
            evento['horario'] == horario and 
            evento['tipo'] != 'fora_de_hora'):
            return evento
    return None

def registrar_evento(dados):
    pessoa = escolher_item(dados['pessoas'], 'Pessoas cadastradas:')
    if not pessoa:
        return False
        
    remedios_da_pessoa = [r for r in dados['remedios'] if r['pessoa_id'] == pessoa['id']]
    remedio = escolher_item(remedios_da_pessoa, 'Medicamentos da pessoa:')
    if not remedio:
        return False
        
    dia = pedir_data('Em que dia aconteceu?')
    if dia < remedio.get('inicio', '0000-00-00'):
        print('Erro: A data informada é anterior ao início do tratamento.')
        return False
        
    print('\nO que aconteceu?')
    print('1 - O remédio foi retirado da caixa')
    print('2 - O remédio não foi retirado')
    print('3 - Tentativa fora do horário (simulação)')
    opcao = pedir_numero('Escolha uma opção: ', 1, 3)
    
    if opcao == 3:
        horario = pedir_texto('Hora da tentativa (HH:MM): ')
        while not validar_horario(horario):
            horario = pedir_texto('Formato inválido. Hora da tentativa (HH:MM): ')
        if dia == date.today().isoformat() and horario > datetime.now().strftime('%H:%M'):
            print('Esse horário ainda não chegou. Confira a hora informada.')
            return False
        for evento in dados['eventos']:
            if (evento['remedio_id'] == remedio['id'] and evento['data'] == dia
                    and evento['horario'] == horario and evento['tipo'] == 'fora_de_hora'):
                print('Essa tentativa já foi registrada.')
                return False
        tipo = 'fora_de_hora'
        minutos = None
    else:
        print("\nQual era o horário previsto?")
        for i, h in enumerate(remedio['horarios'], 1):
            print(f'{i} - {h}')
            
        pos = pedir_numero('Escolha a opção do horário: ', 1, len(remedio['horarios']))
        horario = remedio['horarios'][pos - 1]

        if dia == date.today().isoformat() and horario > datetime.now().strftime('%H:%M'):
            print('Ainda não chegou esse horário. Registre a dose depois.')
            return False

        if verificar_evento_existente(dados, remedio['id'], dia, horario):
            print('Já existe um registro para este remédio nesse dia e horário.')
            return False
            
        if opcao == 1:
            if dia == date.today().isoformat() and remedio['estoque'] <= 0:
                print('O remédio acabou. Atualize a quantidade na opção 11.')
                return False
            minutos = pedir_numero('Minutos de atraso (0 se foi no horário): ', 0, 600)
            tipo = 'no_horario' if minutos <= TOLERANCIA_MINUTOS else 'atrasada'
            if dia == date.today().isoformat():
                remedio['estoque'] -= 1
            else:
                print('Registro antigo: a quantidade atual de remédios não foi alterada.')
        elif opcao == 2:
            minutos = None
            tipo = 'perdida'

    dados['eventos'].append({
        'remedio_id': remedio['id'], 
        'data': dia,
        'horario': horario, 
        'tipo': tipo,
        'minutos_apos_horario': minutos
    })
    
    dicionario_status = {
        'no_horario': 'Remédio retirado no horário', 
        'atrasada': 'Remédio retirado com atraso',
        'perdida': 'Remédio não retirado', 
        'fora_de_hora': 'Tentativa fora do horário registrada'
    }
    
    print(f"Salvo: {dicionario_status[tipo]}")
    if opcao == 1 and dia == date.today().isoformat():
        print(f"Restam {remedio['estoque']} unidade(s) na caixa.")
    return True

def mostrar_doses_hoje(dados):
    pessoa = escolher_item(dados['pessoas'], 'De quem você quer ver as doses?')
    if not pessoa:
        return
        
    hoje = date.today().isoformat()
    print(f"\n--- Resumo de Hoje ({formatar_data(hoje)}) ---")
    
    remedios_da_pessoa = [r for r in dados['remedios'] if r['pessoa_id'] == pessoa['id']]
    encontrou = False

    for remedio in remedios_da_pessoa:
        if hoje < remedio.get('inicio', '0000-00-00'):
            continue

        for horario in remedio['horarios']:
            encontrou = True
            evento = verificar_evento_existente(dados, remedio['id'], hoje, horario)

            if evento:
                status_txt = {'no_horario': 'Retirado no horário',
                              'atrasada': 'Retirado com atraso', 'perdida': 'Não retirado'}
                situacao = status_txt.get(evento['tipo'], 'Sem informação')
            elif horario > datetime.now().strftime('%H:%M'):
                situacao = 'Aguardando o horário'
            else:
                situacao = 'Ainda não foi registrado'

            print(f"{horario} - {remedio['nome']} ({remedio['dosagem']}): {situacao}")

    if not encontrou:
        print('Não há remédios programados para hoje.')

def gerar_relatorio(dados):
    pessoa = escolher_item(dados['pessoas'], 'Gerar relatório para qual pessoa?')
    if not pessoa:
        return
        
    hoje = date.today()
    inicio_semana = hoje - timedelta(days=6)
    previstas = 0
    contadores = {'no_horario': 0, 'atrasada': 0, 'perdida': 0, 'fora_de_hora': 0}
    
    remedios_da_pessoa = [r for r in dados['remedios'] if r['pessoa_id'] == pessoa['id']]
    
    for remedio in remedios_da_pessoa:
        data_inicio = datetime.strptime(remedio.get('inicio', inicio_semana.isoformat()), '%Y-%m-%d').date()
        
        for i in range(7):
            dia_atual = inicio_semana + timedelta(days=i)
            if dia_atual < data_inicio:
                continue
                
            for horario in remedio['horarios']:
                if dia_atual == hoje and horario > datetime.now().strftime('%H:%M'):
                    continue
                    
                previstas += 1
                evento = verificar_evento_existente(dados, remedio['id'], dia_atual.isoformat(), horario)
                
                if evento:
                    contadores[evento['tipo']] += 1
                    
        for evento in dados['eventos']:
            if evento['remedio_id'] == remedio['id'] and evento['tipo'] == 'fora_de_hora':
                if inicio_semana.isoformat() <= evento['data'] <= hoje.isoformat():
                    contadores['fora_de_hora'] += 1

    sem_registro = previstas - contadores['no_horario'] - contadores['atrasada'] - contadores['perdida']
    taxa = (100 * contadores['no_horario'] / previstas) if previstas > 0 else 0

    print(f"\n--- RESUMO DAS RETIRADAS (ÚLTIMOS 7 DIAS) ---")
    print(f"Pessoa acompanhada: {pessoa['nome']}")
    print(f"Período: {formatar_data(inicio_semana.isoformat())} até {formatar_data(hoje.isoformat())}")
    print(f"Doses previstas: {previstas}")
    print(f"Doses no horário: {contadores['no_horario']}")
    print(f"Doses atrasadas: {contadores['atrasada']}")
    print(f"Doses não retiradas (registradas): {contadores['perdida']}")
    print(f"Doses sem informação: {sem_registro}")
    print(f"Tentativas fora de hora: {contadores['fora_de_hora']}")
    print(f"Retiradas no horário: {taxa:.1f}% das doses previstas")

    if previstas == 0:
        print('Ainda não há doses previstas neste período.')
    elif sem_registro > 0:
        print('Há doses sem registro. Confira as informações antes de tirar conclusões.')
    elif taxa >= 90:
        print('A maioria das retiradas foi registrada no horário.')
    else:
        print('Vale conferir os horários em que houve atraso ou falta de retirada.')
    print('Lembrete: retirar da caixa não confirma que o remédio foi tomado.')
            
    if pedir_confirmacao('Deseja salvar esse resumo em relatorio.json?'):
        resumo = {
            'paciente': pessoa['nome'],
            'data_geracao': hoje.isoformat(),
            'total_previstas': previstas,
            'metricas': contadores,
            'sem_registro': sem_registro,
            'taxa_retiradas_no_horario': round(taxa, 1)
        }
        try:
            with open(ARQUIVO_RELATORIO, 'w', encoding='utf-8') as f:
                json.dump(resumo, f, ensure_ascii=False, indent=4)
            print("Arquivo relatorio.json salvo com sucesso.")
        except Exception as e:
            print(f"Erro ao exportar: {e}")

def verificar_estoque(dados):
    if len(dados['remedios']) == 0:
        print("Ainda não há remédios cadastrados no sistema.")
        return
        
    print("\n--- AVISO DE ESTOQUE ---")
    teve_aviso = False
    
    for r in dados['remedios']:
        qtd_diaria = len(r['horarios'])
        dias_restantes = r['estoque'] // qtd_diaria if qtd_diaria > 0 else 0

        if dias_restantes <= 5:
            nome_pessoa = 'Pessoa não encontrada'
            for p in dados['pessoas']:
                if p['id'] == r['pessoa_id']:
                    nome_pessoa = p['nome']
                    break
            print(f"Atenção, {nome_pessoa}: {r['nome']} tem {r['estoque']} unidade(s).")
            print(f"  Estimativa: cerca de {dias_restantes} dia(s) de estoque.")
            teve_aviso = True
            
    if not teve_aviso:
        print('Nenhum remédio está próximo de acabar.')
    print('Estimativa baseada em uma unidade por horário cadastrado.')

def gerenciar_contatos(dados):
    pessoa = escolher_item(dados['pessoas'], 'Escolha a pessoa:')
    if not pessoa:
        return False
        
    contatos = [c for c in dados['contatos'] if c.get('pessoa_id') == pessoa['id']]
    contatos = sorted(contatos, key=lambda c: c['ordem'])
    
    print(f"\nRede de cuidado de {pessoa['nome']}:")
    if not contatos:
        print("Nenhum contato cadastrado.")
    else:
        for c in contatos:
            print(f"{c['ordem']}º - {c['nome']} (Relação: {c['relacao']})")
            
    if pedir_confirmacao('\nDeseja adicionar um novo familiar/cuidador?'):
        nome = pedir_texto('Nome: ')
        relacao = pedir_texto('Relação (ex: Filho, Vizinho): ')
        while True:
            ordem = pedir_numero('Prioridade (1 = primeiro contato): ', 1, 10)
            repetida = False
            for contato in contatos:
                if contato['ordem'] == ordem:
                    repetida = True
            if not repetida:
                break
            print('Essa prioridade já está em uso. Escolha outro número.')

        dados['contatos'].append({
            'pessoa_id': pessoa['id'], 
            'nome': nome,
            'relacao': relacao, 
            'ordem': ordem
        })
        print('Contato salvo! Este programa não envia mensagens automaticamente.')
        return True
    return False

def excluir_remedio(dados):
    pessoa = escolher_item(dados['pessoas'], 'Pessoa:')
    if not pessoa: return False
    
    remedios = [r for r in dados['remedios'] if r['pessoa_id'] == pessoa['id']]
    remedio = escolher_item(remedios, 'Qual remédio quer apagar?')
    if not remedio: return False
    
    print('Atenção: também serão apagados os registros desse remédio.')
    print('Faça uma cópia do dados.json antes de excluir, se precisar guardar o histórico.')
    if pedir_confirmacao(f"Apagar {remedio['nome']} definitivamente?"):
        dados['remedios'].remove(remedio)
        dados['eventos'] = [e for e in dados['eventos'] if e['remedio_id'] != remedio['id']]
        print("Medicamento excluído.")
        return True
    return False

def excluir_pessoa(dados):
    pessoa = escolher_item(dados['pessoas'], 'Quem deseja apagar do sistema?')
    if not pessoa: return False
    
    print('Isso apagará a pessoa, os remédios, os contatos e os registros relacionados.')
    print('Essa ação não pode ser desfeita.')
    if pedir_confirmacao(f"Apagar {pessoa['nome']} definitivamente?"):
        remedios_id = [r['id'] for r in dados['remedios'] if r['pessoa_id'] == pessoa['id']]
        
        dados['pessoas'].remove(pessoa)
        dados['remedios'] = [r for r in dados['remedios'] if r['pessoa_id'] != pessoa['id']]
        dados['contatos'] = [c for c in dados['contatos'] if c.get('pessoa_id') != pessoa['id']]
        dados['eventos'] = [e for e in dados['eventos'] if e['remedio_id'] not in remedios_id]
        
        print("Pessoa e histórico removidos com sucesso.")
        return True
    return False

def atualizar_estoque(dados):
    pessoa = escolher_item(dados['pessoas'], 'Pessoa:')
    if not pessoa: return False
    
    remedios = [r for r in dados['remedios'] if r['pessoa_id'] == pessoa['id']]
    remedio = escolher_item(remedios, 'Qual remédio você quer atualizar?')
    if not remedio: return False
    
    print(f"O estoque atual de {remedio['nome']} é: {remedio['estoque']}")
    novo_estoque = pedir_numero('Digite a nova quantidade total na caixa: ', 0, 10000)
    remedio['estoque'] = novo_estoque
    print("Estoque atualizado!")
    return True



def criar_exemplo(dados):
    for pessoa in dados['pessoas']:
        if pessoa['nome'] == 'Dona Lurdes (exemplo)':
            print('O exemplo já foi criado. Escolha Dona Lurdes nas outras opções.')
            return False

    print('Essa opção cria uma pessoa, um remédio e registros inventados.')
    if not pedir_confirmacao('Deseja criar esse exemplo?'):
        return False

    pessoa_id = gerar_novo_id(dados['pessoas'])
    remedio_id = gerar_novo_id(dados['remedios'])
    inicio = date.today() - timedelta(days=6)

    dados['pessoas'].append({'id': pessoa_id, 'nome': 'Dona Lurdes (exemplo)'})
    dados['remedios'].append({
        'id': remedio_id, 'pessoa_id': pessoa_id, 'nome': 'Remédio A',
        'dosagem': '1 comprimido', 'horarios': ['08:00', '14:00'],
        'estoque': 20, 'inicio': inicio.isoformat()
    })
    dados['contatos'].append({'pessoa_id': pessoa_id, 'nome': 'Ana (exemplo)',
                              'relacao': 'filha', 'ordem': 1})
    dados['contatos'].append({'pessoa_id': pessoa_id, 'nome': 'Carlos (exemplo)',
                              'relacao': 'filho', 'ordem': 2})

    for dias_atras in range(1, 7):
        dia = (date.today() - timedelta(days=dias_atras)).isoformat()
        for horario in ['08:00', '14:00']:
            if dias_atras == 3 and horario == '14:00':
                tipo = 'perdida'
                minutos = None
            elif dias_atras == 2 and horario == '14:00':
                tipo = 'atrasada'
                minutos = 35
            else:
                tipo = 'no_horario'
                minutos = 5
            dados['eventos'].append({
                'remedio_id': remedio_id, 'data': dia, 'horario': horario,
                'tipo': tipo, 'minutos_apos_horario': minutos
            })

    print('Exemplo criado! Use a opção 5 para ver o resumo de Dona Lurdes.')
    return True


def main():
    print("Iniciando o Memora...")
    dados = carregar_dados()
    if dados is None:
        return
    print('Simulação educativa: retirada não significa que o remédio foi tomado.')

    while True:
        try:
            print("\n" + "=" * 44)
            print("       MEMORA - CENTRAL DO CUIDADOR")
            print("=" * 44)
            print("\nCADASTROS")
            for opcao in MENU_OPCOES[0:2]:
                print(opcao)
            print("\nACOMPANHAMENTO")
            for opcao in MENU_OPCOES[2:7]:
                print(opcao)
            print("\nOUTRAS OPÇÕES")
            for opcao in MENU_OPCOES[7:]:
                print(opcao)
            print("\nPara escolher, digite o número da opção.")
            escolha = pedir_numero('Sua escolha: ', 0, 11)
            teve_alteracao = False
            
            match escolha:
                case 1:
                    teve_alteracao = cadastrar_pessoa(dados)
                case 2:
                    teve_alteracao = cadastrar_remedio(dados)
                case 3:
                    teve_alteracao = registrar_evento(dados)
                case 4:
                    mostrar_doses_hoje(dados)
                case 5:
                    gerar_relatorio(dados)
                case 6:
                    verificar_estoque(dados)
                case 7:
                    teve_alteracao = gerenciar_contatos(dados)
                case 8:
                    teve_alteracao = criar_exemplo(dados)
                case 9:
                    teve_alteracao = excluir_pessoa(dados)
                case 10:
                    teve_alteracao = excluir_remedio(dados)
                case 11:
                    teve_alteracao = atualizar_estoque(dados)
                case 0:
                    print("\nObrigado por usar o Memora. Encerrando sistema...")
                    break
                    
            if teve_alteracao:
                if salvar_dados(dados):
                    print('Informações salvas em dados.json.')
                else:
                    print('As últimas alterações não foram salvas. Encerrando para evitar problemas.')
                    break
                
        except (KeyboardInterrupt, EOFError):
            print("\n\nExecução interrompida pelo usuário.")
            break

if __name__ == '__main__':
    main()
