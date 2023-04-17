import PySimpleGUI as sg
from datetime import date
import random
import requests
import locale as l
import mysql.connector as mysql

# função para conexão ao banco e inserção das informações
def banco():
    # variáves recebem valores dos inputs
    nome = values['-nome-']
    email = values['-email-']
    telefone = values['-telefone-']    
    try:
        # esta é a função de conexão com o banco
        # devem ser fornecidos as configurações de conexão
        conexao = mysql.connect(
            host="127.0.0.1", # ip do servidor
            user="root", # usuario
            password="", # senha do usuario
            database="dbpython" # base de dados
        )
        # mensagem para verificação da conexão
        print("Conexão realizada com sucesso.")
        # abre um Cursor para executar um SQL
        cursor = conexao.cursor()
        # comando SQL a ser executado
        sql = "INSERT INTO contatos(nome, email, telefone) VALUES (%s, %s, %s)"
        vals = (nome, email, telefone) # devem ser passados como tupla
        # executando o comando pelo Cursor
        cursor.execute(sql, vals)
        # efetivando a alteração
        conexao.commit() # obrigatório para INSERT, DELETE e UPDATE
        print("Salvo com sucesso.")
    # instrução para tratamento de erro e excessão
    except mysql.Error as e:
        # capturando possiveis erros de conexao ou SQL com TRY CATCH
        print(e.msg)    
# função para disparar pop-up do gráfico, no evento click do botão Graf
def grafico():
    BAR_WIDTH = 50  # largura de cada barra
    BAR_SPACING = 75  # espaço entre as barras
    EDGE_OFFSET = 3  # offset a esquerda da primeira barra
    GRAPH_SIZE = DATA_SIZE = (300, 400)  # tamanho do pop-up em pixels
    # tema, o mesmo definido para o Dashboard
    sg.theme('Dashboard')
    # layout do pop-up
    layout = [[sg.Text('Gráfico de barras com PySimpleGUI')],
              [sg.Graph(GRAPH_SIZE, (0, 0), DATA_SIZE, k='-GRAPH-')],
              [sg.Button('OK'), sg.T('Click para ver mais dados'), sg.Exit()]]
    # janela do pop-up
    window = sg.Window('Gráfico de barras', layout, finalize=True)
    # área do plotagem do gráfico
    graph = window['-GRAPH-']  # type: sg.Graph
    # estrutura de repetição para geração de dados aleatórias
    while True:
        # estrutura de repetição para desenho das barras, após apagar o gráfico anterior
        graph.erase()
        for i in range(7):
            graph_value = random.randint(0, GRAPH_SIZE[1])
            graph.draw_rectangle(top_left=(i * BAR_SPACING + EDGE_OFFSET, graph_value),
                                 bottom_right=(i * BAR_SPACING + EDGE_OFFSET + BAR_WIDTH, 0),
                                 fill_color=sg.theme_button_color()[1])
            graph.draw_text(text=graph_value, location=(i * BAR_SPACING + EDGE_OFFSET + 25, graph_value + 10))
        # normalmente o topo do loop, Mas por conta do tipo de desenho vem o gráfico antes, marque isso no botão
        event, values = window.read()
        # estrutura de decisão para definir ações dos botões
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
    # fim para instruções da função
    window.close()
