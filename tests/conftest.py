"""
Pytest configuration and shared fixtures for SpotifyLyricsLoader tests.
"""

import pytest
import json
import tempfile
from pathlib import Path


@pytest.fixture
def valid_spotify_lyrics_data():
    """Fixture que fornece uma estrutura válida de dados de letras do Spotify."""
    return [
        {
            "startTimeMs": "7430",
            "words": "Uh, acordei desligado",
            "syllables": [],
            "endTimeMs": "0",
            "transliteratedWords": ""
        },
        {
            "startTimeMs": "12010",
            "words": "Sonhei que tava acordado",
            "syllables": [],
            "endTimeMs": "0",
            "transliteratedWords": ""
        },
        {
            "startTimeMs": "15240",
            "words": "Só queria você aqui do meu lado",
            "syllables": [],
            "endTimeMs": "0",
            "transliteratedWords": ""
        },
        {
            "startTimeMs": "106750",
            "words": "",  # Entrada vazia - deve ser filtrada
            "syllables": [],
            "endTimeMs": "0",
            "transliteratedWords": ""
        }
    ]


@pytest.fixture
def temp_json_file(valid_spotify_lyrics_data):
    """Fixture que cria um arquivo JSON temporário com dados válidos de letras."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(valid_spotify_lyrics_data, f)
        temp_path = f.name
    yield temp_path
    # Limpeza
    Path(temp_path).unlink()


@pytest.fixture
def temp_invalid_json_file():
    """Fixture que cria um arquivo temporário com JSON inválido."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("{invalid json content}")
        temp_path = f.name
    yield temp_path
    Path(temp_path).unlink()


@pytest.fixture
def temp_empty_json_file():
    """Fixture que cria um arquivo temporário com um array JSON vazio."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump([], f)
        temp_path = f.name
    yield temp_path
    Path(temp_path).unlink()


@pytest.fixture
def temp_whitespace_only_json_file():
    """Fixture que cria um arquivo temporário com letras apenas com espaços em branco."""
    data = [
        {
            "startTimeMs": "100",
            "words": "   ",  # Apenas espaço em branco
            "syllables": [],
            "endTimeMs": "0",
            "transliteratedWords": ""
        }
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
        temp_path = f.name
    yield temp_path
    Path(temp_path).unlink()


@pytest.fixture
def temp_zero_milliseconds_json_file():
    """Fixture que cria um arquivo temporário com milissegundos zero."""
    data = [
        {
            "startTimeMs": "0",
            "words": "First word at start",
            "syllables": [],
            "endTimeMs": "0",
            "transliteratedWords": ""
        }
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
        temp_path = f.name
    yield temp_path
    Path(temp_path).unlink()


@pytest.fixture
def temp_large_milliseconds_json_file():
    """Fixture que cria um arquivo temporário com valores de milissegundos grandes (1 hora)."""
    data = [
        {
            "startTimeMs": "3600000",  # 1 hora
            "words": "Song at one hour",
            "syllables": [],
            "endTimeMs": "0",
            "transliteratedWords": ""
        }
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
        temp_path = f.name
    yield temp_path
    Path(temp_path).unlink()


@pytest.fixture
def temp_minimal_entry_json_file():
    """Fixture que cria um arquivo temporário com entrada mínima (campos opcionais ausentes)."""
    data = [
        {
            "startTimeMs": "1000",
            "words": "Minimal entry"
            # Faltam syllables, endTimeMs, transliteratedWords
        }
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
        temp_path = f.name
    yield temp_path
    Path(temp_path).unlink()


@pytest.fixture
def temp_special_characters_json_file():
    """Fixture que cria um arquivo temporário com caracteres especiais em letras."""
    data = [
        {
            "startTimeMs": "1000",
            "words": "Açúcar, café & pão!",
            "syllables": [],
            "endTimeMs": "0",
            "transliteratedWords": ""
        }
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
        temp_path = f.name
    yield temp_path
    Path(temp_path).unlink()


@pytest.fixture
def new_format_spotify_lyrics_data():
    """Fixture que fornece dados no novo formato com título, artista e letras."""
    return {
        "title": "Desligado",
        "artist": "Yago Oproprio, Jean Tassy, Zero",
        "lyrics": [
            {
                "startTimeMs": "7430",
                "words": "Uh, acordei desligado",
                "syllables": [],
                "endTimeMs": "0",
                "transliteratedWords": ""
            },
            {
                "startTimeMs": "12010",
                "words": "Sonhei que tava acordado",
                "syllables": [],
                "endTimeMs": "0",
                "transliteratedWords": ""
            },
            {
                "startTimeMs": "15240",
                "words": "Só queria você aqui do meu lado",
                "syllables": [],
                "endTimeMs": "0",
                "transliteratedWords": ""
            },
            {
                "startTimeMs": "106750",
                "words": "",  # Entrada vazia - deve ser filtrada
                "syllables": [],
                "endTimeMs": "0",
                "transliteratedWords": ""
            }
        ]
    }


@pytest.fixture
def temp_new_format_json_file(new_format_spotify_lyrics_data):
    """Fixture que cria um arquivo JSON temporário no novo formato."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(new_format_spotify_lyrics_data, f, ensure_ascii=False)
        temp_path = f.name
    yield temp_path
    # Limpeza
    Path(temp_path).unlink()
