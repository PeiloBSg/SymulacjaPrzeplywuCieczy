from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtCore import Qt

class ObslugaUI:
    def __init__(self, okno_glowne):

        self.okno = okno_glowne

    def init_ui(self):
        # Przycisk START
        self.okno.btn_start = QPushButton("START / STOP", self.okno)
        self.okno.btn_start.setGeometry(380, 690, 150, 40)
        self.okno.btn_start.setStyleSheet("""
            QPushButton { background-color: #d32f2f; border: 2px solid #b71c1c; border-radius: 4px; color: white; font-weight: bold; }
            QPushButton:hover { background-color: #f44336; }
        """)
        # Podpinamy pod metodę w oknie głównym (bo tam jest timer)
        self.okno.btn_start.clicked.connect(self.okno.toggle_process)

        self.okno.lbl_status = QLabel("STAN: OCZEKIWANIE", self.okno)
        self.okno.lbl_status.setGeometry(550, 690, 300, 40)
        self.okno.lbl_status.setStyleSheet("font-size: 14px; color: #aaa;")

        # Przycisk STATYSTYKI
        self.okno.btn_stats = QPushButton("Statystyki (ESC)", self.okno)
        self.okno.btn_stats.setGeometry(950, 10, 130, 40)
        self.okno.btn_stats.setStyleSheet("""
            QPushButton { background-color: #555; color: white; border: 1px solid #777; border-radius: 4px; font-weight: bold; }
            QPushButton:hover { background-color: #777; }
        """)
        # Podpinamy pod lokalną metodę w tej klasie
        self.okno.btn_stats.clicked.connect(self.toggle_statystyki)

    def toggle_statystyki(self):
        """Otwiera lub ukrywa okno statystyk."""
        if self.okno.okno_statystyk.isVisible():
            self.okno.okno_statystyk.hide()
        else:
            self.okno.okno_statystyk.show()
            self.okno.okno_statystyk.raise_()

    def keyPressEvent(self, event):
        """Obsługa klawisza ESC."""
        if event.key() == Qt.Key_Escape:
            self.toggle_statystyki()

    def mousePressEvent(self, event):
        
        uklad = self.okno.uklad
        
        zmiana1 = uklad.p1.sprawdz_klikniecie(event.x(), event.y())
        zmiana2 = uklad.p2.sprawdz_klikniecie(event.x(), event.y())
        zmiana3 = uklad.grzalka.sprawdz_klikniecie(event.x(), event.y())
        
        # Jeśli stan któregokolwiek obiektu się zmienił, odświeżamy główne okno
        if zmiana1 or zmiana2 or zmiana3:
            self.okno.update()