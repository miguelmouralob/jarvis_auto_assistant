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


def ouvir_comando(idioma = "pt-BR"):
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Ouvindo...")
        recognizer.adjust_for_ambient_noise(source)
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
    
    comando = comando.strip().lower()
    
    EXIT_PHRASES = ["encerrar programa", "exit program", "quit program"]
    
    if comando in EXIT_PHRASES:
        print("Encerrando o programa...")
        return False

    for nome, dados in comandos.items():
        if any(frase.strip().lower() in comando for frase in dados.get("keywords", [])):
            if dados["action"] == "set_english_mode":
                idioma_atual = "en-US"
                print("Idioma alterado para Inglês.")
                return True
            elif dados["action"] == "set_portuguese_mode":
                idioma_atual = "pt-BR"
                print("Idioma alterado para Português.")
                return True
            else:
                executar_acao(dados["action"])
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
    
    while rodando:
        comando = ouvir_comando(idioma=idioma_atual)
        if not comando:
            continue
        
        if modo_atual == MODO_COMANDO:
            rodando = interpretar_comando(comando, comandos)
            
        elif modo_atual == MODO_DITADO:
            digitar_texto(comando)
    
    print("Programa encerrado.")
