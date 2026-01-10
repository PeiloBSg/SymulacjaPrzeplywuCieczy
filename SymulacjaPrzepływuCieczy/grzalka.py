from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush

class Grzalka:
    def __init__(self, x, y, width=40, height=20):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.is_active = False # Stan faktyczny (czy grzeje)
        
        # --- NOWOŚĆ: Logika włącznika ---
        self.prad_wlaczony = True # Stan włącznika (czy jest zasilanie)
        
        # Przycisk umieszczamy np. w prawym górnym rogu obszaru grzałki (lub tuż nad nią)
        # x + w - 20 (prawa strona), y - 25 (trochę wyżej)
        self.rect_wlacznik = QRectF(self.x + self.w - 20, self.y - 25, 20, 20)

    def ustaw_stan(self, stan: bool):
        """
        Automatyka próbuje włączyć (stan=True) lub wyłączyć (stan=False).
        Ale jeśli włącznik (prad_wlaczony) jest na False, to grzałka i tak nie ruszy.
        """
        if self.prad_wlaczony:
            self.is_active = stan
        else:
            self.is_active = False

    def sprawdz_klikniecie(self, myszka_x, myszka_y):
        """
        Sprawdza, czy kliknięto przycisk zasilania grzałki.
        Zwraca True, jeśli zmieniono stan (wymaga odświeżenia ekranu).
        """
        if self.rect_wlacznik.contains(myszka_x, myszka_y):
            self.prad_wlaczony = not self.prad_wlaczony
            # Jeśli odcinamy prąd, natychmiast przestaje grzać
            if not self.prad_wlaczony:
                self.is_active = False
            return True
        return False

    def draw(self, painter: QPainter):
        # Grzałka jako spirala/zygzak wewnątrz prostokąta
        kolor = QColor(255, 50, 0) if self.is_active else QColor(80, 80, 80)
        
        painter.setPen(QPen(kolor, 3))
        painter.setBrush(Qt.NoBrush)
        
        # Prosta reprezentacja graficzna (zygzak)
        step = self.w / 4
        y_mid = self.y + self.h / 2
        
        path_pts = [
            (self.x, y_mid),
            (self.x + step, y_mid - 10),
            (self.x + 2*step, y_mid + 10),
            (self.x + 3*step, y_mid - 10),
            (self.x + 4*step, y_mid)
        ]
        
        for i in range(len(path_pts)-1):
            p1 = path_pts[i]
            p2 = path_pts[i+1]
            painter.drawLine(int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1]))

        # Napis ON/OFF
        painter.setPen(Qt.white)
        state_txt = "ON" if self.is_active else "OFF"
        painter.drawText(int(self.x), int(self.y - 5), f"GRZAŁKA: {state_txt}")

        # --- NOWOŚĆ: Rysowanie przycisku zasilania ---
        kolor_wlacznika = QColor(0, 200, 0) if self.prad_wlaczony else QColor(200, 0, 0)
        
        painter.setPen(QPen(Qt.white, 1))
        painter.setBrush(QBrush(kolor_wlacznika))
        painter.drawRect(self.rect_wlacznik)
        
        # Symbol na przycisku
        painter.setPen(Qt.black)
        painter.drawText(self.rect_wlacznik, Qt.AlignCenter, "G")