import random
import time

class Gracz:
    KOLORKI = {
    "czerwony": [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36],
    "czarny": [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
}

    def __init__(self, stan_konta=1001, zadluzenie=0):
        self.stan_konta = stan_konta
        self.zadluzenie = zadluzenie
        self.reka = []
        self.stawka = 0  


    def spin_ruletka(self):
        return random.randint(1,36)


    def ruletka(self):
        while True:
            print("=========================================================================")
            print("Witaj w ruletce!")
            print("Twój stan konta: $", self.stan_konta)
            print("=========================================================================")
            print("Wybierz opcję:")
            print("1. Obstaw na liczbę (1-36)")
            print("2. Obstaw na kolor (Cze(r)wony/(C)zarny)")
            print("3. Wyjdź z gry")

            wybor_ruletka = input("Wybierz opcję: ")
            if wybor_ruletka == "1":
                self.obstaw_liczbe()
            elif wybor_ruletka == "2":
                self.obstaw_kolor()
            elif wybor_ruletka == "3":
                print("Dziękujemy za grę! Twój ostateczny stan konta: $", self.stan_konta)
                break
            else:
                print("Niepoprawny wybór, spróbuj ponownie.")


    def obstaw_liczbe(self):
        while True:
            stawka = input("Postaw na jedną liczbę (1-36): ")
            if not stawka.isdigit() or int(stawka) < 1 or int(stawka) > 36:
                print("Niepoprawna liczba! Wybierz liczbę od 1 do 36.")
                continue
            try:
                stawka_kwota = int(input("Ile chcesz postawić? "))
                if stawka_kwota <= 0:
                    print("Kwota stawki musi być większa niż zero.")
                    continue
            except ValueError:
                print("Niepoprawna kwota stawki!")
                continue

            if stawka_kwota > self.stan_konta:
                print("Nie masz wystarczającej ilości pieniędzy!")
                return

            self.stan_konta -= stawka_kwota
            wynik = self.spin_ruletka()
            print("Kulka zatrzymała się na:", wynik)
            if int(stawka) == wynik:
                wygrana = stawka_kwota * 35
                self.stan_konta += wygrana
                print("Gratulacje! Wygrałeś $", wygrana)
            else:
                print("Niestety, przegrałeś $", stawka_kwota)
            print("Twój aktualny stan konta: $", self.stan_konta)
            break


    def obstaw_kolor(self):
        while True:
            kolor = input("Wybierz kolor (Cze(r)wony/(C)zarny): ").lower()
            if kolor == 'r':
                kolor = 'czerwony'
            elif kolor == 'c':
                kolor = 'czarny'
            else:
                print("Niepoprawny kolor! Wybierz 'Cze(r)wony' lub '(C)zarny'.")
                continue
            try:
                stawka_kwota = int(input("Ile chcesz postawić? "))
                if stawka_kwota <= 0:
                    print("Kwota stawki musi być większa niż zero.")
                    continue
            except ValueError:
                print("Niepoprawna kwota stawki!")
                continue

            if stawka_kwota > self.stan_konta:
                print("Nie masz wystarczającej ilości pieniędzy!")
                return

            self.stan_konta -= stawka_kwota
            wynik = self.spin_ruletka()
            if wynik in self.KOLORKI[kolor]:
                print("Kulka zatrzymała się na:", wynik, kolor)
                wygrana = stawka_kwota * 2
                self.stan_konta += wygrana
                print("Gratulacje! Wygrałeś $", wygrana)
            else:
                print("Kulka zatrzymała się na:", wynik, "Czerwonym" if wynik in self.KOLORKI["czerwony"] else "Czarnym")
                print("Niestety, przegrałeś $", stawka_kwota)
            print("Twój aktualny stan konta: $", self.stan_konta)
            break


    def blackjack(self):
        while True:
            print("Witaj w blackjacku!")
            karty = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
            random.shuffle(karty)
            reka_gracza = []
            reka_krupiera = []

            def punkty(reka):
                suma = sum(reka)
                liczba_asow = reka.count(11)
                while suma > 21 and liczba_asow:
                    suma -= 10
                    liczba_asow -= 1
                return suma

            def pokaz_karty(reka, ukryta_karta=False, czy_krupier=False):
                if czy_krupier:
                    if ukryta_karta:
                        print("Karty krupiera:")
                        print("Karta 1: ***")
                        print("Karta 2:", reka[1])
                    else:
                        print("Karty krupiera:", reka)
                else:
                    print("Twoje karty:", reka)

            def obstaw():
                while True:
                    stawka = input("Ile chcesz obstawić? (całkowita liczba większa od 0): ")
                    if stawka.isdigit() and int(stawka) > 0:
                        stawka_kwota = int(stawka)
                        if stawka_kwota > self.stan_konta:
                            print("Nie masz wystarczającej ilości pieniędzy!")
                        else:
                            return stawka_kwota
                    else:
                        print("Niepoprawna kwota obstawienia! Podaj liczbę całkowitą większą od 0.")

            stawka_kwota = obstaw()
            self.stan_konta -= stawka_kwota

            def graj():
                for _ in range(2):
                    reka_gracza.append(karty.pop())
                    reka_krupiera.append(karty.pop())

                pokaz_karty(reka_gracza)
                pokaz_karty(reka_krupiera, ukryta_karta=True, czy_krupier=True)

                while punkty(reka_gracza) < 21:
                    wybor = input("Czy chcesz dobrać kartę? (t/n): ")
                    if wybor.lower() == 't':
                        reka_gracza.append(karty.pop())
                        pokaz_karty(reka_gracza)
                    else:
                        break

                punkty_gracza = punkty(reka_gracza)
                if punkty_gracza > 21:
                    print("Przekroczyłeś 21! Przegrywasz!")
                    return -1
                else:
                    while punkty(reka_krupiera) < 17:
                        reka_krupiera.append(karty.pop())

                    pokaz_karty(reka_krupiera, czy_krupier=True)
                    punkty_krupiera = punkty(reka_krupiera)

                    if punkty_krupiera > 21 or punkty_gracza > punkty_krupiera:
                        print("Wygrałeś!")
                        return 1
                    elif punkty_gracza < punkty_krupiera:
                        print("Przegrałeś!")
                        return -1
                    else:
                        print("Remis!")
                        return 0

            wynik = graj()
            if wynik == 1:
                self.stan_konta += 2 * stawka_kwota
            elif wynik == 0:
                self.stan_konta += stawka_kwota
            
            if not self.zapytaj_czy_zagrac_ponownie():
                break


    def zapytaj_czy_zagrac_ponownie(self):
        while True:
            decyzja = input("Czy chcesz zagrać ponownie? (t/n): ").lower()
            if decyzja == 't':
                return True
            elif decyzja == 'n':
                return False
            else:
                print("Niepoprawny wybór, wpisz 't' dla tak lub 'n' dla nie.")



    def automaty(self):
        print("=========================================================================")
        print("Witaj w automatach do gier!")
        print("Zasady gry: Aby wygrać, potrzebujesz uzyskać trzy takie same symbole.")
        print("Dostępne symbole: 🍒  🍊  🍋  🍎  🍇  🍉")
        print("=========================================================================")

        def obstaw():
            while True:
                stawka = input("Ile chcesz obstawić? (całkowita liczba większa od 0): ")
                if stawka.isdigit() and int(stawka) > 0:
                    stawka_kwota = int(stawka)
                    if stawka_kwota > self.stan_konta:
                        print("Nie masz wystarczającej ilości pieniędzy!")
                    else:
                        return stawka_kwota
                else:
                    print("Niepoprawna kwota obstawienia! Podaj liczbę całkowitą większą od 0.")

        stawka_kwota = obstaw()
        self.stan_konta -= stawka_kwota

        print("=========================================================================")
        input("Naciśnij enter, aby kręcić automatem...")
        print("=========================================================================")

        symbole = []
        for _ in range(3):
            symbole.append(random.choice(["🍒", "🍊", "🍋", "🍎", "🍇", "🍉"]))
            print("Wypadły symbole:", symbole)
            time.sleep(1)  

        if symbole[0] == symbole[1] == symbole[2]:
            wygrana = stawka_kwota * 10  
            print("Brawo! Wygrałeś! Twój wygrany stan konta wynosi $", wygrana)
            self.stan_konta += wygrana

        else:
            print("Niestety, nie udało się wygrać.")


    def kosci(self):
        print("=========================================================================")
        print("Witaj w grze w kości (Craps)!")
        print("Zasady gry: Gracz stawia zakłady na wynik rzutu dwiema kostkami.")
        print("Jeśli wyrzucisz sumę 7 lub 11 w pierwszym rzucie, wygrywasz.")
        print("Jeśli wyrzucisz sumę 2, 3 lub 12 w pierwszym rzucie, przegrywasz.")
        print("Jeśli wyrzucisz inną sumę, ta suma staje się twoim 'punktem', a teraz musisz wyrzucić tę samą sumę ponownie, zanim wyrzucisz sumę 7, aby wygrać.")
        print("=========================================================================")

        def rzut_kosci():
            return random.randint(1, 6) + random.randint(1, 6)

        def obstaw():
            while True:
                stawka = input("Ile chcesz obstawić? (całkowita liczba większa od 0): ")
                if stawka.isdigit() and int(stawka) > 0:
                    stawka_kwota = int(stawka)
                    if stawka_kwota > self.stan_konta:
                        print("Nie masz wystarczającej ilości pieniędzy!")
                    else:
                        return stawka_kwota
                else:
                    print("Niepoprawna kwota obstawienia! Podaj liczbę całkowitą większą od 0.")

        stawka_kwota = obstaw()
        self.stan_konta -= stawka_kwota

        print("Naciśnij enter, aby rzucić kością...")
        input()

        pierwszy_rzut = rzut_kosci()
        print("Pierwszy rzut:", pierwszy_rzut)

        if pierwszy_rzut in (7, 11):
            wygrana = stawka_kwota * 2 
            print("Gratulacje, wygrałeś w pierwszym rzucie! Twoja wygrana wynosi $", wygrana)
            self.stan_konta += wygrana
        elif pierwszy_rzut in (2, 3, 12):
            print("Niestety, przegrałeś w pierwszym rzucie!")
        else:
            punkt = pierwszy_rzut
            print("Twój punkt to:", punkt)
            print("Teraz spróbuj wyrzucić swoją sumę punktów ponownie, zanim wyrzucisz sumę 7.")

            while True:
                print("Naciśnij enter, aby rzucić kością...")
                input()
                kolejny_rzut = rzut_kosci()
                print("Kolejny rzut:", kolejny_rzut)
                if kolejny_rzut == punkt:
                    wygrana = stawka_kwota * 2  
                    print("Gratulacje, udało ci się wyrzucić swoją sumę punktów ponownie! Wygrywasz!")
                    print("Twoja wygrana wynosi $", wygrana)
                    self.stan_konta += wygrana
                    break
                elif kolejny_rzut == 7:
                    print("Niestety, wyrzuciłeś sumę 7, co oznacza, że przegrywasz.")
                    break


    def wyścigi_psów(self):
        print("=========================================================================")
        print("Witaj na wyścigach psów!")
        psy = [
            {"nazwa": "Azor", "szybkość": random.randint(10, 20), "pozycja": 30},
            {"nazwa": "Burek", "szybkość": random.randint(10, 20), "pozycja": 30},
            {"nazwa": "Cezar", "szybkość": random.randint(10, 20), "pozycja": 30},
            {"nazwa": "Dingo", "szybkość": random.randint(10, 20), "pozycja": 30},
            {"nazwa": "Eros", "szybkość": random.randint(10, 20), "pozycja": 30}
        ]

        psy.sort(key=lambda x: x["szybkość"], reverse=True)
        print("Dzisiaj biorą udział w wyścigu psy:")
        for i, pies in enumerate(psy):
            print(f'{i+1}. "{pies["nazwa"]}"')

        wybor_psa = int(input("Wybierz numer psa, na który chcesz postawić: "))
        if wybor_psa < 1 or wybor_psa > len(psy):
            print("Niepoprawny numer psa!")
            return

        stawka_kwota = int(input("Ile chcesz postawić? "))
        if stawka_kwota > self.stan_konta:
            print("Nie masz wystarczającej ilości pieniędzy!")
            return

        print("Zwierzakom... Gotowi... Start!")
        for i in range(5):
            time.sleep(1)
            print(f"Wyścig trwa...")

        odleglosc = 30
        while odleglosc > 0:
            time.sleep(0.5)
            for pies in psy:
                ruch = random.randint(1, 3)
                pies["pozycja"] = max(0, pies["pozycja"] - ruch)
                print(f"{pies['nazwa']}: {'-' * pies['pozycja']}>")

            psy.sort(key=lambda x: x["pozycja"])
            prowadzenie = psy[0]["nazwa"]
            print(f"Prowadzi: {prowadzenie}")
            odleglosc = min(pies["pozycja"] for pies in psy)

        print("\nPrędkości psów po wyścigu:")
        for pies in psy:
            print(f"{pies['nazwa']}: Prędkość: {pies['szybkość']} km/h")

        psy_po_kolejnosci = [pies["nazwa"] for pies in psy]
        print(f"\nKolejność dobiegnięcia do mety: ")
        for miejsce, pies in enumerate(psy_po_kolejnosci):
            print(f"Miejsce {miejsce+1}: 🐕 {pies}")

        zwyciezca = psy[0]["nazwa"]
        print(f"\nZwycięzcą jest... {zwyciezca}!")

        if psy[wybor_psa - 1]["nazwa"] == zwyciezca:
            wygrana = stawka_kwota * 5
            print(f"Gratulacje! Twój pies {zwyciezca} wygrał! Wygrywasz ${wygrana}.")
            self.stan_konta += wygrana
        else:
            print("Niestety, Twój pies nie wygrał tego wyścigu.")
            self.stan_konta -= stawka_kwota

        print(f"Aktualny stan konta: ${self.stan_konta}")


    def losowanie_liczb(self):
        return random.sample(range(1, 51), 5)


    def obstaw_stawke(self):
        while True:
            stawka = input("Podaj stawkę loterii (całkowita liczba większa od 0): ")
            if stawka.isdigit() and int(stawka) > 0:
                return int(stawka)
            else:
                print("Niepoprawna stawka! Podaj liczbę całkowitą większą od 0.")


    def sprawdz_wynik(self, wybrane_liczby, wylosowane_liczby, stawka_kwota):
        trafione_liczby = set(wybrane_liczby) & set(wylosowane_liczby)
        ilosc_trafien = len(trafione_liczby)
        nagroda = 0
        if ilosc_trafien == 5:
            nagroda = stawka_kwota * 1000  
            return f"Jackpot! Wygrałeś główną nagrodę w wysokości ${nagroda}!"
        elif ilosc_trafien == 4:
            nagroda = stawka_kwota * 100  
            return f"Gratulacje! Wygrałeś nagrodę za trafienie 4 liczb w wysokości ${nagroda}!"
        elif ilosc_trafien == 3:
            nagroda = stawka_kwota * 10  
            return f"Świetnie! Wygrałeś nagrodę za trafienie 3 liczb w wysokości ${nagroda}!"
        elif ilosc_trafien == 2:
            nagroda = stawka_kwota * 5  
            return f"Dobra robota! Wygrałeś nagrodę za trafienie 2 liczb w wysokości ${nagroda}!"
        elif ilosc_trafien == 1:
            nagroda = stawka_kwota * 2  
            return f"Masz szczęście! Wygrałeś nagrodę za trafienie 1 liczby w wysokości ${nagroda}!"
        else:
            return "Niestety, nie udało ci się wygrać. Spróbuj ponownie!"


    def loteria(self):
        print("Witaj w loterii!")
        print("Zasady gry: Wybierz od 1 do 10 liczb od 1 do 50.")
        print("Jeśli trafisz wszystkie wybrane liczby, wygrywasz główną nagrodę!")
        print("Masz także szansę na mniejsze nagrody za trafienie części liczb.")
        print("=========================================================================")

        ilosc_liczb = int(input("Wybierz ilość liczb do obstawienia (od 1 do 10): "))
        if ilosc_liczb < 1 or ilosc_liczb > 10:
            print("Niepoprawna ilość liczb!")
            return

        wybrane_liczby = []
        for i in range(ilosc_liczb):
            while True:
                liczba = input(f"Wybierz liczbę {i + 1}: ")
                if liczba.isdigit() and 1 <= int(liczba) <= 50:
                    if int(liczba) not in wybrane_liczby:
                        wybrane_liczby.append(int(liczba))
                        break
                    else:
                        print("Ta liczba została już wybrana. Wybierz inną.")
                else:
                    print("Niepoprawna liczba! Wybierz liczbę od 1 do 50.")

        print("Twoje wybrane liczby:", wybrane_liczby)
        stawka_kwota = self.obstaw_stawke()
        print(f"Obstawiona stawka: ${stawka_kwota}")
        print("Losowanie liczby...")
        time.sleep(2)
        wylosowane_liczby = self.losowanie_liczb()
        print("Wylosowane liczby to:", wylosowane_liczby)
        wynik = self.sprawdz_wynik(wybrane_liczby, wylosowane_liczby, stawka_kwota)
        print(wynik)

        if "Niestety" in wynik:
            self.stan_konta -= stawka_kwota



    def pokaz_stan_konta(self):
        print("=========================================================================")
        print("Twój aktualny stan konta: $", self.stan_konta)
        print("Twoje zadłużenie: $", self.zadluzenie)
        print("=========================================================================")


    def rzut_kostka(self):
        return random.randint(1, 6)


    def zaciagnij_kredyt(self):
        while True:
            czy_kredyt = input("Czy chcesz zaciągnąć kredyt? (t/n): ")
            if czy_kredyt.lower() == 't':
                while True:
                    kwota_kredytu = input("Podaj kwotę kredytu do zaciągnięcia: ")
                    if kwota_kredytu.isdigit() and int(kwota_kredytu) > 0:
                        self.stan_konta += int(kwota_kredytu)
                        self.zadluzenie += int(kwota_kredytu)
                        print("Zaciągnąłeś kredyt na kwotę $", kwota_kredytu)
                        break
                    else:
                        print("Niepoprawna kwota kredytu! Podaj liczbę całkowitą większą od 0.")
                break
            elif czy_kredyt.lower() == 'n':
                break
            else:
                print("Niepoprawny wybór! Wpisz 't' lub 'n'.")


    def splata_kredytu(self):
        if self.zadluzenie > 0:
            odsetki = int(self.zadluzenie * 0.30)  
            print("Do spłaty kredytu z odsetkami: $", self.zadluzenie + odsetki)
            while True:
                czy_splata = input("Czy chcesz spłacić cały kredyt wraz z odsetkami? (t/n): ")
                if czy_splata.lower() == 't':
                    self.stan_konta -= (self.zadluzenie + odsetki)
                    self.zadluzenie = 0
                    print("Spłaciłeś kredyt wraz z odsetkami.")
                    break
                elif czy_splata.lower() == 'n':
                    print("Nie masz wystarczającej ilości pieniędzy na spłatę kredytu.")
                    print("Spróbuj ponownie później.")
                    break
                else:
                    print("Niepoprawny wybór! Wpisz 't' lub 'n'.")


    def przegrana(self, kwota):
        self.stan_konta -= kwota


    def wygrana(self, kwota):
        self.stan_konta += kwota


    def sprawdz_stawke(self):
        return self.stan_konta >= self.stawka


    def dodaj_karte(self, karta):
        self.reka.append(karta)


    def usun_reke(self):
        self.reka = []


    def wyswietl_reke(self):
        print("Twoja ręka:")
        for karta in self.reka:
            print(f"{karta['wartosc']} {karta['kolor']}")


    def wyswietl_stan_konta(self):
        print(f"Stan konta: {self.stan_konta}")


    def dobierz_karte(self, talia):
        karta = rozdaj_karte(talia)
        self.reka.append(karta)


    def dobierz_poczatkowe_karty(self, talia):
        self.dobierz_karte(talia)
        self.dobierz_karte(talia)


    def dobierz_ostatnia_karte(self, talia):
        print("Dobieranie ostatniej karty...")
        self.dobierz_karte(talia)


def utworz_karte(kolor, wartosc):
    return {"kolor": kolor, "wartosc": wartosc}


def utworz_talie():
    talia = []
    kolory = ['♥', '♦', '♣', '♠']
    wartosci = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    for kolor in kolory:
        for wartosc in wartosci:
            talia.append(utworz_karte(kolor, wartosc))
    return talia

def tasuj_talie(talia):
    random.shuffle(talia)

def rozdaj_karte(talia):
    return talia.pop()


def obstawanie(gracz, stawka):
    while True:
        print(f"Twój aktualny stan konta: {gracz.stan_konta}")
        print(f"Stawka na stole: {gracz.stawka}")
        print("Czy chcesz zagrać za stawkę? (tak/nie)")
        odpowiedz = input().lower()
        if odpowiedz == 't' or odpowiedz == 'tak':
            try:
                if gracz.sprawdz_stawke():
                    gracz.przegrana(gracz.stawka)
                    return True
                else:
                    print("Nie masz wystarczająco pieniędzy.")
            except ValueError:
                print("Podana wartość musi być liczbą całkowitą.")
        elif odpowiedz == 'n' or odpowiedz == 'nie':
            return False
        else:
            print("Nieprawidłowa odpowiedź. Proszę odpowiedzieć 'tak' lub 'nie'.")


def sprawdz_reke(gracz):
    karty = sorted(gracz.reka, key=lambda x: x["wartosc"], reverse=True)
    wartosci_kart = [karta["wartosc"] for karta in karty]

    if len(set([karta["kolor"] for karta in karty])) == 1:
        return "Kolor"

    wartosci = [wartosci_kart[karty.index(karta)] for karta in karty]
    if len(set(wartosci)) == 5 and (max(wartosci) - min(wartosci) == 4):
        return "Strit"

    for wartosc in wartosci_kart:
        if wartosci_kart.count(wartosc) == 4:
            return "Kareta"
        if wartosci_kart.count(wartosc) == 3:
            if "Para" in [wartosci_kart.count(w) for w in wartosci_kart]:
                return "Full"
            else:
                return "Trójka"
        if wartosci_kart.count(wartosc) == 2:
            if "Para" in [wartosci_kart.count(w) for w in wartosci_kart]:
                return "Dwie Pary"
            else:
                return "Para"

    return "Nic"


def nowa_runda(gracz, talia, stawka, wyniki):
    gracz.dobierz_poczatkowe_karty(talia)
    gracz.wyswietl_reke()
    gracz.stawka = stawka  # Ustawiamy stawkę gracza na wartość globalnej stawki
    obstawienie = obstawanie(gracz, stawka)
    if obstawienie:
        podbicie = czy_podbic_stawke(gracz, stawka)
        if podbicie:
            gracz.dobierz_ostatnia_karte(talia)
            gracz.wyswietl_reke()
            if obstawanie(gracz, stawka):
                gracz.dobierz_ostatnia_karte(talia)
                gracz.wyswietl_reke()
                wynik = sprawdz_reke(gracz)
                wyswietl_wynik(wynik)
                if wynik != "Nic":
                    wygrana_kwota = stawka * wyniki[wynik]
                    gracz.wygrana(wygrana_kwota)
                    print(f"Wygrałeś! Zdobywasz {wygrana_kwota} żetonów!")
                else:
                    print("Przegrałeś!")
        else:
            print("Nie chcesz podbić stawki.")
            if obstawanie(gracz, stawka):
                gracz.dobierz_ostatnia_karte(talia)
                gracz.wyswietl_reke()
                wynik = sprawdz_reke(gracz)
                wyswietl_wynik(wynik)
                if wynik != "Nic":
                    wygrana_kwota = stawka * wyniki[wynik]
                    gracz.wygrana(wygrana_kwota)
                    print(f"Wygrałeś! Zdobywasz {wygrana_kwota} żetonów!")
                else:
                    print("Przegrałeś!")
    else:
        print("Nie chcesz postawić stawki.")
        if obstawanie(gracz, stawka):
            gracz.dobierz_ostatnia_karte(talia)
            gracz.wyswietl_reke()
            wynik = sprawdz_reke(gracz)
            wyswietl_wynik(wynik)
            if wynik != "Nic":
                wygrana_kwota = stawka


def czy_podbic_stawke(gracz, stawka, min_podbij_stawke=2, max_podbij_stawke=5):
    while True:
        print("Czy chcesz podbić stawkę? (tak/nie)")
        odpowiedz = input().lower()
        if odpowiedz == 'tak':
            print("Podaj kwotę do podbicia:")
            try:
                podbicie = int(input())
                if podbicie >= min_podbij_stawke and podbicie <= max_podbij_stawke:
                    if podbicie <= gracz.stan_konta:
                        gracz.przegrana(podbicie)
                        gracz.stawka += podbicie  # Aktualizujemy stawkę gracza
                        print(f"Stawka została podbita o {podbicie}. Nowa stawka: {gracz.stawka}")
                        return True
                    else:
                        print("Nie masz wystarczająco pieniędzy.")
                else:
                    print(f"Podbicie musi być pomiędzy {min_podbij_stawke} a {max_podbij_stawke}.")
            except ValueError:
                print("Podana wartość musi być liczbą całkowitą.")
        elif odpowiedz == 'nie':
            return False
        else:
            print("Nieprawidłowa odpowiedź. Proszę odpowiedzieć 'tak' lub 'nie'.")


def wyswietl_wynik(wynik):
    print("Twój układ to:", wynik)


def gra_poker():
    talia = utworz_talie()
    tasuj_talie(talia)
    gracz = Gracz()
    stawka = 50
    wyniki = {"Nic": 0, "Para": 1, "Dwie Pary": 2, "Trójka": 3, "Strit": 5, "Kolor": 8, "Full": 10, "Kareta": 20}

    print("Witaj w grze Poker!")
    while True:
        nowa_runda(gracz, talia, stawka, wyniki)
        gracz.wyswietl_stan_konta()
        if gracz.stan_konta <= 0:
            print("Nie masz już pieniędzy! Koniec gry!")
            break
        print("Czy chcesz zagrać jeszcze raz? (tak/nie)")
        odpowiedz = input().lower()
        if odpowiedz != 'tak':
            print("Dziękujemy za grę!")
            break


def kasyno():
    print("=========================================================================")
    print("Witaj w naszym kasynie!")
    gracz = Gracz() 


    while True:
        print("=========================================================================")
        print("Twój stan konta: $", gracz.stan_konta)
        print("Twoje zadłużenie: $", gracz.zadluzenie)
        print("\nWybierz opcję:")
        print("1. Zagraj w ruletkę")
        print("2. Zagraj w blackjacka")
        print("3. Zagraj w automaty do gier")
        print("4. Zagraj w kości")
        print("5. Wyścigi psów")
        print("6. Loteria")
        print("7. Zagraj w pokera")
        print("8. Zaciągnij kredyt")
        print("9. Spłać kredyt")
        print("10. Pokaż stan konta")
        print("11. Zakończ")


        wybor = input("Wybierz opcję: ")

        if wybor == "1":
            gracz.ruletka()
        elif wybor == "2":
            gracz.blackjack()
        elif wybor == "3":
            gracz.automaty()
        elif wybor == "4":
            gracz.kosci()
        elif wybor == "5":
            gracz.wyścigi_psów()
        elif wybor == "6":
            gracz.loteria()
        elif wybor == "7":
            gra_poker()  
        elif wybor == "8":
            gracz.zaciagnij_kredyt()
        elif wybor == "9":
            gracz.splata_kredytu()
        elif wybor == "10":
            gracz.pokaz_stan_konta()
        elif wybor == "11":
            print("Dziękujemy za grę!")
            break
        else:
            print("Niepoprawny wybór!")

if __name__ == "__main__":
    kasyno()