# dicionário de temas para o dashboard
theme_dict = {'BACKGROUND': '#003D9D',
                'TEXT': '#FFFFFF',
                'INPUT': '#F2EFE8',
                'TEXT_INPUT': '#000000',
                'SCROLL': '#F2EFE8',
                'BUTTON': ('#000000', '#C2D4D8'),
                'PROGRESS': ('#FFFFFF', '#C7D5E0'),
                'BORDER': 1,'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0}
# sg.theme_adiciona um tema('Dashboard', theme_dict)
sg.LOOK_AND_FEEL_TABLE['Dashboard'] = theme_dict
sg.theme('Dashboard')
# posição, borda e cores
BORDER_COLOR = '#FFFFFF'
DARK_HEADER_COLOR = '#FFFFFF'
BPAD_TOP = ((20,20), (20, 10))
BPAD_LEFT = ((20,10), (0, 10))
BPAD_LEFT_INSIDE = (0, 10)
BPAD_RIGHT = ((10,20), (10, 20))

# definição de localidade, para saída da data em português
l.setlocale(l.LC_TIME, "pt")
# data, em formato de texto, importada de datetime
data_atual = date.today()
data_em_texto = data_atual.strftime("%d de %B de %Y").title()
# banner com apresentação e data atual
top_banner = [[sg.Text(' '*2, background_color='#FFFFFF'),sg.Image('icone.png', background_color='#ffffff'),sg.Text(' '*128, background_color='#FFFFFF'),
               sg.Text(data_em_texto, font='Any 14', background_color='#005DAD')]]
# configuração da api para previsao do tempo em Brasília, através de requests
API_KEY = "7753ee82ffac2836bdb825e03be43f51"
cidade = "Brasília"
link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&lang=pt_br"
requisicao = requests.get(link)
requisicao_dic = requisicao.json()
descricao = requisicao_dic['weather'][0]['description']
temperatura = requisicao_dic['main']['temp'] - 273.15
# bloco topo do dashboard com previsao do tempo
top  = [[sg.Text(' '*30,),sg.Text(f"Temperatura em Brasília {temperatura:.2f} ºC", size=(50,1), justification='c', pad=BPAD_TOP, font='Any 16')],
            [sg.T(f'{i*25}-{i*34}') for i in range(7)],]
# bloco com input para nome do usuário, pop-up com mensagem de boas vindas
block_2 = [[sg.Text('Entrar', font='Any 15')],
            [sg.Text('')],
            [sg.Text('Nome do Usuário'), sg.Input(key='-user-')],
            [sg.Button('Login'), sg.Button('Cancelar')]  ]
# bloco com botão que deverá abrir gráfico com valores aleatórios
block_3 = [[sg.Text('Estatística', font='Any 16')],
            [sg.Text('\t  Gráfico', font='Any 10')],
            [sg.Image(data=sg.DEFAULT_BASE64_ICON)],
            [sg.Button('Graf'),sg.Button('Finalizar')]]  # comando para exibir imagens
# bloco com um conjunto de inputs para serem usados com bancos de dados
block_4 = [[sg.Text('Cadastro', font='Any 16')],
            [sg.Text(''),],
            [sg.OptionMenu(values=('Java', 'PHP', 'Python'), default_value='Curso',  k='-OPTION MENU-'),],
            [sg.Button(image_data=sg.DEFAULT_BASE64_ICON, key='-LOGO-'), sg.Text('\tContato')],
            [sg.Text('Nome\t'), sg.Input(key='-nome-')],
            [sg.Text('Endereço\t'), sg.Input(key='-email-')],
            [sg.Text('Telefone\t'), sg.Input(key='-telefone-')],
            [sg.Checkbox('Cadastro', default=True, k='-CB-'),
                sg.Radio('Masc', "RadioDemo", default=True, size=(10,1), k='-R1-'), sg.Radio('Fem', "RadioDemo", default=True, size=(10,1), k='-R2-'),
                sg.Combo(values=('Lógica', 'crud', 'Web'), default_value='Módulo', readonly=True, k='-COMBO-')],
           [sg.Text('')],
           [sg.Button('Cadastro'), sg.Button('Exit')],
            ]
# configuração do desenho do dashboard
layout = [[sg.Column(top_banner, size=(960, 60), pad=(0,0), background_color=DARK_HEADER_COLOR)],
          [sg.Column(top, size=(920, 90), pad=BPAD_TOP)],
          [sg.Column([[sg.Column(block_2, size=(450,150), pad=BPAD_LEFT_INSIDE)],
                      [sg.Column(block_3, size=(450,150),  pad=BPAD_LEFT_INSIDE)]], pad=BPAD_LEFT, background_color=BORDER_COLOR),
           sg.Column(block_4, size=(450, 320), pad=BPAD_RIGHT)]]
# configuração da janela
window = sg.Window('Dashboard PySimpleGUI-Style', layout, margins=(0,0), background_color=BORDER_COLOR, no_titlebar=True, grab_anywhere=True)
# eventos dos botões
while True:             # evento loop
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit' or event == 'Finalizar':
        break           # parar aplicação
    elif event == 'Graf':
            grafico()   # função para rodar pop-up do gráfico
    elif event == "Login":
        sg.popup('Bem vindo ',values['-user-'] , image=sg.EMOJI_BASE64_HAPPY_JOY, keep_on_top=True)   #pop-up de boas vindas
    elif event == "Cadastro":
        banco()
# fechar janela da aplicação           
window.close()
