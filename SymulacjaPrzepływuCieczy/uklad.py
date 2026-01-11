from zbiornik import Zbiornik
from rura import Rura
from pompa import Pompa
from grzalka import Grzalka

class Uklad:
    def __init__(self):
        # === STAŁE GEOMETRYCZNE ===
        self.X_AXIS_LEFT = 140
        self.X_AXIS_RIGHT = 760
        self.Y_Z2 = 50
        self.Y_Z3 = 50
        self.Y_P1 = 300
        self.Y_P2 = 290
        self.Y_SPLIT = 340
        self.Y_Z4_Z5 = 380
        self.Y_BOTTOM_RAIL = 660

        # Listy do łatwego rysowania
        self.lista_zbiornikow = []
        self.lista_rur = []
        self.lista_urzadzen = [] # Pompy, grzałki

        # Inicjalizacja komponentów
        self._utworz_zbiorniki()
        self._utworz_urzadzenia()
        self._utworz_rury()

    def _utworz_zbiorniki(self):
        # Z1: Bufor
        self.z1 = Zbiornik(self.X_AXIS_LEFT - 90, 500, 180, 120, "Z1: Bufor", pojemnosc=300.0)
        self.z1.aktualna_ilosc = 200.0
        self.z1.aktualizuj_poziom()

        # Z2: Dozownik
        self.z2 = Zbiornik(self.X_AXIS_LEFT - 90, self.Y_Z2, 180, 120, "Z2: Dozownik")

        # Z3: Reaktor
        self.z3 = Zbiornik(self.X_AXIS_RIGHT - 110, self.Y_Z3, 220, 200, "Z3: Reaktor", pojemnosc=400.0)

        # Z4 i Z5: Chłodnice
        OFFSET = 150
        self.z4 = Zbiornik(self.X_AXIS_RIGHT - OFFSET - 60, self.Y_Z4_Z5, 120, 120, "Z4: Chłodnica 1")
        self.z5 = Zbiornik(self.X_AXIS_RIGHT + OFFSET - 60, self.Y_Z4_Z5, 120, 120, "Z5: Chłodnica 2")

        # Dodajemy do listy
        self.lista_zbiornikow = [self.z1, self.z2, self.z3, self.z4, self.z5]

    def _utworz_urzadzenia(self):
        self.p1 = Pompa(self.X_AXIS_LEFT, self.Y_P1)
        self.p2 = Pompa(self.X_AXIS_RIGHT, self.Y_P2)
        self.grzalka = Grzalka(self.X_AXIS_RIGHT - 60, self.Y_Z3 + 150, 120, 30)

        # Lista pomocnicza (opcjonalnie do rysowania pętli)
        self.lista_urzadzen = [self.p1, self.p2, self.grzalka]

    def _utworz_rury(self):
        # Rura 1: Z1 -> P1 -> Z2
        pts_r1 = [self.z1.punkt_gora(), (self.X_AXIS_LEFT, self.Y_P1), self.z2.punkt_dol()]
        self.rura1 = Rura(pts_r1)

        # Rura 2: Z2 -> Z3
        y_r2 = self.Y_Z2 + 60
        pts_r2 = [(self.z2.x + self.z2.width, y_r2), (self.z3.x, y_r2)]
        self.rura2 = Rura(pts_r2)

        # Rura 3: Z3 -> P2
        pts_r3 = [self.z3.punkt_dol(), (self.X_AXIS_RIGHT, self.Y_P2)]
        self.rura3 = Rura(pts_r3)

        # Rura 4: P2 -> Rozgałęzienie
        pts_r4 = [(self.X_AXIS_RIGHT, self.Y_P2), (self.X_AXIS_RIGHT, self.Y_SPLIT)]
        self.rura4 = Rura(pts_r4)

        # Rura 5a: Rozgałęzienie -> Z4
        x_z4 = self.z4.x + self.z4.width / 2
        pts_r5a = [(self.X_AXIS_RIGHT, self.Y_SPLIT), (x_z4, self.Y_SPLIT), (x_z4, self.Y_Z4_Z5)]
        self.rura5a = Rura(pts_r5a)

        # Rura 5b: Rozgałęzienie -> Z5
        x_z5 = self.z5.x + self.z5.width / 2
        pts_r5b = [(self.X_AXIS_RIGHT, self.Y_SPLIT), (x_z5, self.Y_SPLIT), (x_z5, self.Y_Z4_Z5)]
        self.rura5b = Rura(pts_r5b)

        # Rura 6: Z4 -> Powrót
        y_out = self.Y_Z4_Z5 + 120
        pts_r6 = [(x_z4, y_out), (x_z4, self.Y_BOTTOM_RAIL), 
                  (self.X_AXIS_LEFT, self.Y_BOTTOM_RAIL), (self.X_AXIS_LEFT, 500 + 120)]
        self.rura6 = Rura(pts_r6)

        # Rura 7: Z5 -> Powrót
        pts_r7 = [(x_z5, y_out), (x_z5, self.Y_BOTTOM_RAIL), (x_z4, self.Y_BOTTOM_RAIL)]
        self.rura7 = Rura(pts_r7)

        # Lista rur
        self.lista_rur = [self.rura1, self.rura2, self.rura3, self.rura4, 
                          self.rura5a, self.rura5b, self.rura6, self.rura7]