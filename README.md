## Autor
- Paweł Rogula
- Politechnika Gdańska
- Nr indeksu: 203988 
- Projekt: Symulacja Przepływu Cieczy

## Opis
Aplikacja symulująca działanie zautomatyzowanej instalacji przemysłowej, zbudowana w języku Python z użyciem biblioteki PyQt5. Projekt odwzorowuje procesy fizyczne takie jak przepływ cieczy, mieszanie temperatur, bezwładność cieplna oraz działanie elementów wykonawczych (pompy, grzałki).

## Instrukcja Pobrania
Wszystkie pliki znajdują się w folderze SymulacjaPrzepływuCieczy

## Wymagania

### Wymagania systemowe:
- Interpreter Python 3.x
- Biblioteka PyQt5
### Konfiguracja projektu (Instalacja):
Aby uruchomić projekt, należy przygotować środowisko Python:
#### 1. Instalacja bibliotek:
W terminalu / wierszu poleceń wpisz:
- `pip install PyQt5`
#### 2. Uruchomienie aplikacji:
Będąc w folderze projektu, uruchom plik startowy:
- `python main.py`

## Sterowanie
- **Start / Stop symulacji**: Przycisk w interfejsie "START / STOP"
- **Statystyki**: Przycisk "Statystyki" lub klawisz ESC
- **Symulacja awarii**: Kliknięcie LPM na Pompę (P1, P2) lub Grzałkę (odcina zasilanie)
- **Wyjście**: Zamknięcie okna

## Funkcjonalności
- Pełna wizualizacja procesu (poziomy cieczy, animacje wirników, przepływy w rurach)
- Fizyka mieszania cieczy o różnych temperaturach (średnia ważona)
- Wizualizacja temperatury poprzez zmianę koloru cieczy (gradient niebieski-czerwony)
- System symulacji awarii sprzętowych (interaktywne elementy)
- Osobne okno ze szczegółowymi statystykami liczbowymi

## Struktura projektu
- `main.py` - main
- `symulacja_ui.py` - główna klasa programu
- `sterownik.py` - logika automatyki (Kontroler)
- `uklad.py` - definicja i inicjalizacja obiektów fizycznych (Model)
- `obsluga_ui.py` - manager interfejsu i obsługi zdarzeń wejściowych
- `zbiornik.py` - logika zbiornika (fizyka cieczy i temperatury)
- `pompa.py` - logika i rysowanie pompy
- `grzalka.py` - logika i rysowanie grzałki
- `rura.py` - rysowanie rur i wizualizacja przepływu
- `statystyki_ui.py` - okno wyświetlające parametry (litry/stopnie)