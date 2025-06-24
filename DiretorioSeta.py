import os
import shutil
import platform
import questionary

# Pasta usada como lixeira para rollback de exclusões
LIXEIRA = os.path.join(os.getcwd(), '__lixeira_temporaria__')
os.makedirs(LIXEIRA, exist_ok=True)

# Lista para armazenar o histórico
historico = []

def limpar_tela():
    comando = 'cls' if platform.system() == 'Windows' else 'clear'
    os.system(comando)

def confirmar_acao(mensagem):
    while True:
        resposta = input(f"{mensagem} (s/n): ").strip().lower()
        if resposta in ['s', 'sim']:
            return True
        elif resposta in ['n', 'nao', 'não']:
            return False
        else:
            print("⚠️ Resposta inválida. Digite 's' ou 'n'.")

def registrar_acao(tipo, dados):
    historico.append({'acao': tipo, 'dados': dados})

def criar_diretorio():
    limpar_tela()
    nome = input("Digite o nome do diretório a ser criado: ")
    if not confirmar_acao(f"Tem certeza que deseja criar o diretório '{nome}'?"):
        print("❌ Ação cancelada.\n")
        return
    try:
        os.makedirs(nome)
        registrar_acao('criar_diretorio', {'nome': nome})
        print(f"✅ Diretório '{nome}' criado com sucesso.\n")
    except FileExistsError:
        print("⚠️ Esse diretório já existe.\n")
    except Exception as e:
        print(f"❌ Erro: {e}\n")

def listar_arquivos():
    limpar_tela()
    print("\nExemplo de caminho:")
    print("  Windows: C:\\meus_arquivos")
    caminho = input("Digite o caminho do diretório (pressione Enter para usar o diretório atual): ") or '.'

    if not os.path.isdir(caminho):
        print(f"❌ O caminho '{caminho}' não é um diretório válido.\n")
        input("Pressione Enter para voltar.")
        return

    try:
        arquivos = os.listdir(caminho)
        if not arquivos:
            print("📁 Diretório vazio.\n")
            input("Pressione Enter para voltar.")
            return

        # Menu com setas para escolher o arquivo
        escolhido = questionary.select(
            "Selecione um arquivo para abrir (ou pressione Esc para voltar):",
            choices=arquivos
        ).ask()

        if escolhido:
            caminho_completo = os.path.join(caminho, escolhido)
            print(f"Abrindo: {caminho_completo}")

            try:
                os.startfile(caminho_completo)  # Apenas Windows
            except AttributeError:
                print("❌ 'os.startfile' só funciona no Windows.")
            except Exception as e:
                print(f"❌ Erro ao abrir: {e}")

        input("\nPressione Enter para voltar ao menu.")

    except Exception as e:
        print(f"❌ Erro: {e}\n")

def renomear():
    limpar_tela()
    origem = input("Nome atual do arquivo ou diretório: ")
    destino = input("Novo nome: ")
    if not confirmar_acao(f"Tem certeza que deseja renomear '{origem}' para '{destino}'?"):
        print("❌ Ação cancelada.\n")
        return
    try:
        os.rename(origem, destino)
        registrar_acao('renomear', {'de': destino, 'para': origem})
        print("✅ Renomeado com sucesso.\n")
    except Exception as e:
        print(f"❌ Erro: {e}\n")

def mover():
    limpar_tela()
    origem = input("Caminho do arquivo ou diretório a mover: ")
    destino = input("Novo caminho/diretório de destino: ")
    if not confirmar_acao(f"Tem certeza que deseja mover '{origem}' para '{destino}'?"):
        print("❌ Ação cancelada.\n")
        return
    try:
        shutil.move(origem, destino)
        registrar_acao('mover', {'de': destino, 'para': origem})
        print("✅ Movido com sucesso.\n")
    except Exception as e:
        print(f"❌ Erro: {e}\n")

def apagar():
    limpar_tela()
    caminho = input("Caminho do arquivo ou diretório a apagar: ")
    if not confirmar_acao(f"Tem certeza que deseja apagar '{caminho}'?"):
        print("❌ Ação cancelada.\n")
        return
    try:
        nome_backup = os.path.join(LIXEIRA, os.path.basename(caminho))
        shutil.move(caminho, nome_backup)
        registrar_acao('apagar', {'original': caminho, 'backup': nome_backup})
        print("🗑️ Apagado (movido para lixeira temporária).\n")
    except Exception as e:
        print(f"❌ Erro: {e}\n")

