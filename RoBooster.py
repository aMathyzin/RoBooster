import sys
import ctypes
import time
import os
import keyboard
import shutil
import winreg as reg
import subprocess
import tempfile
import requests

def baixar_e_definir_icone(url):
    resposta = requests.get(url)
    if resposta.status_code == 200:
        temp_dir = tempfile.gettempdir()
        caminho_icone = os.path.join(temp_dir, "RobloxPlus.ico")
        with open(caminho_icone, "wb") as arquivo:
            arquivo.write(resposta.content)

        ctypes.windll.kernel32.SetConsoleIcon(ctypes.windll.user32.LoadImageW(None, caminho_icone, 1, 0, 0, 0x00000010))
    else:
        print("Falha ao baixar o ícone.")

baixar_e_definir_icone("https://amathyzin.tech/RobloxPlus.ico")

def definir_titulo_janela_console(titulo):
    ctypes.windll.kernel32.SetConsoleTitleW(titulo)

definir_titulo_janela_console("RoBooster")


roblox_otimizado = False

def is_administrador():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_administrador():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    print("Por favor, execute este programa como administrador.")
    sys.exit()

texto_ascii = """
                            ██████╗   ██████╗  ██████╗  ██╗       ██████╗  ██╗  ██╗
                            ██╔══██╗ ██╔═══██╗ ██╔══██╗ ██║      ██╔═══██╗ ╚██╗██╔╝
                            ██████╔╝ ██║   ██║ ██████╔╝ ██║      ██║   ██║  ╚███╔╝
                            ██╔══██╗ ██║   ██║ ██╔══██╗ ██║      ██║   ██║  ██╔██╗
                            ██║  ██║ ╚██████╔╝ ██████╔╝ ███████╗ ╚██████╔╝ ██╔╝ ██╗
                            ╚═╝  ╚═╝  ╚═════╝  ╚═════╝  ╚══════╝  ╚═╝ ╚═╝  ╚═╝  ╚═╝
"""

def tamanho_terminal():
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except OSError:
        return 80, 24

def gerar_gradiente_vermelho(inicio, fim, etapas):
    return [(inicio + (fim - inicio) * i // etapas) for i in range(etapas)]

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

num_frames = 65  
fps = 80

def zoom_texto(texto, fator, largura_term):
    texto_zoom = ""
    linhas = texto.split('\n')
    comprimento_max_linha = max(len(linha) for linha in linhas)
    for linha in linhas:
        espacos = " " * ((largura_term - comprimento_max_linha) // 2)
        texto_zoom += espacos + linha[:int(len(linha) * fator)] + "\n"
    return texto_zoom

def finalizar_processo(nome_processo):
    try:
        subprocess.run(["taskkill", "/F", "/IM", nome_processo], check=True)
        print(f"Processo {nome_processo} finalizado com sucesso.")
    except subprocess.CalledProcessError:
        print(f"Não foi possível finalizar o processo {nome_processo}.")

def limpar_roblox():
    finalizar_processo("RobloxPlayerBeta.exe")

    caminhos_temp_roblox = [
        os.path.join(os.getenv('TEMP'), 'Roblox'),
        os.path.join(os.getenv('LOCALAPPDATA'), 'Roblox', 'logs'),
        os.path.join(os.getenv('LOCALAPPDATA'), 'Roblox', 'cache')
    ]

    caminhos_temp_windows = [
        os.getenv('TEMP'),
        os.getenv('TMP')
    ]

    caminhos_log_windows = [
        os.path.join(os.getenv('SystemRoot'), 'System32', 'winevt', 'Logs')
    ]

    def excluir_arquivos_e_dirs(caminhos):
        for caminho in caminhos:
            if os.path.exists(caminho):
                for root, dirs, files in os.walk(caminho, topdown=False):
                    for name in files:
                        try:
                            os.remove(os.path.join(root, name))
                        except Exception as e:
                            print(f"Erro ao excluir arquivo: {os.path.join(root, name)} - {e}")
                    for name in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, name))
                        except Exception as e:
                            print(f"Erro ao excluir diretório: {os.path.join(root, name)} - {e}")
                if os.path.isdir(caminho):
                    try:
                        shutil.rmtree(caminho)
                    except Exception as e:
                        print(f"Erro ao excluir diretório: {caminho} - {e}")

    print("Limpando arquivos temporários do Roblox...")
    excluir_arquivos_e_dirs(caminhos_temp_roblox)

    print("Limpando arquivos temporários do Windows...")
    excluir_arquivos_e_dirs(caminhos_temp_windows)

    print("Limpando arquivos de log do sistema...")
    excluir_arquivos_e_dirs(caminhos_log_windows)

    print("Limpeza concluída.")

def otimizar_roblox():
    finalizar_processo("RobloxPlayerBeta.exe")

    try:
        caminho_reg = r'SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers'
        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, caminho_reg, 0, reg.KEY_WRITE) as key:
            reg.SetValueEx(key, 'TdrLevel', 0, reg.REG_DWORD, 0)

        ctypes.windll.user32.SystemParametersInfoW(20, 0, None, 0)  # SPI_SETUIEFFECTS

        print("Roblox otimizado com sucesso.")
    except PermissionError:
        print("Permissão negada: Execute o script como administrador.")
    except Exception as e:
        print(f"Ocorreu um erro ao otimizar o Roblox: {e}")

