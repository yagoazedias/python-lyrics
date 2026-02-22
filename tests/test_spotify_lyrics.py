"""
Suite de testes para o módulo SpotifyLyricsLoader.

Os testes cobrem:
- Carregamento de arquivos JSON válidos
- Tratamento de arquivos ausentes
- Tratamento de JSON inválido
- Conversão de dados (milissegundos para segundos)
- Filtragem de letras vazias
- Obtenção de dados de letras
- Recuperação de informações de conteúdo
- Cálculo de duração total
- Definição de metadados
- Casos extremos

As fixtures são definidas em conftest.py
"""

import pytest
import json
import tempfile
from pathlib import Path
from src.loaders import SpotifyLyricsLoader


class TestSpotifyLyricsLoaderInitialization:
    """Testa a inicialização do SpotifyLyricsLoader."""

    def test_init_with_file_path_only(self):
        """Test initialization with only file path."""
        loader = SpotifyLyricsLoader("test.json")
        assert loader.json_file == Path("test.json")
        assert loader.title == ""
        assert loader.artist == ""

    def test_init_with_metadata(self):
        """Test initialization with title and artist."""
        loader = SpotifyLyricsLoader(
            "test.json",
            title="Desligado",
            artist="Yago Oproprio"
        )
        assert loader.title == "Desligado"
        assert loader.artist == "Yago Oproprio"

    def test_init_data_not_loaded_yet(self):
        """Test that data is None before loading."""
        loader = SpotifyLyricsLoader("test.json")
        assert loader._lyrics_data is None
        assert loader._raw_data is None


class TestSpotifyLyricsLoaderLoading:
    """Testa a funcionalidade de carregamento."""

    def test_load_valid_json_file(self, temp_json_file):
        """Testa o carregamento de um arquivo JSON válido."""
        loader = SpotifyLyricsLoader(temp_json_file)
        assert loader.load() is True

    def test_load_missing_file(self):
        """Testa se o carregamento de um arquivo inexistente retorna False."""
        loader = SpotifyLyricsLoader("/nonexistent/path/file.json")
        assert loader.load() is False

    def test_load_invalid_json(self, temp_invalid_json_file):
        """Testa se o carregamento de JSON inválido retorna False."""
        loader = SpotifyLyricsLoader(temp_invalid_json_file)
        assert loader.load() is False

    def test_raw_data_stored_after_load(self, temp_json_file, valid_spotify_lyrics_data):
        """Testa que os dados brutos são armazenados após carregamento bem-sucedido."""
        loader = SpotifyLyricsLoader(temp_json_file)
        loader.load()
        assert loader._raw_data == valid_spotify_lyrics_data


class TestSpotifyLyricsLoaderDataConversion:
    """Testa a funcionalidade de conversão de dados."""

    def test_milliseconds_to_seconds_conversion(self, temp_json_file):
        """Testa a conversão de milissegundos (string) para segundos (float)."""
        loader = SpotifyLyricsLoader(temp_json_file)
        loader.load()
        lyrics_data = loader.get_lyrics_data()

        # 7430 ms deve ser 7.43 segundos
        assert lyrics_data[0]["time"] == 7.43
        # 12010 ms deve ser 12.01 segundos
        assert lyrics_data[1]["time"] == 12.01
        # 15240 ms deve ser 15.24 segundos
        assert lyrics_data[2]["time"] == 15.24

    def test_empty_entries_filtered(self, temp_json_file):
        """Testa que entradas com palavras vazias são filtradas."""
        loader = SpotifyLyricsLoader(temp_json_file)
        loader.load()
        lyrics_data = loader.get_lyrics_data()

        # Deve ter 3 entradas (vazia filtrada)
        assert len(lyrics_data) == 3

        # Verifisar que não há palavras vazias no resultado
        for lyric in lyrics_data:
            assert lyric["original"].strip() != ""

    def test_preserved_lyric_text(self, temp_json_file):
        """Testa que o texto da letra é preservado corretamente."""
        loader = SpotifyLyricsLoader(temp_json_file)
        loader.load()
        lyrics_data = loader.get_lyrics_data()

        assert lyrics_data[0]["original"] == "Uh, acordei desligado"
        assert lyrics_data[1]["original"] == "Sonhei que tava acordado"
        assert lyrics_data[2]["original"] == "Só queria você aqui do meu lado"

    def test_converted_data_structure(self, temp_json_file):
        """Testa que os dados convertidos têm estrutura correta."""
        loader = SpotifyLyricsLoader(temp_json_file)
        loader.load()
        lyrics_data = loader.get_lyrics_data()

        for lyric in lyrics_data:
            assert "time" in lyric
            assert "original" in lyric
            assert isinstance(lyric["time"], float)
            assert isinstance(lyric["original"], str)

    def test_convert_empty_array(self, temp_empty_json_file):
        """Testa a conversão de um array JSON vazio."""
        loader = SpotifyLyricsLoader(temp_empty_json_file)
        loader.load()
        lyrics_data = loader.get_lyrics_data()

        assert lyrics_data == []


