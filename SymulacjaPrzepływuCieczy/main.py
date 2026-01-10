import sys
from PyQt5.QtWidgets import QApplication

# Importujemy naszą główną klasę okna z pliku symulacja_ui.py
from symulacja_ui import SymulacjaProcesu

def main():
    # Tworzenie instancji aplikacji
    app = QApplication(sys.argv)
    
    # Tworzenie i wyświetlanie głównego okna
    okno = SymulacjaProcesu()
    okno.show()
    
    # Uruchomienie pętli zdarzeń
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()