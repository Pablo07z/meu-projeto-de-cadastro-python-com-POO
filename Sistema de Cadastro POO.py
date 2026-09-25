print("<=====Sistema de Cadastro com POO=====>")

# Bibliotecas importadas.
from datetime import datetime
import secrets 
from InquirerPy import prompt 
import json 
cadastro = "Arquivos Python/Projetos concluídos em Python/Projeto de cadastro (versão 2)/dados de cadastro POO.json" #Import do arquivo Json.

class Usuario: #Classe Usuario, representando o usuário e seus atributos.
    def __init__(self, nome, idade, endereco, email, senha, data_cadastro=None):
        self.nome = nome
        self.idade = idade
        self._endereco = endereco
        self._email = email
        self._senha = senha
        self.data_cadastro = data_cadastro if data_cadastro is not None else datetime.now().isoformat()

class Interfaces: #Classe contendo todas as interfaces que serão usadas durante a execução do sistema.
    @staticmethod
    def menu_de_operacoes(): #Interface de Controle Central do Sistema de Cadastro, responsável por direcionar o usuário para as funções de cadastro, login ou saída do sistema.
        while True:
            perguntas = [
                {
                    "type": "list",
                    "name": "opcao",
                    "message": "\nEscolha uma opção:",
                    "choices": [
                        "Cadastrar usuário",
                        "Login de Usuário",
                        "Sair"
                    ]
                }
            ]
            respostas = prompt(perguntas)
            opcao = respostas["opcao"]

            #Condições de execução: Cadastro, Login e sair do programa.
            if opcao == "Cadastrar usuário":
                print("=======| Preparando sua ficha de cadastro... |=======")
                GerenciadorDeUsuarios.informacoes_para_cadastro()

            elif opcao == "Login de Usuário":
                print("=======| É necessário fazer login! |=======")
                usuario, dados = GerenciadorDeUsuarios.Fazer_login_do_usuario() 

                if usuario is None:
                    continue
                Interfaces.menu_de_login(usuario, dados)

            elif opcao == "Sair":
                print("=======| Saindo do sistema... |=======")
                break

    @staticmethod
    def menu_de_login(usuario, dados): #Interface de controle do menu de login, responsável por direcionar o usuário para as funções de atualizar ou remover cadastro.
        while True:
            perguntas_do_login = [
                {
                    "type": "list",
                    "name": "opcao_de_login",
                    "message": "\nEscolha uma opcao:",
                    "choices": ["Atualizar Cadastro", "Remover Cadastro", "Sair do menu"]
                }
                ]
            respostas_do_menu = prompt(perguntas_do_login)
            opcao_login = respostas_do_menu["opcao_de_login"]

            if opcao_login == "Atualizar Cadastro":
                print("=======| Vamos atualizar seu cadastro! |=======\n")
                GerenciadorDeUsuarios.atualizar_cadastro(usuario,dados)
                break
                
            elif opcao_login == "Remover Cadastro":
                print("=======| Vamos remover seu cadastro! |=======\n")
                GerenciadorDeUsuarios.remover_cadastro(usuario,dados)
                break

            elif opcao_login == "Sair do menu":
                print("=======| Saindo do menu de login... |=======\n")
                break
        
    @staticmethod
    def criador_de_senhas(): #Define qual tipo de senha será usado com base na escolha do usuário.
        perguntas_sobre_senha = [
            {
                "type": "list",
                "name": "opcao_de_senhas",
                "message": "\n=======| Para o seu cadastro, deseja implementar uma senha gerada automaticamente? |=======",
                "choices": [
                    "Sim",
                    "Não"
                ]
            }
        ]
        respostas = prompt(perguntas_sobre_senha)
        opcao = respostas["opcao_de_senhas"]
        
        if opcao == "Sim":
            senha = secrets.token_hex(4)
            print(f"Sua senha é: {senha}\n")
            return senha
                
        elif opcao == "Não":
            senha = input("\n=======| Digite sua senha (No mínimo 8 caracteres): |=======\n")
            return senha

