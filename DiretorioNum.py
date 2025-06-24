import os           # Esse módulo fornece funções para interagir com o sistema operacional.
# Funções para limpar a tela, criar diretório, listar arquivos, renomear, mover e apagar arquivos/diretórios.

import shutil       # Esse módulo serve para operações de alto nível com arquivos e pastas, como cópia e movimentação.
# Mover e apagar diretórios inteiros com conteúdo.

import platform     # Esse módulo serve para identificar o sistema operacional em que o programa está rodando.
# Detectar o sistema operacional para limpar o terminal.

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

def criar_diretorio():
    limpar_tela()
    nome = input("Digite o nome do diretório a ser criado: ")
    if not confirmar_acao(f"Tem certeza que deseja criar o diretório '{nome}'?"):
        print("❌ Ação cancelada.\n")
        return
    try:
        os.makedirs(nome)
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
    
    try:
        limpar_tela()
        arquivos = os.listdir(caminho)
        print(f"\n📂 Arquivos em '{caminho}':")
        for arquivo in arquivos:
            print(f"  - {arquivo}")
        print()
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
        if os.path.isdir(caminho):
            shutil.rmtree(caminho)
        else:
            os.remove(caminho)
        print("🗑️ Apagado com sucesso.\n")
    except Exception as e:
        print(f"❌ Erro: {e}\n")

def limpar_temporarios():
    limpar_tela()
    sistema = platform.system()
    
    if sistema == 'Windows':
        caminhos = [os.environ.get('TEMP'), r'C:\Windows\Temp']
    else:
        caminhos = ['/tmp']

    print("🧹 CUIDADO! Essa ação pode apagar arquivos em uso por outros programas.")
    print("Pastas que serão limpas:")
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
            print(f"✅ Arquivos temporários limpos em: {caminho}\n")
        except Exception as e:
            print(f"❌ Erro ao acessar '{caminho}': {e}")

def mostrar_menu():
    print("========== GERENCIADOR DE ARQUIVOS ==========")
    print("1. Criar diretório")
    print("2. Listar arquivos")
    print("3. Renomear arquivo/diretório")
    print("4. Mover arquivo/diretório")
    print("5. Apagar arquivo/diretório")
    print("6. Apagar arquivos temporarios")
    print("7. Sair")
    print("=============================================")

def deseja_continuar():
    return confirmar_acao("Deseja realizar outra ação")

def main():
    while True:
        limpar_tela()
        mostrar_menu()
        opcao = input("Escolha uma opção (1-7): ")

        match opcao:
            case '1':
                criar_diretorio()
            case '2':
                listar_arquivos()
            case '3':
                renomear()
            case '4':
                mover()
            case '5':
                apagar()
            case '6':
                limpar_temporarios()
            case '7':
                print("👋 Saindo do programa.")
                break
            case _:
                print("❌ Opção inválida. Tente novamente.\n")
                continue

        if not deseja_continuar():
            print("👋 Encerrando. Até mais!")
            break

if __name__ == "__main__":
    main()