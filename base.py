import time             # Importa o módulo time para funções relacionadas a tempo (sincronização).
import sys              # Importa o módulo sys para interagir com o sistema, especialmente a saída (stdout).
import os               # Importa o módulo os para interagir com o sistema operacional (tamanho do terminal).
import threading        # Importa o módulo threading para gerenciar a concorrência (screen_lock).
import random           # Importa o módulo random (mantido do original, mas não usado neste modelo).

# --- CONSTANTES ANSI (Cores e Comandos para o Terminal) ---
RESET = "\033[0m"       # Código ANSI para resetar toda a formatação (cor, negrito).
BOLD = "\033[1m"        # Código ANSI para ativar o estilo negrito/destaque.
DIM = "\033[2m"         # Código ANSI para ativar o estilo de cor tênue (dim).

# ----------------------------------------------------------------------------------
# --- CORES PERSONALIZADAS (Modelo Base) ---
# ----------------------------------------------------------------------------------
HIGHLIGHT_COLOR = ""    # String vazia: usa a cor padrão do terminal para o destaque.
MAIN_COLOR = ""         # String vazia: usa a cor padrão do terminal para texto ativo sem destaque especial.

# Cinza Escuro Suave: Código ANSI para uma cor cinza específica (cor inativa).
INACTIVE_LYRIC_COLOR = "\033[38;5;239m" 

INFO_COLOR = ""         # String vazia: usa a cor padrão do terminal para Título/Artista.

# --- FUNÇÕES ANSI (Essenciais para o posicionamento) ---
# Função lambda para gerar o código ANSI que posiciona o cursor em uma linha (row) e coluna (col).
CURSOR_POS = lambda row, col: f"\033[{row};{col}H"
CLEAR_SCREEN = "\033[H\033[J" # Código ANSI para limpar a tela e mover o cursor para o canto (1;1).
HIDE_CURSOR = "\033[?25l"     # Código ANSI para esconder o cursor.
SHOW_CURSOR = "\033[?25h"     # Código ANSI para mostrar o cursor (restauração).

# --- VARIÁVEIS GLOBAIS DE LAYOUT ---
TEXT_WIDTH = 60         # Define a largura máxima que o texto das letras pode ocupar.
TEXT_HEIGHT = 15        # Define a altura máxima da área de exibição das letras.
terminal_width = 80     # Variável global para armazenar a largura detectada do terminal (padrão 80).
terminal_height = 24    # Variável global para armazenar a altura detectada do terminal (padrão 24).

# Objeto Lock para controlar o acesso à saída do terminal em ambientes multithread.
screen_lock = threading.Lock()

# --- FUNÇÃO PARA PEGAR O TAMANHO DO TERMINAL ---
def update_terminal_size():
    """Função para tentar obter o tamanho atual do terminal."""
    global terminal_width, terminal_height # Declara as variáveis globais que serão modificadas.
    try:
        # Tenta obter o tamanho do terminal usando os.get_terminal_size().
        current_term_width, current_term_height = os.get_terminal_size()
        # Define a largura mínima de 80 e atualiza terminal_width.
        terminal_width = max(80, current_term_width)
        # Define a altura mínima de 20 e atualiza terminal_height.
        terminal_height = max(20, current_term_height)
    except OSError:
        pass # Ignora o erro e mantém os valores padrão se falhar.