class TestSpotifyLyricsLoaderGetLyricsData:
    """Testa o método get_lyrics_data."""

    def test_get_lyrics_data_after_load(self, temp_json_file):
        """Testa a recuperação de dados de letras após carregamento bem-sucedido."""
        loader = SpotifyLyricsLoader(temp_json_file)
        loader.load()
        lyrics_data = loader.get_lyrics_data()

        assert isinstance(lyrics_data, list)
        assert len(lyrics_data) == 3
        assert all("time" in lyric and "original" in lyric for lyric in lyrics_data)

    def test_get_lyrics_data_without_load_raises_error(self):
        """Testa que obter dados de letras antes do carregamento levanta RuntimeError."""
        loader = SpotifyLyricsLoader("test.json")

        with pytest.raises(RuntimeError, match="Dados não carregados"):
            loader.get_lyrics_data()

    def test_get_lyrics_data_returns_list(self, temp_json_file):
        """Testa que get_lyrics_data retorna uma lista."""
        loader = SpotifyLyricsLoader(temp_json_file)
        loader.load()
        lyrics_data = loader.get_lyrics_data()

        assert isinstance(lyrics_data, list)


class TestSpotifyLyricsLoaderContentInfo:
    """Testa a recuperação de informações de conteúdo."""

    def test_content_info_with_metadata(self, temp_json_file):
        """Testa a obtenção de informações de conteúdo com título e artista."""
        loader = SpotifyLyricsLoader(
            temp_json_file,
            title="Desligado",
            artist="Yago Oproprio"
        )
        loader.load()
        content_info = loader.get_content_info()

        assert content_info["title_lines"] == ["Desligado"]
        assert content_info["artist_lines"] == ["Yago Oproprio"]

    def test_content_info_without_metadata(self, temp_json_file):
        """Testa a obtenção de informações de conteúdo com valores padrão."""
        loader = SpotifyLyricsLoader(temp_json_file)
        loader.load()
        content_info = loader.get_content_info()

        assert content_info["title_lines"] == ["Música sem título"]
        assert content_info["artist_lines"] == ["Artista desconhecido"]

    def test_content_info_with_partial_metadata(self, temp_json_file):
        """Testa a obtenção de informações de conteúdo com apenas o título definido."""
        loader = SpotifyLyricsLoader(temp_json_file, title="My Song")
        loader.load()
        content_info = loader.get_content_info()

        assert content_info["title_lines"] == ["My Song"]
        assert content_info["artist_lines"] == ["Artista desconhecido"]

    def test_content_info_structure(self, temp_json_file):
        """Testa que as informações de conteúdo têm estrutura correta."""
        loader = SpotifyLyricsLoader(temp_json_file)
        loader.load()
        content_info = loader.get_content_info()

        assert isinstance(content_info, dict)
        assert "title_lines" in content_info
        assert "artist_lines" in content_info
        assert isinstance(content_info["title_lines"], list)
        assert isinstance(content_info["artist_lines"], list)


