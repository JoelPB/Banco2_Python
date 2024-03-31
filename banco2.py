def menu():
    menu = """\n
    ========== Menu ==========
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    ==>
    """
    return input(menu)


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += "\033[32m" + f"Depósito:\tR$ {valor:.2f}\n" + "\033[0;0m"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor > saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif valor > limite:
        print("\n@@@ Operação falhou! O valor de saque excede o limite. @@@")
    elif numero_saques >= limite_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    elif valor > 0:
        saldo -= valor
        extrato += "\033[31m" + f"Saque:\tR$ {valor:.2f}\n" + "\033[0;0m"
        numero_saques += 1
        print("\n=== Saque realizado com suceso! ===")
    else:
        print("\@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n=========== EXTRATO ===========")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print("\033[30;1;43m" + f"\nSaldo:\t\tR$ {saldo:.2f}\n" + "\033[0;0m")
    print("===============================")


def criar_usuário(usuarios):
    cpf = input("Iforme o CPF (somente números): ")
    usuario = filtar_usuario(cpf, usuarios)

    if usuario:
        print("\@@@Já existe um usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Iforme o endereço (logradouro, nº - bairro - cidade/Sigla estado: ")

    usuarios.append({"nome": nome, "data_ascimeto": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("\n=== Usuário criado com sucesso! ===")


def filtar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\n
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("="*100)
        print(linha)


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("\033[32m" + "Informe o valor do depósito: " + "\033[0;0m"))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("\033[31m" + "Informe o valor do saque: " + "\033[0;0m"))
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuário(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Opção inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()
