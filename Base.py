import json
from pathlib import Path


ARQUIVO_USUARIOS = Path(__file__).with_name("usuarios_steam.json")




class Usuario:
    def __init__(self, nome: str, email: str, horas_jogadas: float = 0.0):
        self.set_nome(nome)
        self.set_email(email)
        self.set_horas_jogadas(horas_jogadas)


    def get_nome(self) -> str:
        return self.__nome


    def get_email(self) -> str:
        return self.__email


    def get_horas_jogadas(self) -> float:
        return self.__horas_jogadas


    def set_nome(self, nome: str) -> None:
        if not isinstance(nome, str):
            raise ValueError("Nome inválido! O nome deve ser texto.")


        nome = nome.strip()
        if len(nome) < 3:
            raise ValueError("Nome inválido! O nome deve ter no mínimo 3 caracteres.")


        self.__nome = nome


    def set_email(self, email: str) -> None:
        if not isinstance(email, str):
            raise ValueError("E-mail inválido! O e-mail deve ser texto.")


        email = email.strip()
        if "@" not in email or "." not in email:
            raise ValueError("E-mail inválido! O e-mail deve conter '@' e '.'.")


        self.__email = email


    def set_horas_jogadas(self, horas_jogadas: float) -> None:
        if not isinstance(horas_jogadas, (int, float)):
            raise ValueError("Horas jogadas inválidas! Digite um número válido.")


        if horas_jogadas < 0:
            raise ValueError("Horas jogadas inválidas! O valor não pode ser negativo.")


        self.__horas_jogadas = float(horas_jogadas)


    def to_dict(self) -> dict:
        return {
            "nome": self.get_nome(),
            "email": self.get_email(),
            "horas_jogadas": self.get_horas_jogadas(),
        }




def carregar_usuarios() -> list[Usuario]:
    if not ARQUIVO_USUARIOS.exists():
        return []


    try:
        dados = json.loads(ARQUIVO_USUARIOS.read_text(encoding="utf-8"))
        if not isinstance(dados, list):
            return []


        usuarios = []
        for item in dados:
            usuarios.append(
                Usuario(
                    nome=item.get("nome", ""),
                    email=item.get("email", ""),
                    horas_jogadas=item.get("horas_jogadas", 0.0),
                )
            )
        print("[SUCESSO] Usuários carregados com sucesso.")
        return usuarios
    except (json.JSONDecodeError, OSError, ValueError):
        print("[AVISO] Não foi possível carregar os dados salvos.")
        return []




def salvar_usuarios(usuarios: list[Usuario]) -> None:
    try:
        dados = [usuario.to_dict() for usuario in usuarios]
        ARQUIVO_USUARIOS.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
        print("[SUCESSO] Dados salvos com sucesso.")
    except OSError:
        print("[AVISO] Não foi possível salvar os dados no arquivo.")




def cadastrar_usuario() -> Usuario:
    while True:
        try:
            nome = input("Digite o nome do usuário da Steam: ")
            email = input("Digite o e-mail do usuário: ")
            horas = float(input("Digite as horas jogadas até o momento: "))
            return Usuario(nome, email, horas)
        except ValueError as erro:
            print(f"[AVISO] {erro}")
            print("Tente novamente.")




def listar_usuarios(usuarios: list[Usuario]) -> None:
    if not usuarios:
        print("[AVISO] Nenhum usuário cadastrado.")
        return


    print("\n=== USUÁRIOS CADASTRADOS ===")
    for indice, usuario in enumerate(usuarios):
        print(f"{indice} - {usuario.get_nome()} | {usuario.get_email()} | {usuario.get_horas_jogadas()}h")


    print("\n[SUCESSO] Lista de usuários exibida com sucesso.")




def buscar_usuario(usuarios: list[Usuario], posicao: int) -> Usuario:
    try:
        return usuarios[posicao]
    except IndexError:
        raise IndexError("Posição inválida. Usuário não encontrado.")




