# Jarvis Auto v4 🎙️🤖

Assistente local por voz desenvolvido em Python, capaz de executar comandos no sistema operacional e interagir com campos de texto a partir de ditado por voz, com foco em automação de tarefas simples do dia a dia.

## 🚀 Funcionalidades

### 🌟 O que há de Novo na v4
Introdução de maior estabilidade e segurança com uso de "Wake Words Críticas" --> (Palavras de Ativação), garantindo que o assistente reaja quando for explicitamente chamado para uma ação importante.

```bash
Ouvindo...
Você disse: Abrir navegador
Wake word necessária para comando.
Ouvindo...
Você disse: ASSISTENTE Abrir navegador
Wake word detectada.
Abrindo o navegador...
```

### 🎛️ Modo Comando
* Reconhecimento de voz (pt-BR / en-US)
* Sistema de comandos configurável via JSON (`commands.json`)
* Wake words críticas para aumentar segurança 
* Abertura e fechamento de navegador
* Controle de abas (nova, fechar, anterior, posterior)
* Seleção do campo de texto
* Comando para alterar e auxiliar no uso de palavras entre os idiomas
* Comando opcional de pesquisa (`Enter`)
* Encerramento limpo do assistente por comando de voz

### 📝 Modo Ditado
* Ditado por voz para campos de texto
* Preenchimento automático do campo ativo
* Sistema de atalhos para URLs (ex: “youtube” → youtube.com)
* Retorno automático ao modo comando após o ditado

## 🧠 Conceito de Funcionamento

O assistente opera com dois estados:

* **Modo Comando**: interpreta palavras-chave e executa ações
* **Modo Ditado**: tudo o que é falado é convertido em texto digitado

Essa separação garante mais controle e evita conflitos entre comandos e texto livre.

## 🧱 Estrutura do Projeto

```tree
jarvis/
├── main.py
├── commands.json
├── shortcuts.json
├── config.json         # Arquivo local com configurações sensíveis (não versionado)
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Configuração

O projeto requer um arquivo de configuração local, o `config.json`, para armazenar o caminho do executável do navegador, garantindo a portabilidade e a segurança.

Crie um arquivo `config.json` na raiz do projeto com o seguinte formato:

```json
{
  "browser_path": "C:\\Caminho\\Para\\Seu\\Navegador\\firefox.exe" 
  // Nota: Use barras duplas "\\" ou apenas uma barra "/" em caminhos do Windows no JSON.
}
```

## 📦 Dependências

O projeto requer **Python 3.10+** e as seguintes bibliotecas:

* SpeechRecognition
* PyAudio
* PyAutoGUI
* Pyperclip

**Instale as Dependências:**
    ```
    pip install -r requirements.txt
    ```

## ▶️ Execução

Após configurar o `config.json` e instalar as dependências, execute o assistente com o seguinte comando:

```bash
python main.py
```