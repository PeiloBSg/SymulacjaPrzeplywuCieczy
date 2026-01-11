import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter

# Importujemy nasze moduły
from uklad import Uklad
from sterownik import Sterownik
from statystyki_ui import OknoStatystyk
from obsluga_ui import ObslugaUI

class SymulacjaProcesu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Symulacja Procesu - MVC Pattern")
        self.setFixedSize(1100, 750)
        self.setStyleSheet("background-color: #1e1e1e; color: white; font-family: Segoe UI;")

        # 1. MODEL
        self.uklad = Uklad()

        # 2. KONTROLER
        self.sterownik = Sterownik(self.uklad)

        # 3. WIDOK
        self.okno_statystyk = OknoStatystyk(self)

        # 4. UI MANAGER (Tworzenie i wygląd)
        self.ui_manager = ObslugaUI(self)
        self.ui_manager.init_ui()

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.obsluga_timera)
        self.running = False

    # Przekazywanie zdarzeń do managera UI
    def keyPressEvent(self, event):
        self.ui_manager.keyPressEvent(event)
        super().keyPressEvent(event)

    def mousePressEvent(self, event):
        self.ui_manager.mousePressEvent(event)
        super().mousePressEvent(event)

    def toggle_process(self):
        self.running = not self.running
        if self.running:
            self.timer.start(30)
            self.ui_manager.ustaw_wyglad_aktywny()
        else:
            # Logika (zatrzymanie fizyki)
            self.timer.stop()
            self.uklad.p1.wylacz()
            self.uklad.p2.wylacz()
            self.uklad.grzalka.ustaw_stan(False)
            for r in self.uklad.lista_rur: r.ustaw_przeplyw(False)
            
            self.ui_manager.ustaw_wyglad_nieaktywny()
            self.update()

    def obsluga_timera(self):
        self.sterownik.wykonaj_cykl()
        if self.okno_statystyk.isVisible():
            self.okno_statystyk.aktualizuj_dane(self.uklad.lista_zbiornikow)
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        
        for r in self.uklad.lista_rur: r.draw(p)
        for z in self.uklad.lista_zbiornikow: z.draw(p)
        for u in self.uklad.lista_urzadzen: u.draw(p)