class TestSpotifyLyricsLoaderDuration:
    """Testa o cálculo de duração."""

    def test_total_duration_with_default_buffer(self, temp_json_file):
        """Testa o cálculo de duração total com buffer padrão."""
        loader = SpotifyLyricsLoader(temp_json_file)
        loader.load()
        duration = loader.get_total_duration()

        # Última letra está em 15.24 segundos, buffer padrão é 3.0 segundos
        assert duration == 15.24 + 3.0

    def test_total_duration_with_custom_buffer(self, temp_json_file):
        """Testa o cálculo de duração total com buffer personalizado."""
        loader = SpotifyLyricsLoader(temp_json_file)
        loader.load()
        duration = loader.get_total_duration(buffer_seconds=5.0)

        # Última letra está em 15.24 segundos, buffer personalizado é 5.0 segundos
        assert duration == 15.24 + 5.0

    def test_total_duration_with_zero_buffer(self, temp_json_file):
        """Testa a duração total com buffer zero."""
        loader = SpotifyLyricsLoader(temp_json_file)
        loader.load()
        duration = loader.get_total_duration(buffer_seconds=0.0)

        # Deve ser exatamente o tempo da última letra
        assert duration == 15.24

    def test_total_duration_empty_lyrics(self, temp_empty_json_file):
        """Testa a duração total quando nenhuma letra está carregada."""
        loader = SpotifyLyricsLoader(temp_empty_json_file)
        loader.load()
        duration = loader.get_total_duration()

        # Deve retornar apenas o buffer
        assert duration == 3.0

    def test_total_duration_returns_float(self, temp_json_file):
        """Testa que a duração é retornada como float."""
        loader = SpotifyLyricsLoader(temp_json_file)
        loader.load()
        duration = loader.get_total_duration()

        assert isinstance(duration, float)


class TestSpotifyLyricsLoaderSetMetadata:
    """Testa a definição de metadados."""

    def test_set_metadata_title_and_artist(self, temp_json_file):
        """Testa a definição de título e artista."""
        loader = SpotifyLyricsLoader(temp_json_file)
        loader.load()
        loader.set_metadata(title="New Title", artist="New Artist")

        assert loader.title == "New Title"
        assert loader.artist == "New Artist"

    def test_set_metadata_title_only(self, temp_json_file):
        """Testa a definição apenas do título."""
        loader = SpotifyLyricsLoader(temp_json_file, artist="Original Artist")
        loader.load()
        loader.set_metadata(title="New Title")

        assert loader.title == "New Title"
        assert loader.artist == "Original Artist"

    def test_set_metadata_artist_only(self, temp_json_file):
        """Testa a definição apenas do artista."""
        loader = SpotifyLyricsLoader(temp_json_file, title="Original Title")
        loader.load()
        loader.set_metadata(artist="New Artist")

        assert loader.title == "Original Title"
        assert loader.artist == "New Artist"

    def test_set_metadata_empty_strings(self, temp_json_file):
        """Testa que strings vazias não sobrescrevem metadados existentes."""
        loader = SpotifyLyricsLoader(
            temp_json_file,
            title="Original Title",
            artist="Original Artist"
        )
        loader.load()
        loader.set_metadata(title="", artist="")

        # Metadados originais devem ser preservados
        assert loader.title == "Original Title"
        assert loader.artist == "Original Artist"

    def test_set_metadata_updates_content_info(self, temp_json_file):
        """Testa que set_metadata atualiza as informações de conteúdo."""
        loader = SpotifyLyricsLoader(temp_json_file)
        loader.load()
        loader.set_metadata(title="Updated Title", artist="Updated Artist")

        content_info = loader.get_content_info()
        assert content_info["title_lines"] == ["Updated Title"]
        assert content_info["artist_lines"] == ["Updated Artist"]


