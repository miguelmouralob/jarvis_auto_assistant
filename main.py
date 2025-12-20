import speech_recognition as sr
import os
import time
import json
import pyautogui
import pyperclip

MODO_COMANDO = "comando"
MODO_DITADO = "ditado"

idioma_atual = "pt-BR"

modo_atual = MODO_COMANDO

WAKE_WORDS = ["astra", "assistente", "help"]

ACOES_COM_WAKEWORD = ["open_browser", "close_browser", "create_alarm" , "exit_program"]

config = {}
rodando = True


def carregar_config():
    with open('config.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def carregar_comandos():
    with open('commands.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def carregar_atalhos():
    with open('shortcuts.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def carregar_musicas():
    with open('music_commands.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def detectar_wake_word(comando):
    for wake in WAKE_WORDS:
        if comando.startswith(wake):
            return comando.replace(wake, '', 1).strip()
    return None


def detectar_comando_alarme(comando):
    comando = comando.lower()

    comando_sem_wake = detectar_wake_word(comando)
    if not comando_sem_wake:
        return False
    
    return "criar alarme" in comando_sem_wake or "set alarm" in comando_sem_wake


def ouvir_comando(idioma = "pt-BR"):
    recognizer = sr.Recognizer()
    
    recognizer.pause_threshold = 2.0
    recognizer.non_speaking_duration = 1.5
    recognizer.phrase_threshold = 0.5
    
    with sr.Microphone() as source:
        print("Ouvindo...")
        recognizer.adjust_for_ambient_noise(source, duration = 1.5)
        audio = recognizer.listen(source)
        
    try:
        comando = recognizer.recognize_google(audio, language=idioma)
        print(f"Você disse: {comando}")
        return comando.lower()
    
    except sr.UnknownValueError:
        print("Desculpe, não entendi o que você disse.")
        return ""
    
    except sr.RequestError:
        print("Erro ao se conectar ao serviço de reconhecimento de fala.")
        return ""


def interpretar_comando(comando, comandos):
    global idioma_atual
    
    if detectar_comando_alarme(comando):
        processar_comando_alarme(comando)
        return True
    
    comando = comando.strip().lower()
    
    if comando.startswith("tocar ") or comando.startswith("play "):
        processar_comando_musica(comando)
        return True
    
    acao_exige_wake = False
    comando_sem_wake = comando

    for nome,dados in comandos.items():
        if any(frase.lower() in comando for frase in dados.get("keywords", [])):
            if dados["action"] in ACOES_COM_WAKEWORD:
                acao_exige_wake = True
                break
    
    if acao_exige_wake:
        comando_limpo = detectar_wake_word(comando)
        if not comando_limpo:
            print("Wake word necessária para comando.")
            return True
        
        print("Wake word detectada.")
        comando_sem_wake = comando_limpo
    else:
        comando_sem_wake = comando
    
    
    for nome, dados in comandos.items():
        if any(frase.lower() in comando_sem_wake for frase in dados.get("keywords", [])):
            acao = dados["action"]
            
            if acao == "exit_program":
                encerrar_programa()
                return False
            
            if acao == "set_english_mode":
                idioma_atual = "en-US"
                print("Idioma alterado para Inglês.")
                return True
            elif acao == "set_portuguese_mode":
                idioma_atual = "pt-BR"
                print("Idioma alterado para Português.")
                return True
            else:
                executar_acao(acao)
                return True
    
    print("Comando não reconhecido.")
    return True


def start_dictation():
    global modo_atual
    modo_atual = MODO_DITADO
    print("Modo ditado ativado.")


def executar_acao(acao):
    if acao == "open_browser":
        abrir_navegador()
    
    elif acao == "close_browser":
        fechar_navegador()
    
    elif acao == "new_tab":
        nova_guia()
    
    elif acao == "close_tab":
        fechar_guia()
    
    elif acao == "input_text":
        text_selector()
    
    elif acao == "text_enter":
        enter_text()
    
    elif acao == "prev_tab":
        guia_anterior()
    
    elif acao == "next_tab":
        guia_posterior()
    
    elif acao == "start_dictation":
        start_dictation()
    
    else:
        print("Comando não reconhecido.")


def abrir_navegador():
    try:
        print("Abrindo o navegador...")
        os.startfile(config["browser_path"])
        time.sleep(3)
    except FileNotFoundError:
        print("Erro: Caminho do navegador não encontrado. Verifique o arquivo config.json.")
    except Exception as e:
        print(f"Erro ao tentar abrir o navegador: {e}")


def fechar_navegador():
    print("Fechando o navegador...")
    pyautogui.hotkey('alt', 'f4')
    time.sleep(3)


def nova_guia():
    print("Abrindo uma nova guia...")
    pyautogui.hotkey('ctrl', 't')
    time.sleep(0.5)


def fechar_guia():
    print("Fechando a guia atual...")
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(0.5)


def text_selector():
    print("Selecionando o campo de texto...")
    pyautogui.hotkey('ctrl', 'e')
    time.sleep(0.5)


def guia_anterior():
    print("Indo para a guia anterior...")
    pyautogui.hotkey('ctrl', 'pgup')
    time.sleep(0.5)


def guia_posterior():
    print("Indo para a próxima guia...")
    pyautogui.hotkey('ctrl', 'pgdn')
    time.sleep(0.5)


def processar_comando_musica(comando):
    global music_commands
    
    comando = comando.replace("tocar ", "").replace("play ", "").strip().lower()
    
    for entrada in music_commands:
        nomes_artista = entrada.get("nomes", [])
        musicas = entrada.get("musicas", {})
    
    for nomes_artista in nomes_artista:
        nome_normalizado = nomes_artista.lower()
        if nome_normalizado in comando:
            musica = comando.replace(nome_normalizado, "").strip().lower()
            tocar_musica(nomes_artista, musica, musicas)
            return
    
    print("Artista não reconhecido.")


def tocar_musica(nome_artista_original, musica_falada, musicas_dict):
    musica_falada = musica_falada.lower().strip()
    
    if musica_falada in musicas_dict:
        dados_musica = musicas_dict[musica_falada]
    else:
        matches = [m for m in musicas_dict.keys() if musica_falada in m or m in musica_falada]
        if not matches:
            print(f"Música '{musica_falada}' não encontrada para {nome_artista_original}.")
            return

        musica_encontrada = matches[0]
        dados_musica = musicas_dict[musica_encontrada]
        print(f"Música reconhecida como '{musica_encontrada}'.")
    
        musica_encontrada = musica_falada
    
    if "youtube" in dados_musica:
        link = dados_musica["youtube"]
        print("Abrindo no Youtube...")
    elif "spotify" in dados_musica:
        link = dados_musica["spotify"]
        print("Abrindo no Spotify...")
    else:
        print("Nenhum link disponível para essa música.")
        return

    os.startfile(link)


def extrair_duracao(comando):
    partes = comando.split()
    
    for i, palavra in enumerate(partes):
        if palavra.isdigit():
            valor = int(palavra)
            
            if i + 1 < len(partes):
                unidade = partes[i + 1]
                
                if unidade.startswith("seg"):
                    return valor
                elif unidade.startswith("min"):
                    return valor * 60
                elif unidade.startswith("hor"):
                    return valor * 3600

    return None


def processar_comando_alarme(comando):
    comando_limpo = detectar_wake_word(comando)
    if not comando_limpo:
        print("Wake word necessária para comando de alarme.")
        return
    
    duracao = extrair_duracao(comando_limpo)
    
    if duracao is None:
        print("Duração do alarme não especificada ou inválida.")
        return
    
    criar_alarme(duracao)


def criar_alarme(duracao):
    inicio = time.time()
    fim = inicio + duracao

    print(f"Alarme definido para daqui a {duracao} segundos.")

    try:
        while True:
            agora = time.time()
            tempo_restante = fim - agora

            if tempo_restante <= 0:
                print(f"\rTempo restante: 00:00:00.000", end="")
                print("\n\aBEEP! O tempo acabou!")
                break

            segundos_total = int(tempo_restante)
            horas = segundos_total // 3600
            minutos = (segundos_total % 3600) // 60
            segundos = segundos_total % 60
            milissegundos = int((tempo_restante - segundos_total) * 1000)

            print(
                f"\rTempo restante: {horas:02}:{minutos:02}:{segundos:02}.{milissegundos:03}",
                end=""
            )

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nAlarme interrompido pelo usuário.")


def digitar_texto(texto):
    global modo_atual, idioma_atual
    
    texto = texto.lower().strip()
    
    if texto in ["sair do ditado", "exit dictation"]:
        modo_atual = MODO_COMANDO
        print("Saindo do modo ditado. Voltando ao modo comando.")
        return
    
    if texto in ["modo_inglês", "english mode"]:
        idioma_atual = "en-US"
        print("Idioma alterado para Inglês.")
        return
    elif texto in ["modo_português", "portuguese mode"]:
        idioma_atual = "pt-BR"
        print("Idioma alterado para Português.")
        return
    
    if texto in atalhos:
        texto_para_digitar = atalhos[texto]
        print(f"Atalho reconhecido: {texto} -> {texto_para_digitar}")
    else:
        texto_para_digitar = texto
        print(f"Digitando o texto: {texto_para_digitar}")
    
    pyperclip.copy(texto_para_digitar)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    
    modo_atual = MODO_COMANDO
    print("Voltando ao modo comando.")


def enter_text():
    pyautogui.press('enter')
    time.sleep(0.5)


def encerrar_programa():
    global rodando
    print("Encerrando o programa...")
    rodando = False


if __name__ == "__main__":
    config = carregar_config()
    comandos = carregar_comandos()
    atalhos = carregar_atalhos()
    music_commands = carregar_musicas()
    
    while rodando:
        comando = ouvir_comando(idioma=idioma_atual)
        if not comando:
            continue
        
        if modo_atual == MODO_COMANDO:
            rodando = interpretar_comando(comando, comandos)
            
        elif modo_atual == MODO_DITADO:
            digitar_texto(comando)
    
    print("Programa encerrado.")
