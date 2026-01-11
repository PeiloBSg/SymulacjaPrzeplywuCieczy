from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush

class Pompa:
    def __init__(self, x, y, r=20):
        self.x = x
        self.y = y
        self.r = r  # promien
        self.is_running = False
        self.angle = 0  # do animacji obrotu
        
        # Logika włącznika
        self.prad_wlaczony = True # Czy włącznik jest na ON (domyślnie tak)

        self.rect_wlacznik = QRectF(self.x + 8, self.y - 30, 16, 16)

    def wlacz(self):
        # Pompa włączy się TYLKO jeśli ma "zasilanie" z włącznika
        if self.prad_wlaczony:
            self.is_running = True
        else:
            self.is_running = False

    def wylacz(self):
        self.is_running = False

    def sprawdz_klikniecie(self, myszka_x, myszka_y):

        if self.rect_wlacznik.contains(myszka_x, myszka_y):
            self.prad_wlaczony = not self.prad_wlaczony
            # Jeśli wyłączamy prąd, pompa natychmiast staje
            if not self.prad_wlaczony:
                self.is_running = False
            return True
        return False

    def draw(self, painter: QPainter):
        # Obudowa pompy
        rect = QRectF(self.x - self.r, self.y - self.r, 2 * self.r, 2 * self.r)
        
        # Kolor zależny od stanu (działa / stoi)
        color = QColor(50, 255, 50) if self.is_running else QColor(100, 100, 100)
        
        painter.setPen(QPen(Qt.white, 2))
        painter.setBrush(QBrush(color))
        painter.drawEllipse(rect)
        
        # Symbol wirnika (prosta animacja)
        painter.setPen(QPen(Qt.black, 2))
        if self.is_running:
            self.angle = (self.angle + 15) % 360
        
        painter.save()
        painter.translate(self.x, self.y)
        painter.rotate(self.angle)
        painter.drawLine(-self.r + 4, 0, self.r - 4, 0)
        painter.drawLine(0, -self.r + 4, 0, self.r - 4)
        painter.restore()
        
        # Podpis
        painter.setPen(Qt.white)
        painter.drawText(int(self.x - 15), int(self.y + self.r + 15), "POMPA")

        # Rysowanie włącznika
        kolor_wlacznika = QColor(0, 200, 0) if self.prad_wlaczony else QColor(200, 0, 0)
        
        painter.setPen(QPen(Qt.white, 1))
        painter.setBrush(QBrush(kolor_wlacznika))
        painter.drawRect(self.rect_wlacznik)
        
        # Litera "S" na włączniku
        painter.setPen(Qt.black)
        painter.setFont(painter.font()) # Reset czcionki
        painter.drawText(self.rect_wlacznik, Qt.AlignCenter, "I/O")