def iniciar_roblox_otimizado():
    try:
        caminho_bloxstrap = os.path.join(os.getenv('LOCALAPPDATA'), 'Bloxstrap', 'Bloxstrap.exe')
        subprocess.Popen([caminho_bloxstrap], shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.HIGH_PRIORITY_CLASS)
        print("O Processo do Roblox foi iniciado!")
        time.sleep(3)
        sys.exit()
    except Exception as e:
        print(f"Ocorreu um erro ao iniciar o Roblox otimizado: {e}")

def tratar_pressao_botao(largura_term, altura_term):
    global roblox_otimizado

    if roblox_otimizado:
        texto_botoes = "\n" + "─" * largura_term + "\n" + \
                       " " * ((largura_term - 20) // 2) + "[1] Iniciar Roblox otimizado" + "\n" + \
                       "─" * largura_term + "\n"
    else:
        texto_botoes = "\n" + "─" * largura_term + "\n" + \
                       " " * ((largura_term - 20) // 2) + "[1] Limpar o Roblox" + " " * 5 + "[2] Otimizar o Roblox" + "\n" + \
                       " " * ((largura_term - 20) // 2) + "[3] Iniciar Roblox otimizado" + "\n" + \
                       "─" * largura_term + "\n"

    print(texto_botoes)
    while True:
        if keyboard.is_pressed('1'):
            if roblox_otimizado:
                iniciar_roblox_otimizado()
                break
            else:
                print("Limpando o Roblox...")
                limpar_roblox()
                roblox_otimizado = True
                break
        elif keyboard.is_pressed('2') and not roblox_otimizado:
            print("Otimizando o Roblox...")
            otimizar_roblox()
            roblox_otimizado = True
            break
        elif keyboard.is_pressed('3') and roblox_otimizado:
            iniciar_roblox_otimizado()
            break
        time.sleep(0.1)

def definir_propriedades_janela_cmd():
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()

    style = ctypes.windll.user32.GetWindowLongW(hwnd, -16)
    style &= ~0x00040000  # WS_SIZEBOX
    style &= ~0x00020000  # WS_MAXIMIZEBOX
    ctypes.windll.user32.SetWindowLongW(hwnd, -16, style)

    style &= ~0x00010000  # WS_MAXIMIZE
    ctypes.windll.user32.SetWindowLongW(hwnd, -16, style)

    style &= ~0x00000008  # WS_THICKFRAME
    ctypes.windll.user32.SetWindowLongW(hwnd, -16, style)

definir_propriedades_janela_cmd()

largura_term, altura_term = tamanho_terminal()

while True:
    for frame in range(num_frames):
        limpar_terminal()

        etapa = (frame * 255 // num_frames)
        gradiente_vermelho = gerar_gradiente_vermelho(0 + etapa, 255 - etapa, len(texto_ascii))

        fator_zoom = frame / num_frames

        texto_zoom = zoom_texto(texto_ascii, fator_zoom, largura_term)

        linhas = texto_zoom.split('\n')

        for i, linha in enumerate(linhas):
            if linha.strip():
                intensidade_vermelho = gradiente_vermelho[i % len(gradiente_vermelho)]
                codigo_cor = f'\033[38;2;{intensidade_vermelho};0;0m'
                print(codigo_cor + linha)

        time.sleep(1 / fps)

    print('\033[0m')

    tratar_pressao_botao(largura_term, altura_term)