# --- FUNÇÃO PARA AJUSTAR O TEXTO À LARGURA ---
def split_and_wrap_text(text, max_width):
    """Função que processa o texto para aplicar a quebra de linha ('wrap')."""
    
    parts_by_newline = text.split('\n') # Divide o texto em partes, respeitando quebras de linha existentes.
    wrapped_lines = []                  # Lista para armazenar as linhas finais formatadas.

    for part in parts_by_newline:       # Itera sobre cada parte separada por '\n'.
        words = part.split()            # Divide a parte em palavras.
        current_line = []               # Lista para construir a linha atual.
        current_line_length = 0         # Contador do comprimento da linha atual.
        
        for word in words:              # Itera sobre cada palavra.
            # Verifica se a palavra cabe na largura máxima.
            if current_line_length + len(word) + (1 if current_line else 0) <= max_width:
                current_line.append(word) # Adiciona a palavra à linha.
                # Atualiza o comprimento da linha, incluindo o espaço.
                current_line_length += len(word) + (1 if current_line else 0)
            else:
                # Se não couber, adiciona a linha completa à lista de linhas finais.
                wrapped_lines.append(" ".join(current_line))
                current_line = [word]     # Começa uma nova linha com a palavra.
                current_line_length = len(word) # Define o comprimento da nova linha.
        
        if current_line:                # Após o loop, se a linha atual não estiver vazia, a adiciona.
            wrapped_lines.append(" ".join(current_line))
    
    return wrapped_lines                # Retorna a lista de linhas ajustadas.

# --- FUNÇÃO PRINCIPAL: Display de TODO o Conteúdo ---
def display_content(current_line_index, lyrics_data, content_info):
    """Função que desenha todo o conteúdo na tela, focando na linha ativa."""
    
    start_col = 2                       # Coluna inicial de renderização (margem esquerda).
    start_row = 1                       # Linha inicial de renderização (topo).
    LYRIC_WRAP_WIDTH = TEXT_WIDTH       # Usa a largura definida para quebrar as letras.
    current_display_row = 0             # Contador de linhas já exibidas na tela.

    with screen_lock:                   # Entra na seção crítica, garantindo acesso exclusivo ao stdout.
        sys.stdout.write(CLEAR_SCREEN)  # Limpa a tela antes de redesenhar.

        # 1. RENDERIZA TÍTULO E ARTISTA
        for title_part_line in content_info["title_lines"]: # Itera sobre as linhas do título.
            title_wrapped = split_and_wrap_text(title_part_line, LYRIC_WRAP_WIDTH) # Quebra de linha no título.
            for line in title_wrapped:                      # Itera sobre as partes do título.
                if current_display_row < TEXT_HEIGHT:       # Verifica se há espaço vertical.
                    # Posiciona o cursor para escrever o título.
                    sys.stdout.write(CURSOR_POS(start_row + current_display_row, start_col))
                    # Escreve o título em Negrito e cor INFO_COLOR.
                    sys.stdout.write(f"{BOLD}{INFO_COLOR}{line}{RESET}") 
                    current_display_row += 1                # Incrementa o contador de linhas exibidas.

        for info_part_line in content_info["artist_lines"]: # Repete o processo para o nome do artista.
            info_wrapped = split_and_wrap_text(info_part_line, LYRIC_WRAP_WIDTH)
            for line in info_wrapped:
                if current_display_row < TEXT_HEIGHT:
                    sys.stdout.write(CURSOR_POS(start_row + current_display_row, start_col))
                    sys.stdout.write(f"{BOLD}{INFO_COLOR}{line}{RESET}") 
                    current_display_row += 1

        if current_display_row < TEXT_HEIGHT:
            current_display_row += 1                        # Adiciona uma linha em branco após o Título/Artista.
    
        # 2. LÓGICA DE EXIBIÇÃO DAS LETRAS
        start_lyric_index = current_line_index              # O índice inicial é a linha ativa (estilo Spotify).
        lines_to_show = TEXT_HEIGHT - current_display_row   # Calcula quantas linhas de letra ainda cabem na tela.
        end_lyric_index = start_lyric_index + lines_to_show # Índice da última linha de letra a ser exibida.

        for i in range(start_lyric_index, end_lyric_index): # Itera apenas sobre as letras visíveis.
            if i >= 0 and i < len(lyrics_data):             # Verifica se o índice é válido.
                line_data = lyrics_data[i]                  # Pega os dados da linha (tempo, texto, highlight).
                line_text_to_wrap = line_data["original"]   # Pega o texto original.
                
                active_highlight_color = HIGHLIGHT_COLOR    # Define a cor de destaque (vazia).
                wrapped_lines = split_and_wrap_text(line_text_to_wrap, LYRIC_WRAP_WIDTH) # Quebra de linha na letra.
                
                is_highlighted = line_data.get("highlight", False) # Verifica se a linha tem o marcador "highlight".
                
                for line_part in wrapped_lines:             # Itera sobre as partes da linha (se houver quebra de linha).
                    # Define a cor/estilo:
                    if i == current_line_index:             # Se for a linha ATIVA:
                        # Usa BOLD e a cor de destaque se houver 'highlight' ou se for a primeira linha (time 0.0).
                        color = BOLD + (active_highlight_color if is_highlighted or line_data.get("time", -1) == 0.0 else MAIN_COLOR)
                    else:
                        # Se for linha INATIVA: usa a cor Cinza Escuro Suave.
                        color = INACTIVE_LYRIC_COLOR
                    
                    display_line = f"{color}{line_part}{RESET}" # Formata a linha com cores e reset.
                    
                    if current_display_row < TEXT_HEIGHT:   # Verifica o limite da tela.
                        row_to_render = start_row + current_display_row
                        
                        sys.stdout.write(CURSOR_POS(row_to_render, start_col)) # Posiciona o cursor.
                        sys.stdout.write(display_line)      # Escreve a linha no terminal.
                    current_display_row += 1                # Incrementa o contador de linhas.
            else:
                current_display_row += 1                    # Se o índice for inválido (após o fim das letras), incrementa a linha de exibição.
                
        sys.stdout.flush()                                  # Força a escrita de todo o buffer de saída.

