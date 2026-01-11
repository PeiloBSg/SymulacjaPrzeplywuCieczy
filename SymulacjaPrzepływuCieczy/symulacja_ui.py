import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter

# Importujemy nasze moduły
from uklad import Uklad
from sterownik import Sterownik
from statystyki_ui import OknoStatystyk

class SymulacjaProcesu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Symulacja Procesu - MVC Pattern")
        self.setFixedSize(1100, 750)
        self.setStyleSheet("background-color: #1e1e1e; color: white; font-family: Segoe UI;")

        # 1. MODEL: Tworzymy fizyczny układ
        self.uklad = Uklad()

        # 2. KONTROLER: Tworzymy sterownik i dajemy mu dostęp do układu
        self.sterownik = Sterownik(self.uklad)

        # 3. WIDOK: UI i okna pomocnicze
        self.okno_statystyk = OknoStatystyk(self)
        self.init_ui()

        # Timer (Serce pętli)
        self.timer = QTimer()
        self.timer.timeout.connect(self.obsluga_timera)
        self.running = False

    def init_ui(self):
        # Przycisk START
        self.btn_start = QPushButton("START / STOP", self)
        self.btn_start.setGeometry(380, 690, 150, 40)
        self.btn_start.setStyleSheet("""
            QPushButton { background-color: #d32f2f; border: 2px solid #b71c1c; border-radius: 4px; color: white; font-weight: bold; }
            QPushButton:hover { background-color: #f44336; }
        """)
        self.btn_start.clicked.connect(self.toggle_process)

        self.lbl_status = QLabel("STAN: OCZEKIWANIE", self)
        self.lbl_status.setGeometry(550, 690, 300, 40)
        self.lbl_status.setStyleSheet("font-size: 14px; color: #aaa;")

        # Przycisk STATYSTYKI
        self.btn_stats = QPushButton("Statystyki (ESC)", self)
        self.btn_stats.setGeometry(950, 10, 130, 40)
        self.btn_stats.setStyleSheet("""
            QPushButton { background-color: #555; color: white; border: 1px solid #777; border-radius: 4px; font-weight: bold; }
            QPushButton:hover { background-color: #777; }
        """)
        self.btn_stats.clicked.connect(self.toggle_statystyki)

    def toggle_statystyki(self):
        if self.okno_statystyk.isVisible():
            self.okno_statystyk.hide()
        else:
            self.okno_statystyk.show()
            self.okno_statystyk.raise_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.toggle_statystyki()
        else:
            super().keyPressEvent(event)

    def mousePressEvent(self, event):
        # Interakcja myszy z obiektami (Włączniki)
        # Odwołujemy się do układu, bo tam są obiekty
        zmiana1 = self.uklad.p1.sprawdz_klikniecie(event.x(), event.y())
        zmiana2 = self.uklad.p2.sprawdz_klikniecie(event.x(), event.y())
        zmiana3 = self.uklad.grzalka.sprawdz_klikniecie(event.x(), event.y())
        
        if zmiana1 or zmiana2 or zmiana3:
            self.update() 
        super().mousePressEvent(event)

    def toggle_process(self):
        self.running = not self.running
        if self.running:
            self.timer.start(30)
            self.btn_start.setStyleSheet("background-color: #388E3C; border: 2px solid #1B5E20;")
            self.lbl_status.setText("STAN: PRACA AUTOMATYCZNA")
        else:
            self.timer.stop()
            
            # Bezpieczne zatrzymanie wszystkiego
            self.uklad.p1.wylacz()
            self.uklad.p2.wylacz()
            self.uklad.grzalka.ustaw_stan(False)
            for r in self.uklad.lista_rur: r.ustaw_przeplyw(False)
            
            self.btn_start.setStyleSheet("background-color: #d32f2f; border: 2px solid #b71c1c;")
            self.lbl_status.setText("STAN: ZATRZYMANY")
            self.update()

    def obsluga_timera(self):
        """
        To jest główna pętla aplikacji wywoływana przez timer.
        """
        # 1. Zleć sterownikowi wykonanie obliczeń
        self.sterownik.wykonaj_cykl()

        # 2. Zaktualizuj okno statystyk (jeśli widoczne)
        if self.okno_statystyk.isVisible():
            self.okno_statystyk.aktualizuj_dane(self.uklad.lista_zbiornikow)

        # 3. Odśwież grafikę (wywołuje paintEvent)
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        
        # Rysowanie - pobieramy obiekty z self.uklad
        for r in self.uklad.lista_rur: r.draw(p)
        for z in self.uklad.lista_zbiornikow: z.draw(p)
        
        self.uklad.grzalka.draw(p)
        self.uklad.p1.draw(p)
        self.uklad.p2.draw(p)