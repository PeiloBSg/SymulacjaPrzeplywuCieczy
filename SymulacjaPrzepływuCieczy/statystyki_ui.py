from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QGroupBox, QGridLayout

class OknoStatystyk(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Statystyki Systemu")
        self.resize(350, 300)
        
        # Główny układ
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Ramka grupująca
        self.group = QGroupBox("Parametry Rzeczywiste")
        self.grid = QGridLayout()
        self.group.setLayout(self.grid)
        self.layout.addWidget(self.group)
        
        # Słownik, żeby pamiętać etykiety i nie tworzyć ich od nowa co klatkę
        self.labels = {}

    def aktualizuj_dane(self, lista_zbiornikow):
        """
        Przyjmuje listę obiektów (instancji klasy Zbiornik) i wypisuje ich stan.
        """
        row = 0
        for z in lista_zbiornikow:
            # Klucz do identyfikacji (np. nazwa zbiornika)
            klucz = z.nazwa 
            
            # Format danych w nowym oknie
            dane_tekst = f"{z.aktualna_ilosc:.0f} L  |  {z.temperatura:.1f} °C"
            
            if klucz not in self.labels:
                # Jeśli to pierwszy raz, tworzymy etykiety
                lbl_nazwa = QLabel(f"<b>{z.nazwa}</b>")
                lbl_dane = QLabel(dane_tekst)
                
                # Dodajemy do siatki: (widget, wiersz, kolumna)
                self.grid.addWidget(lbl_nazwa, row, 0)
                self.grid.addWidget(lbl_dane, row, 1)
                
                # Zapisujemy referencję do labela z danymi
                self.labels[klucz] = lbl_dane
                row += 1
            else:
                # Jeśli już istnieje, tylko aktualizujemy tekst
                self.labels[klucz].setText(dane_tekst)