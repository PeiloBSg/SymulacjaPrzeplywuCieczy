from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QColor, QPen, QLinearGradient

class Zbiornik:
    def __init__(self, x, y, width=100, height=140, nazwa="", pojemnosc=100.0):
        self.x = float(x)
        self.y = float(y)
        self.width = float(width)
        self.height = float(height)
        self.nazwa = nazwa

        self.pojemnosc = pojemnosc
        self.aktualna_ilosc = 0.0
        self.poziom = 0.0
        self.temperatura = 20.0

    def dodaj_ciecz(self, ilosc: float, temp_dolewana: float = 20.0) -> float:

        wolne = self.pojemnosc - self.aktualna_ilosc
        dodano = min(ilosc, wolne)

        # Logika mieszania temperatur (średnia ważona)
        if dodano > 0.0001:
            masa_obecna = self.aktualna_ilosc
            masa_dodana = dodano
            
            energia_obecna = masa_obecna * self.temperatura
            energia_dodana = masa_dodana * temp_dolewana
            
            calkowita_masa = masa_obecna + masa_dodana
            
            # Nowa temperatura to całkowita energia podzielona przez całkowitą masę
            if calkowita_masa > 0:
                self.temperatura = (energia_obecna + energia_dodana) / calkowita_masa

            self.aktualna_ilosc += dodano
            self.aktualizuj_poziom()
            
        return dodano

    def usun_ciecz(self, ilosc: float) -> float:
        usunieto = min(ilosc, self.aktualna_ilosc)
        self.aktualna_ilosc -= usunieto
        self.aktualizuj_poziom()
        
        # Jeśli zbiornik jest pusty, resetujemy temperaturę do otoczenia (opcjonalne)
        if self.aktualna_ilosc <= 0.1:
            self.temperatura = 20.0
            
        return usunieto

    def aktualizuj_poziom(self):
        self.poziom = self.aktualna_ilosc / self.pojemnosc

    def czy_pusty(self) -> bool:
        return self.aktualna_ilosc <= 0.1

    def czy_pelny(self) -> bool:
        return self.aktualna_ilosc >= self.pojemnosc - 0.1

    # --- Punkty zaczepienia (Geometryczne środki boków) ---
    def punkt_gora(self): return (self.x + self.width / 2, self.y)
    def punkt_dol(self): return (self.x + self.width / 2, self.y + self.height)
    def punkt_lewo(self): return (self.x, self.y + self.height / 2)
    def punkt_prawo(self): return (self.x + self.width, self.y + self.height / 2)
    
    def punkt_gora_lewo(self): return (self.x + 20, self.y)
    def punkt_gora_prawo(self): return (self.x + self.width - 20, self.y)

    def ogrzej(self, moc: float):
        if self.aktualna_ilosc > 0: self.temperatura = min(100.0, self.temperatura + moc)
            
    def schlodz(self, moc: float):
        # Chłodzenie nie może spaść poniżej temperatury otoczenia (np. 20 st)
        self.temperatura = max(20.0, self.temperatura - moc)

    def get_kolor_cieczy(self):
        # Od Niebieskiego (zimna) do Czerwonego (gorąca)
        # Zakładamy zakres wizualizacji 20C - 100C
        ratio = (self.temperatura - 20) / 80.0
        ratio = max(0.0, min(1.0, ratio))
        r = int(0 + ratio * 255)
        g = int(140 - ratio * 100)
        b = int(255 - ratio * 200)
        return QColor(r, g, b)

    def draw(self, painter: QPainter):
        # 1. Rysowanie obudowy (tło)
        rect = QRectF(self.x, self.y, self.width, self.height)
        painter.setPen(QPen(QColor(200, 200, 200), 2))
        painter.setBrush(QColor(40, 40, 45)) # Ciemnoszare tło
        painter.drawRoundedRect(rect, 8, 8)

        # 2. Rysowanie cieczy z gradientem
        if self.poziom > 0.01:
            h_cieczy = self.height * self.poziom
            y_start = self.y + self.height - h_cieczy
            # Lekki margines wewnątrz (2px)
            rect_liquid = QRectF(self.x + 2, y_start, self.width - 4, h_cieczy - 2)
            
            base_col = self.get_kolor_cieczy()
            grad = QLinearGradient(self.x, y_start, self.x + self.width, y_start)
            grad.setColorAt(0.0, base_col.darker(150)) # Cień z lewej
            grad.setColorAt(0.5, base_col)             # Jasny środek
            grad.setColorAt(1.0, base_col.darker(150)) # Cień z prawej
            
            painter.setPen(Qt.NoPen)
            painter.setBrush(grad)
            # Dolne rogi zaokrąglone, górne proste (chyba że pełny)
            painter.drawRoundedRect(rect_liquid, 4, 4)

        # 3. Podziałka (Miarka z prawej strony)
        painter.setPen(QPen(QColor(150, 150, 150), 1))
        x_line = self.x + self.width
        for i in range(1, 10):
            y_line = self.y + self.height * (i / 10.0)
            len_line = 8 if i == 5 else 4
            painter.drawLine(int(x_line), int(y_line), int(x_line + len_line), int(y_line))

        # 4. Napisy
        painter.setPen(Qt.white)
        # Nazwa nad zbiornikiem
        painter.drawText(int(self.x), int(self.y - 8), self.nazwa)