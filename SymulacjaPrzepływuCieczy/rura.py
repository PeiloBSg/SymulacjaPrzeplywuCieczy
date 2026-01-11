from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath

class Rura:
    def __init__(self, punkty, grubosc=8):
        self.punkty = [QPointF(float(p[0]), float(p[1])) for p in punkty]
        self.grubosc = grubosc
        self.kolor_rury = QColor(100, 100, 100)
        self.kolor_cieczy = QColor(0, 180, 255)
        self.czy_plynie = False

    def ustaw_przeplyw(self, plynie: bool):
        self.czy_plynie = plynie

    def draw(self, painter: QPainter):
        if len(self.punkty) < 2:
            return

        path = QPainterPath()
        path.moveTo(self.punkty[0])
        for p in self.punkty[1:]:
            path.lineTo(p)

        # 1. Zewnętrzna obudowa rury (ciemniejsza, szersza)
        painter.setPen(QPen(self.kolor_rury, self.grubosc + 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)

        # 2. Wnętrze rury (tło dla cieczy - ciemne)
        painter.setPen(QPen(QColor(30, 30, 30), self.grubosc - 2, Qt.SolidLine))
        painter.drawPath(path)

        # 3. Ciecz (jeśli płynie)
        if self.czy_plynie:
            painter.setPen(QPen(self.kolor_cieczy, self.grubosc - 4, Qt.SolidLine))
            painter.drawPath(path)