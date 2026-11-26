
import json
from pathlib import Path


# =========================
# SUPERCLASSE PESSOA
# =========================

class Pessoa:
    def __init__(self, nome, email):
        self.__nome = nome
        self.__email = email

    def get_nome(self):
        return self.__nome

    def get_email(self):
        return self.__email

    def set_nome(self, nome):
        if nome.strip():
            self.__nome = nome
            return True
        return False

    def set_email(self, email):
        if "@" in email and "." in email:
            self.__email = email
            return True
        return False


# =========================
# CLASSE JOGO
# =========================

class Jogo:
    def __init__(self, titulo, genero, horas_registradas=0):
        self.__titulo = titulo
        self.__genero = genero
        self.__horas_registradas = horas_registradas

    def get_titulo(self):
        return self.__titulo

    def get_genero(self):
        return self.__genero

    def get_horas_registradas(self):
        return self.__horas_registradas

    def registrar_horas(self, horas):
        if horas > 0:
            self.__horas_registradas += horas
            return True
        return False

    def to_dict(self):
        return {
            "titulo": self.__titulo,
            "genero": self.__genero,
            "horas_registradas": self.__horas_registradas
        }


# =========================
# CLASSE USUARIO
# HERDA DE PESSOA
# =========================

class Usuario(Pessoa):
    def __init__(self, nome, email, horas_jogadas=0):
        super().__init__(nome, email)

        self.__horas_jogadas = horas_jogadas
        self.__biblioteca = []

    def get_horas_jogadas(self):
        return self.__horas_jogadas

    def get_biblioteca(self):
        return self.__biblioteca

    def adicionar_jogo(self, jogo):
        for jogo_existente in self.__biblioteca:
            if jogo_existente.get_titulo().lower() == jogo.get_titulo().lower():
                return False

        # Cria uma cópia do jogo para a biblioteca do usuário
        novo_jogo = Jogo(
            jogo.get_titulo(),
            jogo.get_genero(),
            jogo.get_horas_registradas()
        )

        self.__biblioteca.append(novo_jogo)
        return True

    def registrar_horas_jogo(self, titulo, horas):
        if horas <= 0:
            return False

        for jogo in self.__biblioteca:
            if jogo.get_titulo().lower() == titulo.lower():
                jogo.registrar_horas(horas)
                self.__horas_jogadas += horas
                return True

        return False

    def to_dict(self):
        return {
            "nome": self.get_nome(),
            "email": self.get_email(),
            "horas_jogadas": self.__horas_jogadas,
            "biblioteca": [
                jogo.to_dict() for jogo in self.__biblioteca
            ]
        }


# =========================
# CLASSE STEAM DATABASE
# =========================

