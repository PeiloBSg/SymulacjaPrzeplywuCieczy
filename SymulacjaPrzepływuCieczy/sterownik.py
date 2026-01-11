class Sterownik:
    def __init__(self, uklad_fizyczny):
        # Sterownik musi mieć dostęp do sprzętu (pomp, zaworów, zbiorników)
        self.uklad = uklad_fizyczny
        self.tempo = 0.8  # Szybkość symulacji

    def wykonaj_cykl(self):
        """
        Ta metoda wykonuje jeden krok logiki automatyki.
        Jest wywoływana przez Timer z głównego okna.
        """
        u = self.uklad # Alias dla wygody, żeby nie pisać self.uklad.z1...
        
        # 1. Z1 -> Z2 (Transfer)
        if not u.z1.czy_pusty() and not u.z2.czy_pelny():
            u.p1.wlacz() 
            # Sprawdzenie fizyczne pompy (czy włącznik jest ON)
            if u.p1.is_running:
                ilosc = u.z1.usun_ciecz(self.tempo)
                u.z2.dodaj_ciecz(ilosc)
                u.rura1.ustaw_przeplyw(True)
            else:
                u.rura1.ustaw_przeplyw(False)
        else:
            u.p1.wylacz()
            u.rura1.ustaw_przeplyw(False)

        # 2. Z2 -> Z3 (Dozowanie)
        if u.z2.poziom > 0.05 and not u.z3.czy_pelny():
            ilosc = u.z2.usun_ciecz(self.tempo * 0.8)
            u.z3.dodaj_ciecz(ilosc)
            u.rura2.ustaw_przeplyw(True)
        else:
            u.rura2.ustaw_przeplyw(False)

        # 3. Reaktor Z3 (Grzanie / Reakcja)
        if u.z3.aktualna_ilosc > 10:
            u.grzalka.ustaw_stan(True) 
            # Sprawdzenie fizyczne grzałki (bezpiecznik)
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
                ilosc = u.z3.usun_ciecz(self.tempo * 2.0)
                polowa = ilosc / 2.0
                r5a = False
                r5b = False

                # Rozdział na dwie chłodnice
                if not u.z4.czy_pelny():
                    u.z4.dodaj_ciecz(polowa)
                    r5a = True
                else:
                    u.z5.dodaj_ciecz(polowa)

                if not u.z5.czy_pelny():
                    u.z5.dodaj_ciecz(polowa)
                    r5b = True
                else:
                    u.z4.dodaj_ciecz(polowa)

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

        # 5. Powrót Z4/Z5 -> Z1
        # Z4
        if u.z4.poziom > 0.05:
            u.z4.schlodz(0.6)
            ilosc = u.z4.usun_ciecz(self.tempo * 0.6)
            u.z1.dodaj_ciecz(ilosc)
            u.rura6.ustaw_przeplyw(True)
        else:
            u.rura6.ustaw_przeplyw(False)

        # Z5
        if u.z5.poziom > 0.05:
            u.z5.schlodz(0.6)
            ilosc = u.z5.usun_ciecz(self.tempo * 0.6)
            u.z1.dodaj_ciecz(ilosc)
            u.rura7.ustaw_przeplyw(True)
            u.rura6.ustaw_przeplyw(True) # Wspólny kolektor
        else:
            u.rura7.ustaw_przeplyw(False)

        # Fizyka otoczenia (naturalne chłodzenie)
        u.z1.schlodz(0.02)
        u.z2.schlodz(0.02)