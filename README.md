# Jarvis Auto v5 🎙️🤖

Assistente local por voz desenvolvido em Python, capaz de executar comandos no sistema operacional e interagir com campos de texto a partir de ditado por voz, com foco em automação de tarefas simples do dia a dia.

## 🚀 Funcionalidades

### 🌟 O que há de Novo na v5
Possibilidade de pesquisar por músicas. Suporte de línguas para PT-BR e EN-US. Links específicos para Youtube e Spotify.
* Começar o comando dizendo "Tocar" ou "Play";
* Dizer o nome do artista --> será verificado se consta no arquivo;
* Dizer o nome da música --> será verificado se consta no arquivo; 

```bash
Você disse: tocar xuxa parabéns
Abrindo no Youtube
```

*OBS* --> Nesse exemplo, a palavra referência "parabéns", é p/ a música "Parabéns da Xuxa".

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
├── music_commands.json         #novo arquivo p/ músicas
├── config.json         
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

E também um arquivo local para as músicas, `music_commands.json`, para armazenar os artistas e as músicas, com seus respectivos links.

Crie um arquivo `music_commands.json` na raiz do projeto com o seguinte formato:

```json
[
    {
        "nomes": ["Nome do artista", "Outra possibilidade do nome"],
        "musicas": {
            "palavra_para_reconhecer ou nome_da_musica": {
                "spotify": "link da música no spotify",
                "youtube": "link da música no youtube"
            }
        }
    }
]
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

Após configurar o `config.json`, `music_commands.json` e instalar as dependências, execute o assistente com o seguinte comando:

```bash
python main.py
```