def limpar_temporarios():
    limpar_tela()
    sistema = platform.system()
    caminhos = [os.environ.get('TEMP'), r'C:\\Windows\\Temp'] if sistema == 'Windows' else ['/tmp']
    print("🧹 CUIDADO! Essa ação pode apagar arquivos em uso por outros programas.")
    for c in caminhos:
        print(f"  - {c}")
    if not confirmar_acao("Tem certeza que deseja continuar com a limpeza?"):
        print("❌ Ação cancelada.\n")
        return
    for caminho in caminhos:
        if not caminho or not os.path.exists(caminho):
            continue
        try:
            for arquivo in os.listdir(caminho):
                caminho_completo = os.path.join(caminho, arquivo)
                try:
                    if os.path.isfile(caminho_completo) or os.path.islink(caminho_completo):
                        os.remove(caminho_completo)
                    elif os.path.isdir(caminho_completo):
                        shutil.rmtree(caminho_completo)
                except Exception as e:
                    print(f"⚠️ Erro ao remover '{caminho_completo}': {e}")
            print(f"✅ Temporários limpos em: {caminho}\n")
        except Exception as e:
            print(f"❌ Erro ao acessar '{caminho}': {e}")

def exibir_historico():
    limpar_tela()
    if not historico:
        print("📜 Nenhuma ação registrada no histórico.\n")
        input("Pressione Enter para voltar ao menu.")
        return
    print("📜 Histórico de ações:\n")
    for i, h in enumerate(historico, 1):
        print(f"{i}. {h['acao']} - {h['dados']}")
    print("\nDigite o número da ação para desfazer ou pressione Enter para voltar.")
    escolha = input("Número da ação para desfazer: ").strip()
    if escolha.isdigit():
        indice = int(escolha) - 1
        if 0 <= indice < len(historico):
            desfazer_acao(indice)
        else:
            print("⚠️ Número inválido.")
            input("Pressione Enter para continuar.")

def desfazer_acao(indice):
    acao = historico.pop(indice)
    tipo = acao['acao']
    dados = acao['dados']
    try:
        if tipo == 'renomear':
            os.rename(dados['de'], dados['para'])
            print("↩️ Renomeação desfeita.")
        elif tipo == 'mover':
            shutil.move(dados['de'], dados['para'])
            print("↩️ Movimento desfeito.")
        elif tipo == 'criar_diretorio':
            shutil.rmtree(dados['nome'])
            print("↩️ Diretório removido.")
        elif tipo == 'apagar':
            shutil.move(dados['backup'], dados['original'])
            print("↩️ Arquivo restaurado.")
        else:
            print("⚠️ Tipo de ação desconhecido.")
    except Exception as e:
        print(f"❌ Erro ao desfazer: {e}")
    input("Pressione Enter para continuar.")

def deseja_continuar():
    return confirmar_acao("Deseja realizar outra ação")

def mostrar_menu():
    return questionary.select(
        "Selecione uma opção:",
        choices=[
            "Criar diretório",
            "Listar arquivos",
            "Renomear arquivo/diretório",
            "Mover arquivo/diretório",
            "Apagar arquivo/diretório",
            "Apagar arquivos temporarios",
            "Ver histórico de ações",
            "Sair"
        ]
    ).ask()

def main():
    while True:
        limpar_tela()
        opcao = mostrar_menu()

        if opcao == "Criar diretório":
            criar_diretorio()
        elif opcao == "Listar arquivos":
            listar_arquivos()
        elif opcao == "Renomear arquivo/diretório":
            renomear()
        elif opcao == "Mover arquivo/diretório":
            mover()
        elif opcao == "Apagar arquivo/diretório":
            apagar()
        elif opcao == "Apagar arquivos temporarios":
            limpar_temporarios()
        elif opcao == "Ver histórico de ações":
            exibir_historico()
        elif opcao == "Sair":
            print("👋 Saindo do programa.")
            break

        if not deseja_continuar():
            print("👋 Encerrando. Até mais!")
            break

if __name__ == "__main__":
    main()