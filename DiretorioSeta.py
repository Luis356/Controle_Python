import os
import shutil
import platform
import questionary

LIXEIRA = os.path.join(os.getcwd(), '__lixeira_temporaria__')
os.makedirs(LIXEIRA, exist_ok=True)

historico = []

def limpar_tela():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def confirmar_acao(msg):
    while True:
        resp = input(f"{msg} (s/n): ").strip().lower()
        if resp in ['s', 'sim']:
            return True
        elif resp in ['n', 'nao', 'não']:
            return False
        else:
            print("⚠️ Digite 's' ou 'n'.")

def registrar_acao(tipo, dados):
    historico.append({'acao': tipo, 'dados': dados})

def criar_diretorio():
    limpar_tela()
    nome = input("Digite o nome do novo item: ").strip()
    tipo = questionary.select("Qual tipo deseja criar?", choices=["Pasta", "Arquivo .txt"]).ask()

    if tipo == "Pasta":
        if confirmar_acao(f"Criar pasta '{nome}'?"):
            try:
                os.makedirs(nome)
                registrar_acao('criar_diretorio', {'nome': nome})
                print("✅ Pasta criada.")
            except Exception as e:
                print(f"❌ Erro: {e}")
    else:
        if confirmar_acao(f"Criar arquivo '{nome}.txt'?"):
            try:
                with open(f"{nome}.txt", 'w') as f:
                    f.write("")  # cria vazio
                registrar_acao('criar_arquivo', {'nome': f"{nome}.txt"})
                print("✅ Arquivo criado.")
            except Exception as e:
                print(f"❌ Erro: {e}")

def listar_arquivos(caminho='.'):
    while True:
        limpar_tela()
        print(f"📁 Listando: {os.path.abspath(caminho)}\n")
        try:
            itens = [f for f in os.listdir(caminho) if f != '__lixeira_temporaria__']
            if not itens:
                print("📂 Pasta vazia.")
                input("Enter para voltar.")
                return

            escolhido = questionary.select("Escolha um item:", choices=itens + ['< Voltar>']).ask()
            if not escolhido or escolhido == '< Voltar>':
                return

            caminho_completo = os.path.join(caminho, escolhido)
            if os.path.isdir(caminho_completo):
                caminho = caminho_completo  # entra na pasta e repete
            else:
                if confirmar_acao(f"Deseja abrir o arquivo '{escolhido}'?"):
                    try:
                        os.startfile(caminho_completo)
                    except Exception as e:
                        print(f"❌ Erro ao abrir: {e}")
                input("Pressione Enter para voltar.")
                return
        except Exception as e:
            print(f"❌ Erro: {e}")
            input("Pressione Enter para voltar.")
            return

def renomear():
    limpar_tela()
    caminho = input("Digite o caminho (Enter = atual): ") or '.'
    if not os.path.isdir(caminho): print("❌ Caminho inválido."); return

    itens = [f for f in os.listdir(caminho) if f != '__lixeira_temporaria__']
    if not itens: print("📁 Vazio."); return
    esc = questionary.select("Escolha para renomear:", choices=itens + ['< Voltar>']).ask()
    if esc == '< Voltar>': return

    origem = os.path.join(caminho, esc)
    novo_nome = input("Novo nome: ").strip()
    destino = os.path.join(caminho, novo_nome)

    if confirmar_acao(f"Renomear '{esc}' para '{novo_nome}'?"):
        try:
            os.rename(origem, destino)
            registrar_acao('renomear', {'de': destino, 'para': origem})
            print("✅ Renomeado.")
        except Exception as e:
            print(f"❌ Erro: {e}")

