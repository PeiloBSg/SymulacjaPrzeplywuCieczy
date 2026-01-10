import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter

# Importy Twoich klas
from zbiornik import Zbiornik
from rura import Rura
from pompa import Pompa
from grzalka import Grzalka
from statystyki_ui import OknoStatystyk

class SymulacjaProcesu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Symulacja Procesu - Układ Wyrównany")
        self.setFixedSize(1100, 750)
        self.setStyleSheet("background-color: #1e1e1e; color: white; font-family: Segoe UI;")

        # === UKŁAD GEOMETRYCZNY ===
        X_AXIS_LEFT = 140   # Oś dla Z1, P1, Z2
        X_AXIS_RIGHT = 760  # Oś dla Z3, P2
        
        Y_Z2 = 50
        Y_Z3 = 50
        Y_P1 = 300
        Y_P2 = 290
        Y_SPLIT = 340
        Y_Z4_Z5 = 380
        Y_BOTTOM_RAIL = 660

        # === 1. ZBIORNIKI ===
        self.z1 = Zbiornik(X_AXIS_LEFT - 90, 500, 180, 120, "Z1: Bufor", pojemnosc=300.0)
        self.z1.aktualna_ilosc = 200.0
        self.z1.aktualizuj_poziom()

        self.z2 = Zbiornik(X_AXIS_LEFT - 90, Y_Z2, 180, 120, "Z2: Dozownik")
        self.z3 = Zbiornik(X_AXIS_RIGHT - 110, Y_Z3, 220, 200, "Z3: Reaktor", pojemnosc=400.0)
        
        OFFSET_CHLODNIC = 150
        self.z4 = Zbiornik(X_AXIS_RIGHT - OFFSET_CHLODNIC - 60, Y_Z4_Z5, 120, 120, "Z4: Chłodnica 1")
        self.z5 = Zbiornik(X_AXIS_RIGHT + OFFSET_CHLODNIC - 60, Y_Z4_Z5, 120, 120, "Z5: Chłodnica 2")

        self.zbiorniki = [self.z1, self.z2, self.z3, self.z4, self.z5]

        # === INICJALIZACJA OKNA STATYSTYK ===
        self.okno_statystyk = OknoStatystyk(self)

        # === 2. URZĄDZENIA ===
        self.p1 = Pompa(X_AXIS_LEFT, Y_P1) 
        self.p2 = Pompa(X_AXIS_RIGHT, Y_P2)
        # Grzałka pod Z3
        self.grzalka = Grzalka(X_AXIS_RIGHT - 60, Y_Z3 + 150, 120, 30)

        # === 3. RURY ===
        # Rura 1: Z1 -> P1 -> Z2
        pts_r1 = [self.z1.punkt_gora(), (X_AXIS_LEFT, Y_P1), self.z2.punkt_dol()]
        self.rura1 = Rura(pts_r1)

        # Rura 2: Z2 -> Z3
        y_rura2 = Y_Z2 + 60
        pts_r2 = [(self.z2.x + self.z2.width, y_rura2), (self.z3.x, y_rura2)]
        self.rura2 = Rura(pts_r2)

        # Rura 3: Z3 -> P2
        pts_r3 = [self.z3.punkt_dol(), (X_AXIS_RIGHT, Y_P2)]
        self.rura3 = Rura(pts_r3)

        # Rura 4: P2 -> Rozgałęzienie
        pts_r4 = [(X_AXIS_RIGHT, Y_P2), (X_AXIS_RIGHT, Y_SPLIT)]
        self.rura4 = Rura(pts_r4)

        # Rura 5a i 5b: Rozgałęzienie -> Z4 / Z5
        x_z4_center = self.z4.x + self.z4.width / 2
        pts_r5a = [(X_AXIS_RIGHT, Y_SPLIT), (x_z4_center, Y_SPLIT), (x_z4_center, Y_Z4_Z5)]
        self.rura5a = Rura(pts_r5a)

        x_z5_center = self.z5.x + self.z5.width / 2
        pts_r5b = [(X_AXIS_RIGHT, Y_SPLIT), (x_z5_center, Y_SPLIT), (x_z5_center, Y_Z4_Z5)]
        self.rura5b = Rura(pts_r5b)

        # Rura 6: Z4 -> Powrót
        y_out = Y_Z4_Z5 + 120
        pts_r6 = [(x_z4_center, y_out), (x_z4_center, Y_BOTTOM_RAIL), 
                  (X_AXIS_LEFT, Y_BOTTOM_RAIL), (X_AXIS_LEFT, 500 + 120)]
        self.rura6 = Rura(pts_r6)

        # Rura 7: Z5 -> Powrót
        pts_r7 = [(x_z5_center, y_out), (x_z5_center, Y_BOTTOM_RAIL), (x_z4_center, Y_BOTTOM_RAIL)]
        self.rura7 = Rura(pts_r7)

        self.rury = [self.rura1, self.rura2, self.rura3, self.rura4, self.rura5a, self.rura5b, self.rura6, self.rura7]

        # === LOGIKA ===
        self.timer = QTimer()
        self.timer.timeout.connect(self.cykl_automatyki)
        self.running = False
        self.init_ui()

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

    # --- OBSŁUGA KLAWISZY (ESC) ---
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.toggle_statystyki()
        else:
            super().keyPressEvent(event)

    # --- OBSŁUGA MYSZY (Włączniki) ---
    def mousePressEvent(self, event):
        # Sprawdzamy, czy kliknięto w włącznik P1, P2 lub Grzałki
        zmiana1 = self.p1.sprawdz_klikniecie(event.x(), event.y())
        zmiana2 = self.p2.sprawdz_klikniecie(event.x(), event.y())
        zmiana3 = self.grzalka.sprawdz_klikniecie(event.x(), event.y())
        
        if zmiana1 or zmiana2 or zmiana3:
            self.update() # Odświeżamy widok (kolor włącznika)
        
        super().mousePressEvent(event)

    def toggle_process(self):
        self.running = not self.running
        if self.running:
            self.timer.start(30)
            self.btn_start.setStyleSheet("background-color: #388E3C; border: 2px solid #1B5E20;")
            self.lbl_status.setText("STAN: PRACA AUTOMATYCZNA")
        else:
            self.timer.stop()
            self.p1.wylacz()
            self.p2.wylacz()
            self.grzalka.ustaw_stan(False)
            for r in self.rury: r.ustaw_przeplyw(False)
            self.btn_start.setStyleSheet("background-color: #d32f2f; border: 2px solid #b71c1c;")
            self.lbl_status.setText("STAN: ZATRZYMANY")
            self.update()

    def cykl_automatyki(self):
        tempo = 0.8
        
        # 1. Z1 -> Z2
        if not self.z1.czy_pusty() and not self.z2.czy_pelny():
            self.p1.wlacz() 
            if self.p1.is_running:
                ilosc = self.z1.usun_ciecz(tempo)
                self.z2.dodaj_ciecz(ilosc)
                self.rura1.ustaw_przeplyw(True)
            else:
                self.rura1.ustaw_przeplyw(False)
        else:
            self.p1.wylacz()
            self.rura1.ustaw_przeplyw(False)

        # 2. Z2 -> Z3
        if self.z2.poziom > 0.05 and not self.z3.czy_pelny():
            ilosc = self.z2.usun_ciecz(tempo * 0.8)
            self.z3.dodaj_ciecz(ilosc)
            self.rura2.ustaw_przeplyw(True)
        else:
            self.rura2.ustaw_przeplyw(False)

        # 3. Reaktor Z3 (GRZAŁKA)
        if self.z3.aktualna_ilosc > 10:
            # Automatyka chce włączyć grzałkę
            self.grzalka.ustaw_stan(True) 
            # Ale czy faktycznie się włączyła? (Sprawdzamy is_active, które uwzględnia przycisk)
            if self.grzalka.is_active:
                self.z3.ogrzej(0.4)
            else:
                self.z3.schlodz(0.1) # Grzałka odłączona prądem, więc stygnie
        else:
            self.grzalka.ustaw_stan(False)
            self.z3.schlodz(0.1)

        # 4. Z3 -> P2 -> Z4/Z5
        gotowy_do_spustu = (self.z3.temperatura > 55.0 or self.z3.poziom > 0.85)
        miejsce_w_chlodnicach = (not self.z4.czy_pelny() or not self.z5.czy_pelny())

        if gotowy_do_spustu and miejsce_w_chlodnicach and self.z3.aktualna_ilosc > 0:
            self.p2.wlacz()
            if self.p2.is_running:
                ilosc = self.z3.usun_ciecz(tempo * 2.0)
                polowa = ilosc / 2.0
                r5a = False
                r5b = False

                if not self.z4.czy_pelny():
                    self.z4.dodaj_ciecz(polowa)
                    r5a = True
                else:
                    self.z5.dodaj_ciecz(polowa)

                if not self.z5.czy_pelny():
                    self.z5.dodaj_ciecz(polowa)
                    r5b = True
                else:
                    self.z4.dodaj_ciecz(polowa)

                self.rura3.ustaw_przeplyw(True)
                self.rura4.ustaw_przeplyw(True)
                self.rura5a.ustaw_przeplyw(r5a)
                self.rura5b.ustaw_przeplyw(r5b)
            else:
                self.rura3.ustaw_przeplyw(False)
                self.rura4.ustaw_przeplyw(False)
                self.rura5a.ustaw_przeplyw(False)
                self.rura5b.ustaw_przeplyw(False)
        else:
            self.p2.wylacz()
            self.rura3.ustaw_przeplyw(False)
            self.rura4.ustaw_przeplyw(False)
            self.rura5a.ustaw_przeplyw(False)
            self.rura5b.ustaw_przeplyw(False)

        # 5. Powrót
        # Z4
        if self.z4.poziom > 0.05:
            self.z4.schlodz(0.6)
            ilosc = self.z4.usun_ciecz(tempo * 0.6)
            self.z1.dodaj_ciecz(ilosc)
            self.rura6.ustaw_przeplyw(True)
        else:
            self.rura6.ustaw_przeplyw(False)

        # Z5
        if self.z5.poziom > 0.05:
            self.z5.schlodz(0.6)
            ilosc = self.z5.usun_ciecz(tempo * 0.6)
            self.z1.dodaj_ciecz(ilosc)
            self.rura7.ustaw_przeplyw(True)
            self.rura6.ustaw_przeplyw(True)
        else:
            self.rura7.ustaw_przeplyw(False)

        # Naturalne chłodzenie
        self.z1.schlodz(0.02)
        self.z2.schlodz(0.02)

        # AKTUALIZACJA STATYSTYK
        if self.okno_statystyk.isVisible():
            self.okno_statystyk.aktualizuj_dane(self.zbiorniki)

        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        for r in self.rury: r.draw(p)
        for z in self.zbiorniki: z.draw(p)
        self.grzalka.draw(p)
        self.p1.draw(p)
        self.p2.draw(p)