class TestSpotifyLyricsLoaderEdgeCases:
    """Testa casos extremos e cenários especiais."""

    def test_lyric_with_whitespace_only(self, temp_whitespace_only_json_file):
        """Testa o tratamento de entradas com apenas espaços em branco."""
        loader = SpotifyLyricsLoader(temp_whitespace_only_json_file)
        loader.load()
        lyrics_data = loader.get_lyrics_data()

        # Deve ser filtrado pois é apenas espaço em branco
        assert len(lyrics_data) == 0

    def test_zero_milliseconds(self, temp_zero_milliseconds_json_file):
        """Testa o tratamento de milissegundos zero."""
        loader = SpotifyLyricsLoader(temp_zero_milliseconds_json_file)
        loader.load()
        lyrics_data = loader.get_lyrics_data()

        assert len(lyrics_data) == 1
        assert lyrics_data[0]["time"] == 0.0

    def test_large_millisecond_values(self, temp_large_milliseconds_json_file):
        """Testa o tratamento de valores de milissegundos grandes."""
        loader = SpotifyLyricsLoader(temp_large_milliseconds_json_file)
        loader.load()
        lyrics_data = loader.get_lyrics_data()

        assert lyrics_data[0]["time"] == 3600.0

    def test_missing_optional_fields(self, temp_minimal_entry_json_file):
        """Testa o tratamento de entradas com campos opcionais ausentes."""
        loader = SpotifyLyricsLoader(temp_minimal_entry_json_file)
        loader.load()
        lyrics_data = loader.get_lyrics_data()

        assert len(lyrics_data) == 1
        assert lyrics_data[0]["original"] == "Minimal entry"

    def test_consecutive_loads(self, temp_json_file):
        """Testa o carregamento do mesmo arquivo várias vezes."""
        loader = SpotifyLyricsLoader(temp_json_file)

        # Primeiro carregamento
        assert loader.load() is True
        first_data = loader.get_lyrics_data()

        # Segundo carregamento
        assert loader.load() is True
        second_data = loader.get_lyrics_data()

        # Should have same data
        assert first_data == second_data
        assert len(first_data) == 3

    def test_special_characters_in_lyrics(self, temp_special_characters_json_file):
        """Testa o tratamento de caracteres especiais em letras."""
        loader = SpotifyLyricsLoader(temp_special_characters_json_file)
        loader.load()
        lyrics_data = loader.get_lyrics_data()

        assert lyrics_data[0]["original"] == "Açúcar, café & pão!"

    def test_lyric_ordering_preserved(self, temp_json_file):
        """Testa que a ordem das letras é preservada."""
        loader = SpotifyLyricsLoader(temp_json_file)
        loader.load()
        lyrics_data = loader.get_lyrics_data()

        # Verifisar ordem cronológica
        for i in range(len(lyrics_data) - 1):
            assert lyrics_data[i]["time"] <= lyrics_data[i + 1]["time"]