class GerenciadorDeUsuarios: # A responsável por lidar com todos os métodos relacionados ao usuário.
    @staticmethod
    def informacoes_para_cadastro(): #Responsável por coletar informações do usuário para criar o cadastro.
        nome = input("\n=======| Digite seu nome: |=======\n").strip().title()
        idade = input("\n=======| Digite a sua idade (informe apenas números): |=======\n").strip()
        endereco = input("\n=======| Informe seu endereço (rua, número da residência, bairro, cidade): |=======\n").strip().split(",")
        email = input("\n=======| Informe seu email: |=======\n").strip()
        senha = Interfaces.criador_de_senhas() # -> Chama a função responsável pela criação de senhas do cadastro.

        dados = GerenciadorDeUsuarios.carregar_usuarios()
        usuario_valido, mensagem_erro = Validadores.validador_de_cadastro(dados,idade,email,senha)
        if not usuario_valido:
            print(mensagem_erro)

        else:
            GerenciadorDeUsuarios.criar_cadastro(dados, nome, idade, endereco, email, senha)

    @staticmethod
    def consultar_arquivo(): #Responsável por consultar o arquivo de cadastro e verificar o arquivo.
        try:
            with open(cadastro, "r", encoding="utf-8") as files:
                dados = json.load(files)
                return dados
                
        except(FileNotFoundError, json.JSONDecodeError):
            dados = []
            return dados

    @staticmethod
    def carregar_usuarios(): #Responsável por transformar os dicionários de cada usuário em instâncias da classe Usuario com base nos dados carregados.
        dados_carregados = GerenciadorDeUsuarios.consultar_arquivo()
        dados = [Usuario(**{chave.lstrip("_"): valor for chave, valor in usuario.items()}) for usuario in dados_carregados]
        return dados

    @staticmethod
    def criar_cadastro(dados, nome, idade, endereco, email, senha): #É quem de fato cria o cadastro do usuário após todo o processo de validação.
            usuario = Usuario(nome,idade,endereco,email,senha).__dict__
            dados = [u.__dict__ for u in dados]

            dados.append(usuario)

            with open(cadastro, "w", encoding="utf-8") as files:
                json.dump(dados, files, ensure_ascii=False, indent=6)
                print("=======| Seu cadastro foi realizado com sucesso! |=======\n")
                print("=======|"*7)

    @staticmethod
    def Fazer_login_do_usuario(): #Responsável por fazer o login do usuário, verificando se o email e senha informados são válidos.
        dados = GerenciadorDeUsuarios.carregar_usuarios()
        
        usuario_encontrado = False

        email_login = input("\n=======| Digite seu email: |=======\n").strip()
        senha_login = input("\n=======| Digite sua senha: |=======\n").strip()

        for usuario in dados:
            if usuario._email == email_login and usuario._senha == senha_login:
                usuario_encontrado = True
                return(usuario, dados)

        if not usuario_encontrado:
            print("=======| Usuário não encontrado, tente novamente! |=======")
            return None, dados
            
    @staticmethod
    def atualizar_cadastro(usuario, dados): #É quem atualiza os dados do usuário com base nas informações fornecidas por ele.
        print("=======| Preencha os espaços com seus novos dados (apenas o que deseja alterar) |=======")
        nome = input("\n=======| Alterar nome: |=======\n").strip().title()
        idade = input("\n=======| Alterar idade: |=======\n").strip()
        endereco = input("\n=======| Alterar endereço: |=======\n").strip().split(",")
        email = input("\n=======| Alterar email: |=======\n").strip()
        senha = input("\n=======| Alterar senha: |=======\n").strip()

        nome = nome if nome else usuario.nome
        idade = idade if idade else usuario.idade
        endereco = endereco if endereco !=[""] else usuario._endereco
        email = email if email else usuario._email
        senha = senha if senha else usuario._senha

        usuario_valido, mensagem_erro = Validadores.validador_de_cadastro(dados, idade, email, senha, usuario)
        if not usuario_valido:
            print(mensagem_erro)
        
        else:
            local_no_arquivo = dados.index(usuario)
            usuario_atualizado = Usuario(nome,idade,endereco,email,senha)
            dados[local_no_arquivo] = usuario_atualizado
            dados_para_salvar = [u.__dict__ for u in dados]
    
            with open(cadastro, "w", encoding="utf-8") as files:
                json.dump(dados_para_salvar, files, ensure_ascii = False, indent = 6)   
                print("=======| Seu cadastro foi atualizado! |=======")
                return
                
    @staticmethod
    def remover_cadastro(usuario, dados): #Remove o usuário do sistema e atualiza isso no arquivo.
        dados.remove(usuario)
        dados = [u.__dict__ for u in dados]
        
        with open(cadastro, "w", encoding = "utf-8") as files:
            json.dump(dados, files, ensure_ascii = False, indent=6)
            print("=======| Seu cadastro foi removido! |=======")
            return
        