# --- FUNÇÃO PARA LIMPAR TELA E CURSOR ---
def cleanup_screen():
    """Função essencial para restaurar o estado padrão do terminal ao sair."""
    with screen_lock:                       # Protege a saída do terminal.
        sys.stdout.write(CLEAR_SCREEN)      # Limpa a tela.
        sys.stdout.write(SHOW_CURSOR)       # Torna o cursor visível.
        sys.stdout.flush()                  # Garante a execução dos comandos.

# ----------------------------------------------------------------------------------
# --- DADOS DO CONTEÚDO (MODELO BASE) ---
# ----------------------------------------------------------------------------------
CONTENT_INFO = {
    "title_lines": [
        "Nome da Música ou Título do Poema" # Linha do título/nome da obra.
    ],
    "artist_lines": [
        "Nome do Artista ou Autor"          # Linha do artista/autor.
    ]
}

# ##########################################################################
# # LETRAS E TEMPOS (MODELO BASE)
# ##########################################################################
LYRICS_DATA = [
    # Dicionário com tempo (segundos) e texto ("original").
    {"time": 0.0, "original": "Esta é a primeira frase de exemplo do modelo."},
    {"time": 4.5, "original": "O ritmo da animação é definido por estes tempos."},
    {"time": 9.0, "original": "Adicione aqui as demais frases e seus respectivos tempos."},
    # Exemplo de linha com destaque específico.
    {"time": 15.0, "original": "Linhas com 'highlight': True podem ter uma cor diferente.", "highlight": True},
    {"time": 20.0, "original": "Fim do trecho de exemplo."}
]
# ##########################################################################

TOTAL_MUSIC_DURATION = 25.0 # Define a duração total para o loop de animação.