class TestSpotifyLyricsLoaderNewFormat:
    """Testa o carregamento do novo formato com título e artista no arquivo."""

    def test_load_new_format_file(self, temp_new_format_json_file):
        """Testa o carregamento de um arquivo no novo formato."""
        loader = SpotifyLyricsLoader(temp_new_format_json_file)
        assert loader.load() is True

    def test_new_format_extracts_title(self, temp_new_format_json_file):
        """Testa que o título é extraído do arquivo no novo formato."""
        loader = SpotifyLyricsLoader(temp_new_format_json_file)
        loader.load()
        assert loader.title == "Desligado"

    def test_new_format_extracts_artist(self, temp_new_format_json_file):
        """Testa que o artista é extraído do arquivo no novo formato."""
        loader = SpotifyLyricsLoader(temp_new_format_json_file)
        loader.load()
        assert loader.artist == "Yago Oproprio, Jean Tassy, Zero"

    def test_new_format_content_info_from_file(self, temp_new_format_json_file):
        """Testa que as informações de conteúdo são obtidas do arquivo."""
        loader = SpotifyLyricsLoader(temp_new_format_json_file)
        loader.load()
        content_info = loader.get_content_info()

        assert content_info["title_lines"] == ["Desligado"]
        assert content_info["artist_lines"] == ["Yago Oproprio, Jean Tassy, Zero"]

    def test_new_format_override_with_constructor_params(self, temp_new_format_json_file):
        """Testa que parâmetros do construtor não sobrescrevem valores do arquivo."""
        loader = SpotifyLyricsLoader(
            temp_new_format_json_file,
            title="Título do Construtor",
            artist="Artista do Construtor"
        )
        loader.load()

        # Parâmetros passados no construtor já estão definidos, então não são sobrescritos
        assert loader.title == "Título do Construtor"
        assert loader.artist == "Artista do Construtor"

    def test_new_format_uses_file_when_no_constructor_params(self, temp_new_format_json_file):
        """Testa que valores do arquivo são usados quando construtor está vazio."""
        loader = SpotifyLyricsLoader(temp_new_format_json_file)
        loader.load()

        assert loader.title == "Desligado"
        assert loader.artist == "Yago Oproprio, Jean Tassy, Zero"

    def test_new_format_lyrics_data(self, temp_new_format_json_file):
        """Testa que os dados de letras são extraídos corretamente do novo formato."""
        loader = SpotifyLyricsLoader(temp_new_format_json_file)
        loader.load()
        lyrics_data = loader.get_lyrics_data()

        assert len(lyrics_data) == 3  # Entrada vazia filtrada
        assert lyrics_data[0]["original"] == "Uh, acordei desligado"
        assert lyrics_data[1]["original"] == "Sonhei que tava acordado"
        assert lyrics_data[2]["original"] == "Só queria você aqui do meu lado"

    def test_new_format_backward_compatibility_with_old_format(self, temp_json_file):
        """Testa que o carregador ainda funciona com o formato antigo (array)."""
        loader = SpotifyLyricsLoader(temp_json_file)
        assert loader.load() is True
        lyrics_data = loader.get_lyrics_data()
        assert len(lyrics_data) == 3


class TestSpotifyLyricsLoaderIntegration:
    """Testes de integração combinando múltiplos recursos."""

    def test_full_workflow(self, temp_json_file):
        """Testa o fluxo completo: carregamento, obtenção de dados, definição de metadados, obtenção de informações, duração."""
        loader = SpotifyLyricsLoader(temp_json_file, title="Original", artist="Original Artist")

        # Load
        assert loader.load() is True

        # Get initial data
        lyrics_data = loader.get_lyrics_data()
        assert len(lyrics_data) == 3

        # Get initial info
        content_info = loader.get_content_info()
        assert content_info["title_lines"] == ["Original"]

        # Update metadata
        loader.set_metadata(title="Updated", artist="Updated Artist")

        # Verify info updated
        content_info = loader.get_content_info()
        assert content_info["title_lines"] == ["Updated"]
        assert content_info["artist_lines"] == ["Updated Artist"]

        # Get duration
        duration = loader.get_total_duration(buffer_seconds=2.0)
        assert duration == 15.24 + 2.0

    def test_multiple_loaders_independence(self, temp_json_file):
        """Testa que múltiplas instâncias do loader são independentes."""
        loader1 = SpotifyLyricsLoader(temp_json_file, title="Loader 1", artist="Artist 1")
        loader2 = SpotifyLyricsLoader(temp_json_file, title="Loader 2", artist="Artist 2")

        loader1.load()
        loader2.load()

        info1 = loader1.get_content_info()
        info2 = loader2.get_content_info()

        assert info1["title_lines"] == ["Loader 1"]
        assert info2["title_lines"] == ["Loader 2"]