class Validadores: #Classe contendo todos os validadores das entradas de dados recebidas do usuário.
    @staticmethod
    def validador_de_email(email):
        if not "@" in email:
            return False, "\n=======| O email deve conter um domínio válido! |=======\n"
            
        if email.count("@") != 1:
            return False, "\n=======| O email deve conter apenas um @ |=======\n"
        
        usuario, dominio = email.split("@")
    
        if usuario == "":
            return False, "\n=======| Insira algo antes do @ em seu email |=======\n"
        
        if dominio == "":
            return False, "\n=======| Insira algo no domínio após @ em seu email |=======\n"
        
        if dominio.startswith("."):
            return False, "\n=======| O domínio do email não deve começar com pontos! |=======\n"
        
        if dominio.endswith("."):
            return False, "\n=======| O email não deve terminar com um ponto! |=======\n"
        
        if not "." in dominio:
            return False, "\n=======| O domínio de email inválido! |=======\n"
        
        return True, "\n=======| O email é válido! |=======\n"
    
    @staticmethod
    def validador_de_idade(idade): #Verifica se o usuário escreveu apenas números ao informar sua idade.
        if not idade.isdigit():
            return False, "\n=======| Digite apenas números |=======\n"
        
        idade = int(idade)
            
        if idade < 18:
            return False, "\n=======| É necessário ser maior de 18 anos para se cadastrar! |=======\n"
        
        return True, "\n=======| Idade válida! |=======\n"

    @staticmethod
    def validador_de_senhas(senha): #Verifica se a senha gerada ou criada são válidas.
        if len(senha) < 8:
            return False, "\n=======| Sua senha deve ter pelo menos 8 caracteres! |=======\n"
    
        if senha == "":
            return False, "\n=======| Digite uma senha! |=======\n"
    
        else:
            return True, "\n=======| Senha válida! |=======\n"

    @staticmethod
    def validador_de_cadastro(dados, idade, email, senha, usuario=None): #Responsável por verificar se o cadastro é válido:
            idade_valida, mensagem_idade = Validadores.validador_de_idade(idade)
            if not idade_valida:
                return False, mensagem_idade
    
            email_valido, mensagem_email = Validadores.validador_de_email(email)
            if not email_valido:
                return False, mensagem_email
            
            senha_valida, mensagem_senha = Validadores.validador_de_senhas(senha)
            if not senha_valida:
                return False, mensagem_senha
    
            cadastro_valido, mensagem_invalida = Validadores.verificador_de_duplicatas_cadastro(dados, email, usuario)
            if not cadastro_valido:
                return False, mensagem_invalida
    
            return True, "\n=======| Todas as informações foram verificadas! |=======\n"

    @staticmethod
    def verificador_de_duplicatas_cadastro(dados, email, usuario_atual=None): #Responsável por verificar se o email em cadastro é ou não usado por outro usuário já cadastrado.
        usuario_existe = False
        
        for usuario in dados:
            if usuario._email == email and usuario_atual is not usuario:
                usuario_existe = True
                break
    
        if usuario_existe:
            return False, "\n=======| O usuário já existe |=======\n"
        
        else:
            return True, ("\n=======| Usuário pronto para o cadastro! |=======\n")

#Bloco de inicio que chama a função de menu principal do sistema.
print("|=======| Olá, bem-vindo ao nosso sistema de cadastro! |=======|")
Interfaces.menu_de_operacoes()