def editar_usuario(usuarios: list[Usuario]) -> None:
    if not usuarios:
        print("[AVISO] Nenhum usuário cadastrado para editar.")
        return


    try:
        posicao = int(input("Digite a posição do usuário que deseja editar: "))
        usuario = buscar_usuario(usuarios, posicao)


        novo_nome = input("Novo nome (deixe em branco para manter): ").strip()
        if novo_nome:
            usuario.set_nome(novo_nome)


        novo_email = input("Novo e-mail (deixe em branco para manter): ").strip()
        if novo_email:
            usuario.set_email(novo_email)


        nova_horas = input("Novas horas jogadas (deixe em branco para manter): ").strip()
        if nova_horas:
            usuario.set_horas_jogadas(float(nova_horas))


        print(f"\nUsuário atualizado: {usuario.get_nome()} | {usuario.get_email()} | {usuario.get_horas_jogadas()}h")
        print("[SUCESSO] Usuário editado com sucesso.")
    except ValueError as erro:
        print(f"[AVISO] {erro}")
    except IndexError as erro:
        print(f"[AVISO] {erro}")




def remover_usuario(usuarios: list[Usuario]) -> None:
    if not usuarios:
        print("[AVISO] Nenhum usuário cadastrado para remover.")
        return


    try:
        posicao = int(input("Digite a posição do usuário que deseja remover: "))
        usuario = buscar_usuario(usuarios, posicao)
        usuarios.pop(posicao)
        print(f"[SUCESSO] Usuário removido: {usuario.get_nome()}")
    except ValueError:
        print("[AVISO] Digite uma posição válida.")
    except IndexError as erro:
        print(f"[AVISO] {erro}")




def calcular_media_horas(usuarios: list[Usuario]) -> float:
    try:
        horas = [usuario.get_horas_jogadas() for usuario in usuarios]
        if not horas:
            raise ZeroDivisionError("Não foi possível calcular a média, pois não há usuários cadastrados.")
        return sum(horas) / len(horas)
    except ZeroDivisionError as erro:
        print(f"[AVISO] {erro}")
        return 0.0




if __name__ == "__main__":
    usuarios: list[Usuario] = carregar_usuarios()


    while True:
        print("\n=== MENU PRINCIPAL - STEAM DATABASE ===")
        print("1 - Cadastrar usuário")
        print("2 - Listar usuários")
        print("3 - Buscar usuário por posição")
        print("4 - Editar usuário")
        print("5 - Remover usuário")
        print("6 - Calcular média de horas jogadas")
        print("7 - Salvar dados")
        print("0 - Sair")


        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("[AVISO] Entrada inválida. Digite apenas números do menu.")
            continue


        if opcao == 1:
            usuario = cadastrar_usuario()
            usuarios.append(usuario)
            print(f"\nUsuário cadastrado com sucesso: {usuario.get_nome()} - Email: {usuario.get_email()}")
            print("[SUCESSO] Cadastro concluído com segurança.")


        elif opcao == 2:
            listar_usuarios(usuarios)
            print("[SUCESSO] Operação de listagem concluída.")


        elif opcao == 3:
            if not usuarios:
                print("[AVISO] Nenhum usuário cadastrado para buscar.")
                continue


            try:
                posicao = int(input("Digite a posição do usuário: "))
                usuario = buscar_usuario(usuarios, posicao)
                print(f"Usuário encontrado: {usuario.get_nome()} | {usuario.get_email()} | {usuario.get_horas_jogadas()}h")
                print("[SUCESSO] Busca realizada com sucesso.")
            except ValueError:
                print("[AVISO] Digite um número inteiro válido para a posição.")
            except IndexError as erro:
                print(f"[AVISO] {erro}")


        elif opcao == 4:
            editar_usuario(usuarios)


        elif opcao == 5:
            remover_usuario(usuarios)


        elif opcao == 6:
            try:
                media = calcular_media_horas(usuarios)
                print(f"Média de horas jogadas: {media:.2f} horas")
                print("[SUCESSO] Relatório de tempo de jogo concluído.")
            except ZeroDivisionError as erro:
                print(f"[AVISO] {erro}")


        elif opcao == 7:
            salvar_usuarios(usuarios)


        elif opcao == 0:
            salvar_usuarios(usuarios)
            print("Sistema encerrado com segurança. Até logo!")
            print("[SUCESSO] Programa finalizado com sucesso.")
            break


        else:
            print("[AVISO] Opção inválida. Escolha outra opção do menu.")