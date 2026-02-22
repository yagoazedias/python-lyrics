# 🎓 Para a Galerinha que veio através das minhas Redes💜
## 🐍 Python: Player de Letras Sincronizado (Console)

Olá! Eu sou estudante de Python e criei este projeto como uma forma de colocar em prática meus estudos e juntar com duas coisas que eu amo, que é a música e a programação. Espero poder ajudar a tirar algumas dúvidas e contribuir com outros estudantes que nem eu 💜

Este repositório contém o código base de um **Player de Letras (Lyrics Player)**. Ele permite exibir poemas, letras de músicas, cenas de filmes, declarações ou qualquer texto escrito no terminal do VS Code, com o texto destacando-se no momento exato (o famoso "karaokê de terminal"!).

---

## 🏗️ Estrutura do Projeto

O projeto segue a estrutura padrão de projetos Python profissionais:

```
.
├── src/                          # Código-fonte
│   ├── __init__.py
│   └── loaders/                  # Pacote de carregadores
│       ├── __init__.py
│       └── spotify_lyrics.py     # SpotifyLyricsLoader
│
├── tests/                        # Testes automatizados
│   ├── conftest.py              # Fixtures do pytest
│   └── test_spotify_lyrics.py   # 46 testes abrangentes
│
├── base.py                       # Aplicação principal
└── samples/                      # Dados de exemplo
    └── oproprio/
        └── desligado.json        # Arquivo de exemplo com metadados
```

### 🎵 SpotifyLyricsLoader

Uma classe robusta para carregar e converter letras da API do Spotify:

```python
from src.loaders import SpotifyLyricsLoader

# Carregar letras
loader = SpotifyLyricsLoader("caminho/para/arquivo.json")
if loader.load():
    lyrics = loader.get_lyrics_data()
    info = loader.get_content_info()
    duration = loader.get_total_duration()
```

**Recursos:**
- ✅ Suporta formato com título e artista
- ✅ Compatível com formato legado (array simples)
- ✅ Conversão automática de milissegundos para segundos
- ✅ Filtragem de entradas vazias
- ✅ Tratamento robusto de erros

### 📄 Formato de Arquivo JSON

O arquivo JSON inclui metadados estruturados:

```json
{
  "title": "Nome da Música",
  "artist": "Nome do Artista",
  "lyrics": [
    {
      "startTimeMs": "7430",
      "words": "Primeira linha da letra"
    },
    {
      "startTimeMs": "12010",
      "words": "Segunda linha da letra"
    }
  ]
}
```

O título e artista são carregados **automaticamente** do arquivo.

### 💻 Argumentos de Linha de Comando

Execute a aplicação com diferentes arquivos de letras:

```bash
# Usar arquivo padrão
python3 base.py

# Especificar arquivo
python3 base.py --arquivo samples/oproprio/desligado.json

# Forma abreviada
python3 base.py -f samples/oproprio/desligado.json

# Ver ajuda
python3 base.py --help
```

### 🧪 Testes Automatizados

O projeto inclui **46 testes abrangentes**:

```bash
# Executar todos os testes
python3 -m pytest tests/ -v

# Testes de carregamento
python3 -m pytest tests/test_spotify_lyrics.py::TestSpotifyLyricsLoaderLoading -v

# Ver cobertura
python3 -m pytest tests/ --cov=src/
```

**Cobertura de testes:**
- ✅ Carregamento de arquivos
- ✅ Conversão de dados
- ✅ Tratamento de erros
- ✅ Múltiplos formatos de arquivo
- ✅ Casos extremos (edge cases)
- ✅ Integração completa

---

## 🛠️ Como Usar e Estudar (Guia Rápido)

O projeto é excelente para praticar **Sincronização de Tempo** e **Controle do Terminal** com comandos ANSI.

### 📝 1. Adaptando o Conteúdo

#### Opção A: Usando um arquivo JSON (Recomendado)

Crie um arquivo JSON com a estrutura:

```json
{
  "title": "Minha Música",
  "artist": "Meu Artista",
  "lyrics": [
    {"startTimeMs": "0", "words": "Primeira linha"},
    {"startTimeMs": "5000", "words": "Segunda linha"}
  ]
}
```

Depois execute:

```bash
python3 base.py --arquivo caminho/para/seu_arquivo.json
```

#### Opção B: Editar dados diretamente (Para aprendizado)

Para colocar seu próprio texto (música ou poema), concentre-se na **Seção 5 (`DADOS DO CONTEÚDO`)** do código:

* **`"time"`:** Defina o *timestamp* exato (em segundos) em que a linha deve ser renderizada.
* **`"original"`:** Insira o seu texto. Use o `\n` para forçar quebras de linha manuais e ver a função `split_and_wrap_text` em ação!
* **`TOTAL_MUSIC_DURATION`:** Ajuste este valor para o tempo total de execução.

### ✨ 2. Dicas de Customização e Solução de Problemas

* **Customização Rápida:** Para testar temas e cores diferentes, edite as variáveis de cor na **Seção 2 (`CONFIGURAÇÃO DE ESTILO`)**. Experimente!
* **Sincronia Fina:** Se o ritmo não bater com a leitura, ajuste os valores decimais (`0.1s`, `0.2s`) dos *timestamps* em `LYRICS_DATA`.
* **Problemas com Cor:** Se o código ANSI não funcionar, verifique se seu terminal (ou ambiente de execução) tem suporte completo (o VS Code Terminal geralmente funciona perfeitamente).
* **Múltiplos Arquivos:** Use `--arquivo` para testar diferentes arquivos de letras sem modificar o código.

---

## 📋 Requisitos

- Python 3.x
- Terminal com suporte a ANSI (VS Code, Linux, Mac, Windows Terminal)
- pytest (para rodar testes): `pip install pytest`

## 🚀 Instalação Rápida

```bash
# Clone ou baixe o repositório
git clone https://github.com/seu-usuario/C-DIGO-BASE-PARA-A-LYRICS-.git
cd C-DIGO-BASE-PARA-A-LYRICS-

# Instale as dependências de teste (opcional)
pip install pytest

# Execute a aplicação
python3 base.py

# Ou execute com seu próprio arquivo
python3 base.py -f samples/sua_musica.json

# Execute os testes
python3 -m pytest tests/ -v
```

Bons estudos! 🐍💜