def mover():
    limpar_tela()
    caminho = input("Digite o caminho (Enter = atual): ") or '.'
    if not os.path.isdir(caminho): print("❌ Caminho inválido."); return

    itens = [f for f in os.listdir(caminho) if f != '__lixeira_temporaria__']
    if not itens: print("📁 Vazio."); return
    esc = questionary.select("Escolha para mover:", choices=itens + ['< Voltar>']).ask()
    if esc == '< Voltar>': return

    origem = os.path.join(caminho, esc)
    destino = input("Novo destino (caminho completo): ").strip()
    if confirmar_acao(f"Mover '{esc}' para '{destino}'?"):
        try:
            shutil.move(origem, destino)
            registrar_acao('mover', {'de': destino, 'para': origem})
            print("✅ Movido.")
        except Exception as e:
            print(f"❌ Erro: {e}")

def apagar():
    limpar_tela()
    caminho = input("Digite o caminho (Enter = atual): ") or '.'
    if not os.path.isdir(caminho): print("❌ Caminho inválido."); return

    itens = [f for f in os.listdir(caminho) if f != '__lixeira_temporaria__']
    if not itens: print("📁 Vazio."); return
    esc = questionary.select("Escolha para apagar:", choices=itens + ['< Voltar>']).ask()
    if esc == '< Voltar>': return

    caminho_completo = os.path.join(caminho, esc)
    if confirmar_acao(f"Deseja apagar '{caminho_completo}'?"):
        try:
            backup = os.path.join(LIXEIRA, os.path.basename(caminho_completo))
            shutil.move(caminho_completo, backup)
            registrar_acao('apagar', {'original': caminho_completo, 'backup': backup})
            print("🗑️ Movido para lixeira.")
        except Exception as e:
            print(f"❌ Erro: {e}")

def exibir_historico():
    limpar_tela()
    if not historico:
        print("📜 Sem histórico.")
        input("Enter para voltar.")
        return

    escolhas = [f"{i+1}. {h['acao']} - {h['dados']}" for i, h in enumerate(historico)]
    escolhas.append("< Voltar>")
    escolha = questionary.select("Histórico de ações:", choices=escolhas).ask()
    if escolha == "< Voltar>": return
    desfazer_acao(int(escolha.split('.')[0]) - 1)

def desfazer_acao(indice):
    acao = historico.pop(indice)
    tipo = acao['acao']
    dados = acao['dados']
    try:
        if tipo == 'criar_diretorio' or tipo == 'criar_arquivo':
            shutil.rmtree(dados['nome']) if os.path.isdir(dados['nome']) else os.remove(dados['nome'])
            print("↩️ Removido.")
        elif tipo == 'renomear':
            os.rename(dados['de'], dados['para'])
            print("↩️ Renomeação desfeita.")
        elif tipo == 'mover':
            shutil.move(dados['de'], dados['para'])
            print("↩️ Movimento desfeito.")
        elif tipo == 'apagar':
            shutil.move(dados['backup'], dados['original'])
            print("↩️ Arquivo restaurado.")
    except Exception as e:
        print(f"❌ Erro ao desfazer: {e}")
    input("Enter para continuar.")

def mostrar_menu():
    return questionary.select("Menu principal:", choices=[
        "Criar diretório/arquivo",
        "Listar arquivos",
        "Renomear",
        "Mover",
        "Apagar",
        "Ver histórico de ações",
        "Sair"
    ]).ask()

def main():
    while True:
        limpar_tela()
        op = mostrar_menu()
        pergunta = True

        match op:
            case "Criar diretório/arquivo":
                criar_diretorio()
            case "Listar arquivos":
                pergunta = listar_arquivos()
            case "Renomear":
                renomear()
            case "Mover":
                mover()
            case "Apagar":
                apagar()
            case "Ver histórico de ações":
                exibir_historico()
                pergunta = False
            case "Sair":
                break

        if pergunta and not confirmar_acao("Deseja realizar outra ação?"):
            break

    if os.path.exists(LIXEIRA):
        if historico:
            if confirmar_acao("Existem ações pendentes. Deseja mesmo excluir a lixeira temporária?"):
                shutil.rmtree(LIXEIRA)
                print("🧹 Lixeira excluída.")
            else:
                print("⚠️ Lixeira mantida.")
        else:
            shutil.rmtree(LIXEIRA)
            print("🧹 Lixeira excluída.")

    print("👋 Até mais!")

if __name__ == "__main__":
    main()