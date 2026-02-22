"""
Módulo SpotifyLyricsLoader

Carrega e converte dados de letras da API do Spotify (color-lyrics/v2/track/)
para o formato esperado pela aplicação de animação de letras.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple


class SpotifyLyricsLoader:
    """
    Carrega e converte dados de letras coloridas da API do Spotify para o formato LYRICS_DATA.

    Suporta dois formatos de arquivo:
    1. Formato antigo: Array direto de objetos de letras
    2. Formato novo: Objeto com chaves 'title', 'artist' e 'lyrics'

    Exemplo com formato novo:
        loader = SpotifyLyricsLoader("samples/oproprio/desligado.json")
        lyrics_data = loader.get_lyrics_data()
        content_info = loader.get_content_info()  # Inclui título e artista do arquivo
        total_duration = loader.get_total_duration()

    Exemplo com formato antigo:
        loader = SpotifyLyricsLoader("samples/lyricks.json", title="Título", artist="Artista")
        lyrics_data = loader.get_lyrics_data()
        content_info = loader.get_content_info()
        total_duration = loader.get_total_duration()
    """

    def __init__(self, json_file: str, title: str = "", artist: str = ""):
        """
        Inicializa o carregador com um arquivo JSON de letras do Spotify.

        Args:
            json_file (str): Caminho para o arquivo JSON de letras da API do Spotify
            title (str): Título da música (opcional, será sobrescrito se estiver no arquivo)
            artist (str): Nome do artista (opcional, será sobrescrito se estiver no arquivo)
        """
        self.json_file = Path(json_file)
        self.title = title
        self.artist = artist
        self._lyrics_data: Optional[List[Dict]] = None
        self._raw_data: Optional[List[Dict]] = None
        self._metadata: Optional[Dict] = None

    def load(self) -> bool:
        """
        Carrega e analisa o arquivo JSON.

        Suporta dois formatos:
        1. Array de letras (formato antigo)
        2. Objeto com "title", "artist" e "lyrics" (formato novo)

        Returns:
            bool: True se carregado com sucesso, False caso contrário
        """
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Verifica se é o novo formato (objeto com title, artist, lyrics)
            if isinstance(data, dict) and 'lyrics' in data:
                self._metadata = {
                    'title': data.get('title', ''),
                    'artist': data.get('artist', '')
                }
                # Se o título ou artista não foram definidos no construtor, usa os do arquivo
                if not self.title and self._metadata['title']:
                    self.title = self._metadata['title']
                if not self.artist and self._metadata['artist']:
                    self.artist = self._metadata['artist']
                self._raw_data = data.get('lyrics', [])
            else:
                # Formato antigo (array direto)
                self._raw_data = data if isinstance(data, list) else []

            self._convert_data()
            return True
        except FileNotFoundError:
            print(f"Erro: Arquivo '{self.json_file}' não encontrado.")
            return False
        except json.JSONDecodeError:
            print(f"Erro: JSON inválido em '{self.json_file}'.")
            return False

    def _convert_data(self) -> None:
        """
        Converte dados brutos de letras do Spotify para o formato LYRICS_DATA.
        Filtra entradas vazias e converte milissegundos para segundos.
        """
        self._lyrics_data = []

        if not self._raw_data:
            return

        for item in self._raw_data:
            # Pula entradas com palavras vazias
            if not item.get('words', '').strip():
                continue

            # Converte startTimeMs de milissegundos (string) para segundos (float)
            start_time_ms = int(item.get('startTimeMs', 0))
            start_time_seconds = start_time_ms / 1000.0

            # Cria a entrada convertida no formato LYRICS_DATA
            converted_entry = {
                "time": start_time_seconds,
                "original": item.get('words', '')
            }

            self._lyrics_data.append(converted_entry)

    def get_lyrics_data(self) -> List[Dict]:
        """
        Obtém os dados convertidos de letras.

        Returns:
            List[Dict]: Lista de letras no formato LYRICS_DATA
                Exemplo: [{"time": 7.43, "original": "Uh, acordei desligado"}, ...]
        """
        if self._lyrics_data is None:
            raise RuntimeError("Dados não carregados. Chame load() primeiro.")
        return self._lyrics_data

    def get_content_info(self) -> Dict[str, List[str]]:
        """
        Obtém as informações de conteúdo no formato esperado por display_content().

        Returns:
            Dict: Informações de conteúdo com title_lines e artist_lines
        """
        return {
            "title_lines": [self.title] if self.title else ["Música sem título"],
            "artist_lines": [self.artist] if self.artist else ["Artista desconhecido"]
        }

    def get_total_duration(self, buffer_seconds: float = 3.0) -> float:
        """
        Calcula a duração total da música baseado no último tempo de letra.

        Args:
            buffer_seconds (float): Segundos extras para adicionar após a última letra

        Returns:
            float: Duração total em segundos
        """
        if not self._lyrics_data or len(self._lyrics_data) == 0:
            return buffer_seconds

        last_lyric_time = self._lyrics_data[-1]['time']
        return last_lyric_time + buffer_seconds

    def set_metadata(self, title: str = "", artist: str = "") -> None:
        """
        Define ou atualiza o título da música e o nome do artista.

        Args:
            title (str): Título da música
            artist (str): Nome do artista
        """
        if title:
            self.title = title
        if artist:
            self.artist = artist

    def print_summary(self) -> None:
        """Imprime um resumo dos dados de letras carregados."""
        if self._lyrics_data is None:
            print("Nenhum dado carregado.")
            return

        print("\n📊 Resumo dos Dados de Letras:")
        print(f"   Total de linhas: {len(self._lyrics_data)}")

        if self._lyrics_data:
            print(f"   Tempo de início: {self._lyrics_data[0]['time']}s")
            print(f"   Tempo de término: {self._lyrics_data[-1]['time']}s")
            print(f"   TOTAL_MUSIC_DURATION recomendado: {self.get_total_duration()}s")

            print(f"\n   📝 Primeiras 3 entradas:")
            for i, lyric in enumerate(self._lyrics_data[:3]):
                print(f"      {i+1}. {lyric['time']}s - {lyric['original']}")