class SteamDatabase:
    def __init__(self):
        self.__arquivo = Path(__file__).with_name("steam_database.json")
        self.__usuarios = []
        self.__jogos_catalogo = []

        self.carregar_dados()

    # ---------------------
    # SALVAR DADOS
    # ---------------------

    def salvar_dados(self):
        dados = {
            "usuarios": [
                usuario.to_dict() for usuario in self.__usuarios
            ],
            "jogos_catalogo": [
                jogo.to_dict() for jogo in self.__jogos_catalogo
            ]
        }

        with open(self.__arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    # ---------------------
    # CARREGAR DADOS
    # ---------------------

    def carregar_dados(self):
        if not self.__arquivo.exists():
            return

        try:
            with open(self.__arquivo, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            self.__usuarios = []
            self.__jogos_catalogo = []

            for dados_jogo in dados.get("jogos_catalogo", []):
                jogo = Jogo(
                    dados_jogo["titulo"],
                    dados_jogo["genero"],
                    dados_jogo.get("horas_registradas", 0)
                )
                self.__jogos_catalogo.append(jogo)

            for dados_usuario in dados.get("usuarios", []):
                usuario = Usuario(
                    dados_usuario["nome"],
                    dados_usuario["email"],
                    dados_usuario.get("horas_jogadas", 0)
                )

                for dados_jogo in dados_usuario.get("biblioteca", []):
                    jogo = Jogo(
                        dados_jogo["titulo"],
                        dados_jogo["genero"],
                        dados_jogo.get("horas_registradas", 0)
                    )
                    usuario.get_biblioteca().append(jogo)

                self.__usuarios.append(usuario)

        except (json.JSONDecodeError, KeyError, TypeError):
            print("Erro ao carregar os dados salvos.")

    # ---------------------
    # CRUD DE USUÁRIOS
    # ---------------------

    def cadastrar_usuario(self, nome, email):
        for usuario in self.__usuarios:
            if usuario.get_email().lower() == email.lower():
                return False

        usuario = Usuario(nome, email)
        self.__usuarios.append(usuario)
        self.salvar_dados()
        return True

    def listar_usuarios(self):
        if not self.__usuarios:
            print("\nNenhum usuário cadastrado.")
            return

        print("\n===== USUÁRIOS CADASTRADOS =====")

        for usuario in self.__usuarios:
            print(f"Nome: {usuario.get_nome()}")
            print(f"E-mail: {usuario.get_email()}")
            print(f"Horas jogadas: {usuario.get_horas_jogadas()}")
            print("-" * 30)

    def buscar_usuario(self, email):
        for usuario in self.__usuarios:
            if usuario.get_email().lower() == email.lower():
                return usuario

        return None

    def atualizar_usuario(self, email):
        usuario = self.buscar_usuario(email)

        if usuario is None:
            print("Usuário não encontrado.")
            return

        novo_nome = input("Digite o novo nome: ").strip()
        novo_email = input("Digite o novo e-mail: ").strip()

        if not novo_nome or not novo_email:
            print("Nome e e-mail não podem ficar vazios.")
            return

        outro_usuario = self.buscar_usuario(novo_email)

        if outro_usuario is not None and outro_usuario != usuario:
            print("Esse e-mail já está cadastrado.")
            return

        usuario.set_nome(novo_nome)

        if usuario.set_email(novo_email):
            self.salvar_dados()
            print("Usuário atualizado com sucesso!")
        else:
            print("E-mail inválido.")

    def remover_usuario(self, email):
        usuario = self.buscar_usuario(email)

        if usuario is None:
            print("Usuário não encontrado.")
            return False

        self.__usuarios.remove(usuario)
        self.salvar_dados()
        print("Usuário removido com sucesso!")
        return True

    # ---------------------
    # MÉDIA DE HORAS
    # ---------------------

    def calcular_media_horas(self):
        if not self.__usuarios:
            print("Não há usuários cadastrados.")
            return

        total_horas = sum(
            usuario.get_horas_jogadas()
            for usuario in self.__usuarios
        )

        media = total_horas / len(self.__usuarios)

        print(f"\nMédia de horas jogadas: {media:.2f} horas")

    # ---------------------
    # CATÁLOGO DE JOGOS
    # ---------------------

    def cadastrar_jogo(self, titulo, genero):
        for jogo in self.__jogos_catalogo:
            if jogo.get_titulo().lower() == titulo.lower():
                return False

        jogo = Jogo(titulo, genero)
        self.__jogos_catalogo.append(jogo)
        self.salvar_dados()
        return True

    def listar_catalogo(self):
        if not self.__jogos_catalogo:
            print("\nO catálogo está vazio.")
            return

        print("\n===== CATÁLOGO DE JOGOS =====")

        for jogo in self.__jogos_catalogo:
            print(f"Título: {jogo.get_titulo()}")
            print(f"Gênero: {jogo.get_genero()}")
            print("-" * 30)

    def buscar_jogo(self, titulo):
        for jogo in self.__jogos_catalogo:
            if jogo.get_titulo().lower() == titulo.lower():
                return jogo

        return None

    # ---------------------
    # BIBLIOTECA DO USUÁRIO
    # ---------------------

    def adicionar_jogo_biblioteca(self, email, titulo_jogo):
        usuario = self.buscar_usuario(email)
        jogo = self.buscar_jogo(titulo_jogo)

        if usuario is None:
            print("Usuário não encontrado.")
            return

        if jogo is None:
            print("Jogo não encontrado no catálogo.")
            return

        if usuario.adicionar_jogo(jogo):
            self.salvar_dados()
            print("Jogo adicionado à biblioteca!")
        else:
            print("Esse jogo já está na biblioteca do usuário.")

    def listar_biblioteca(self, email):
        usuario = self.buscar_usuario(email)

        if usuario is None:
            print("Usuário não encontrado.")
            return

        biblioteca = usuario.get_biblioteca()

        if not biblioteca:
            print("A biblioteca desse usuário está vazia.")
            return

        print(f"\n===== BIBLIOTECA DE {usuario.get_nome()} =====")

        for jogo in biblioteca:
            print(f"Título: {jogo.get_titulo()}")
            print(f"Gênero: {jogo.get_genero()}")
            print(f"Horas no jogo: {jogo.get_horas_registradas()}")
            print("-" * 30)

    def registrar_horas_jogo(self, email, titulo, horas):
        usuario = self.buscar_usuario(email)

        if usuario is None:
            print("Usuário não encontrado.")
            return

        if usuario.registrar_horas_jogo(titulo, horas):
            self.salvar_dados()
            print("Horas registradas com sucesso!")
        else:
            print("Jogo não encontrado na biblioteca ou horas inválidas.")


# =========================
# MENU PRINCIPAL
# =========================

def menu():
    steam = SteamDatabase()

    while True:
        print("\n========== STEAM DATABASE ==========")
        print("1 - Cadastrar usuário")
        print("2 - Listar usuários")
        print("3 - Atualizar usuário")
        print("4 - Remover usuário")
        print("5 - Calcular média de horas jogadas")
        print("6 - Cadastrar jogo no catálogo")
        print("7 - Listar catálogo")
        print("8 - Adicionar jogo à biblioteca")
        print("9 - Listar biblioteca de usuário")
        print("10 - Registrar horas em um jogo")
        print("0 - Sair")
        print("=================================")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ").strip()
            email = input("E-mail: ").strip()

            if not nome or not email:
                print("Nome e e-mail são obrigatórios.")
            elif "@" not in email or "." not in email:
                print("E-mail inválido.")
            elif steam.cadastrar_usuario(nome, email):
                print("Usuário cadastrado com sucesso!")
            else:
                print("Esse e-mail já está cadastrado.")

        elif opcao == "2":
            steam.listar_usuarios()

        elif opcao == "3":
            email = input("Digite o e-mail do usuário que deseja atualizar: ")
            steam.atualizar_usuario(email)

        elif opcao == "4":
            email = input("Digite o e-mail do usuário que deseja remover: ")
            steam.remover_usuario(email)

        elif opcao == "5":
            steam.calcular_media_horas()

        elif opcao == "6":
            titulo = input("Título do jogo: ").strip()
            genero = input("Gênero do jogo: ").strip()

            if not titulo or not genero:
                print("Título e gênero são obrigatórios.")
            elif steam.cadastrar_jogo(titulo, genero):
                print("Jogo cadastrado no catálogo!")
            else:
                print("Esse jogo já está no catálogo.")

        elif opcao == "7":
            steam.listar_catalogo()

        elif opcao == "8":
            email = input("E-mail do usuário: ")
            titulo = input("Título do jogo: ")
            steam.adicionar_jogo_biblioteca(email, titulo)

        elif opcao == "9":
            email = input("E-mail do usuário: ")
            steam.listar_biblioteca(email)

        elif opcao == "10":
            email = input("E-mail do usuário: ")
            titulo = input("Título do jogo: ")

            try:
                horas = float(input("Quantas horas deseja registrar? "))
                steam.registrar_horas_jogo(email, titulo, horas)
            except ValueError:
                print("Digite um número válido de horas.")

        elif opcao == "0":
            print("Encerrando o Steam Database...")
            break

        else:
            print("Opção inválida!")


# =========================
# EXECUÇÃO
# =========================

if __name__ == "__main__":
    menu()