# --- FUNÇÃO PRINCIPAL PARA A ANIMAÇÃO ---
def start_lyrics_animation():
    """Gerencia o ciclo de tempo e a lógica de avanço das letras."""
    sys.stdout.write(HIDE_CURSOR)           # Esconde o cursor no início.
    sys.stdout.write(CLEAR_SCREEN)          # Limpa a tela no início.
    sys.stdout.flush()

    update_terminal_size()                  # Obtém o tamanho atual do terminal.
    
    start_time = time.monotonic()           # Registra o tempo inicial (referência zero).
    current_line_index = 0                  # Inicializa o índice da próxima linha a ser carregada.
    
    # Loop principal: continua enquanto não atingir a duração total.
    while time.monotonic() - start_time < TOTAL_MUSIC_DURATION:
        elapsed_time = time.monotonic() - start_time # Calcula o tempo decorrido desde o início.
        
        # Avança o índice da linha sempre que o tempo decorrido ultrapassa o tempo da próxima linha.
        while current_line_index < len(LYRICS_DATA) and elapsed_time >= LYRICS_DATA[current_line_index]["time"]:
            current_line_index += 1
            
        try:
            # O índice da linha ATIVA (a que está sendo exibida) é o anterior.
            display_index_for_display = current_line_index - 1
            
            # Condição para garantir que a primeira linha seja exibida imediatamente se time=0.0.
            if display_index_for_display < 0 and LYRICS_DATA and LYRICS_DATA[0]["time"] == 0.0:
                display_index_for_display = 0
            
            # Pula o loop de exibição se ainda não chegou ao tempo da primeira linha.
            if display_index_for_display < 0:
                continue

            # Proteção contra ultrapassar o limite final da lista.
            if display_index_for_display >= len(LYRICS_DATA):
                display_index_for_display = len(LYRICS_DATA) - 1
                
            # Chama a função de exibição para desenhar na tela.
            display_content(display_index_for_display, LYRICS_DATA, CONTENT_INFO)
            
        except OSError:
            break # Sai do loop em caso de erro de saída.
            
        # --- Cálculo do Tempo de Espera (Sleep) ---
        next_target_time = TOTAL_MUSIC_DURATION
        # Se houver mais linhas, usa o tempo da próxima linha como alvo.
        if current_line_index < len(LYRICS_DATA):
            next_target_time = LYRICS_DATA[current_line_index]["time"]
            
        # Calcula o tempo exato para esperar (tempo alvo - tempo decorrido).
        time_to_sleep = next_target_time - (time.monotonic() - start_time) 
        # Garante um mínimo de 10ms de espera e evita valores negativos.
        time_to_sleep = max(0.01, time_to_sleep) 
        time.sleep(time_to_sleep) # Pausa a execução.

    # Mensagem Final
    with screen_lock:                       # Protege a saída para a mensagem final.
        update_terminal_size()
        sys.stdout.write(CLEAR_SCREEN)      # Limpa a tela para a mensagem final.
        final_message = "FIM DA MÚSICA 🎶 (Modelo Base)"
        
        color_code = BOLD + INFO_COLOR
        
        # Lógica de centralização da mensagem.
        final_message_col = (terminal_width - len(final_message) - len(color_code) - len(RESET)) // 2
        final_message_row = terminal_height // 2
        
        # Escreve a mensagem final centralizada.
        sys.stdout.write(f"{CURSOR_POS(final_message_row, final_message_col)}{color_code}{final_message}{RESET}\n")
        
        artist_title = f"{CONTENT_INFO['artist_lines'][0]} - {CONTENT_INFO['title_lines'][0]}"
        # Escreve o título/artista centralizado abaixo.
        sys.stdout.write(f"{CURSOR_POS(final_message_row + 1, (terminal_width - len(artist_title) - len(INFO_COLOR) - len(RESET)) // 2)}{BOLD}{INFO_COLOR}{artist_title}{RESET}\n")
        
        sys.stdout.flush()
    time.sleep(3) # Espera 3 segundos antes de continuar.

if __name__ == "__main__":
    try:
        start_lyrics_animation() # Inicia a função principal de animação.
        with screen_lock:
            sys.stdout.write(CLEAR_SCREEN)
            update_terminal_size()
            message = "Programa finalizado. Pressione Enter para sair."
            # Exibe a mensagem de finalização antes de pedir o input.
            sys.stdout.write(CURSOR_POS(terminal_height // 2 - 1, (terminal_width - len(message)) // 2))
            sys.stdout.write(message + "\n")
            sys.stdout.flush()
        input() # Aguarda o usuário pressionar Enter para fechar (muito importante).
    except KeyboardInterrupt:
        print("\nExibição interrompida pelo usuário.")
    except Exception as e:
        print(f"\nOcorreu um erro: {e}")
    finally:
        cleanup_screen() # GARANTE que o terminal seja restaurado (executa sempre).