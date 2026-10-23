class Cliente:
    def __init__(self, nome: str, email: str):
        self.set_nome(nome)
        self.set_email(email)

    def get_nome(self) -> str:
        return self.__nome

    def get_email(self) -> str:
        return self.__email

    def set_nome(self, nome: str) -> None:
        if isinstance(nome, str) and len(nome.strip()) >= 3:
            self.__nome = nome.strip()
        else:
            print("[ERRO] Nome inválido! O nome deve ter no mínimo 3 caracteres.")
            if not hasattr(self, '_Cliente__nome'):
                self.__nome = "Cliente Indefinido"

    def set_email(self, email: str) -> None:
        if isinstance(email, str) and "@" in email and "." in email:
            self.__email = email.strip()
        else:
            print("[ERRO] E-mail inválido! O e-mail deve conter '@' e '.'.")
            if not hasattr(self, '_Cliente__email'):
                self.__email = "email_invalido@dominio.com"


if __name__ == "__main__":
    print("=== TESTANDO A CLASSE BASE DO PROJETO FINAL ===")
    
    objeto_valido = Cliente("Carlos Silva", "carlos@email.com")
    print(f"Objeto Criado: {objeto_valido.get_nome()} - Email: {objeto_valido.get_email()}")
    
    print("\n--- Teste 1: Tentativa de criar com e-mail inválido ---")
    objeto_invalido = Cliente("João Souza", "joao_sem_at_dominio")
    print(f"Resultado mantido com segurança: {objeto_invalido.get_email()}")
    
    print("\n--- Teste 2: Tentativa de alterar o nome para um texto muito curto ---")
    objeto_valido.set_nome("AB")
    print(f"Nome do objeto protegido: {objeto_valido.get_nome()}")