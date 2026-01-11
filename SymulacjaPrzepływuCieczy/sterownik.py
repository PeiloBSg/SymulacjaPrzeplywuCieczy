class Sterownik:
    def __init__(self, uklad_fizyczny):
        self.uklad = uklad_fizyczny
        self.tempo = 0.8

    def wykonaj_cykl(self):
        u = self.uklad
        
        # 1. Z1 -> Z2 (Transfer)
        if not u.z1.czy_pusty() and not u.z2.czy_pelny():
            u.p1.wlacz() 
            if u.p1.is_running:
                temp_zrodla = u.z1.temperatura
                ilosc = u.z1.usun_ciecz(self.tempo)
                u.z2.dodaj_ciecz(ilosc, temp_zrodla)
                u.rura1.ustaw_przeplyw(True)
            else:
                u.rura1.ustaw_przeplyw(False)
        else:
            u.p1.wylacz()
            u.rura1.ustaw_przeplyw(False)

        # 2. Z2 -> Z3 (Dozowanie)
        if u.z2.poziom > 0.05 and not u.z3.czy_pelny():
            temp_zrodla = u.z2.temperatura
            ilosc = u.z2.usun_ciecz(self.tempo * 0.8)
            u.z3.dodaj_ciecz(ilosc, temp_zrodla)
            u.rura2.ustaw_przeplyw(True)
        else:
            u.rura2.ustaw_przeplyw(False)

        # 3. Reaktor Z3 (Grzanie / Reakcja)
        if u.z3.aktualna_ilosc > 10:
            u.grzalka.ustaw_stan(True) 
            if u.grzalka.is_active:
                u.z3.ogrzej(0.4)
            else:
                u.z3.schlodz(0.1)
        else:
            u.grzalka.ustaw_stan(False)
            u.z3.schlodz(0.1)

        # 4. Z3 -> P2 -> Z4/Z5 (Spust do chłodnic)
        gotowy_do_spustu = (u.z3.temperatura > 55.0 or u.z3.poziom > 0.85)
        miejsce_w_chlodnicach = (not u.z4.czy_pelny() or not u.z5.czy_pelny())

        if gotowy_do_spustu and miejsce_w_chlodnicach and u.z3.aktualna_ilosc > 0:
            u.p2.wlacz()
            if u.p2.is_running:
                temp_goraca = u.z3.temperatura
                ilosc = u.z3.usun_ciecz(self.tempo * 2.0)
                polowa = ilosc / 2.0
                r5a = False
                r5b = False

                if not u.z4.czy_pelny():
                    u.z4.dodaj_ciecz(polowa, temp_goraca)
                    r5a = True
                else:
                    u.z5.dodaj_ciecz(polowa, temp_goraca)

                if not u.z5.czy_pelny():
                    u.z5.dodaj_ciecz(polowa, temp_goraca)
                    r5b = True
                else:
                    u.z4.dodaj_ciecz(polowa, temp_goraca)

                u.rura3.ustaw_przeplyw(True)
                u.rura4.ustaw_przeplyw(True)
                u.rura5a.ustaw_przeplyw(r5a)
                u.rura5b.ustaw_przeplyw(r5b)
            else:
                u.rura3.ustaw_przeplyw(False)
                u.rura4.ustaw_przeplyw(False)
                u.rura5a.ustaw_przeplyw(False)
                u.rura5b.ustaw_przeplyw(False)
        else:
            u.p2.wylacz()
            u.rura3.ustaw_przeplyw(False)
            u.rura4.ustaw_przeplyw(False)
            u.rura5a.ustaw_przeplyw(False)
            u.rura5b.ustaw_przeplyw(False)

        # 5. Powrót Z4/Z5 -> Z1 (Recyrkulacja)
        self._obsluz_powrot(u.z4, u.rura6)
        self._obsluz_powrot(u.z5, u.rura7, u.rura6)

        # Fizyka otoczenia
        u.z1.schlodz(0.02)
        u.z2.schlodz(0.02)

    def _obsluz_powrot(self, zbiornik, rura_powrotna, rura_kolektor=None):
        """Metoda pomocnicza obsługująca powrót cieczy (DRY principle)."""
        if zbiornik.poziom > 0.05 and zbiornik.temperatura < 30.0:
            zbiornik.schlodz(0.6)
            temp = zbiornik.temperatura
            ilosc = zbiornik.usun_ciecz(self.tempo * 0.6)
            self.uklad.z1.dodaj_ciecz(ilosc, temp)
            
            rura_powrotna.ustaw_przeplyw(True)
            if rura_kolektor:
                rura_kolektor.ustaw_przeplyw(True)
        else:
            zbiornik.schlodz(0.6)
            rura_powrotna.ustaw_przeplyw(False)

    def zatrzymaj_wszystko(self):
        u = self.uklad
        u.p1.wylacz()
        u.p2.wylacz()
        u.grzalka.ustaw_stan(False)
        for r in u.lista_rur:
            r.ustaw_przeplyw(False)