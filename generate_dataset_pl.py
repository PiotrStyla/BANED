#!/usr/bin/env python3
"""
generate_dataset_pl.py - Generator datasetu polskich fake news
Polska wersja generatora z realistycznymi wzorcami fake news i prawdziwych newsów
"""
import random
import csv
import argparse


# ============================================================================
# ŁATWE PRZYKŁADY - Wyraźne rozróżnienie
# ============================================================================

EASY_REAL_TEMPLATES = [
    # Rząd/Polityka
    "{ministerstwo} ogłasza nową {polityka} dotyczącą {temat}",
    "Sejm uchwala ustawę o {temat}",
    "Rada Ministrów przyjmuje program {temat}",
    "Prezydent podpisuje ustawę dotyczącą {temat}",
    "GUS publikuje dane o {temat}",
    "Urząd Miasta ogłasza konkurs na {projekt}",
    "Komisja sejmowa dyskutuje nad {temat}",
    "Premier zapowiada zmiany w {temat}",
    
    # Zdrowie/Nauka
    "Ministerstwo Zdrowia wydaje wytyczne dotyczące {temat}",
    "Badanie opublikowane w {czasopismo} pokazuje {odkrycie}",
    "Naukowcy z {uniwersytet} odkrywają {odkrycie}",
    "Badania kliniczne potwierdzają skuteczność {lek}",
    "Szpital uniwersytecki raportuje sukces terapii {leczenie}",
    "Polska Akademia Nauk prezentuje wyniki badań nad {temat}",
    
    # Edukacja
    "Ministerstwo Edukacji i Nauki wprowadza {program}",
    "{uniwersytet} otrzymuje grant na badania {temat}",
    "Kuratorium zatwierdza nową podstawę programową {przedmiot}",
    "Polski uniwersytet w rankingu najlepszych uczelni",
    
    # Gospodarka/Biznes
    "Giełda Papierów Wartościowych notuje wzrost w sektorze {sektor}",
    "Narodowy Bank Polski utrzymuje stopy procentowe",
    "Podpisano umowę handlową z {kraj}",
    "GUS: {statystyka} w {okres}",
    "Firma polska otrzymuje grant unijny na {projekt}",
    
    # Lokalne
    "Straż Miejska publikuje statystyki przestępczości",
    "Straż Pożarna interweniowała przy {zdarzenie}",
    "Biblioteka otwiera nowy oddział w {dzielnica}",
    "Miejski Zarząd Dróg planuje remont {ulica}",
    "Muzeum organizuje wystawę poświęconą {temat}",
]

EASY_FAKE_TEMPLATES = [
    # Teorie spiskowe
    "Tajemnica {organizacja} ukrywana przed Polakami o {temat}",
    "Rząd ukrywa prawdę o {temat} - wyciek dokumentów",
    "Wielkie koncerny farmaceutyczne tuszują lekarstwo na {choroba}",
    "Illuminati kontroluje {temat} przez {metoda}",
    "Unia Europejska planuje {spisek} przeciwko Polsce",
    "Masoneria kieruje {instytucja} za kulisami",
    "Chemtrails to sposób na {spisek}",
    
    # Absurdalne twierdzenia zdrowotne
    "Jedzenie {jedzenie} leczy {choroba} natychmiast",
    "Picie {napoj} odmładza o 20 lat",
    "Noszenie {przedmiot} chroni przed {zagrozenie}",
    "Patrzenie na {obiekt} poprawia {zdolnosc}",
    "{jedzenie} zawiera sekretny składnik który {efekt}",
    "Medycyna ludowa kuruje {choroba} lepiej niż leki",
    
    # Absurdalne twierdzenia
    "Naukowcy w szoku - {niemozliwe_wydarzenie}",
    "Polak odkrył {niemozliwa_rzecz} na podwórku",
    "Kobieta żyje bez {podstawowa_potrzeba} od {okres}",
    "Dziecko wynalazło {niemozliwe_urzadzenie} w garażu",
    "Emeryt przypadkiem rozwiązał problem {problem}",
    
    # Spiski ekonomiczne
    "Banki planują {zly_plan} Twoje oszczędności",
    "Rząd chce zabronić {zwykla_rzecz} - PILNE",
    "Nowy porządek światowy kontroluje {temat}",
    "Miliarderze knują jak {zly_plan}",
]

# Słowniki podstawień
MINISTERSTWA = ["Ministerstwo Zdrowia", "Ministerstwo Edukacji i Nauki", 
                "Ministerstwo Spraw Wewnętrznych", "Ministerstwo Sprawiedliwości",
                "Ministerstwo Finansów", "Ministerstwo Rozwoju"]

POLITYKI = ["regulację", "program", "strategię", "reformę", "modernizację", "wsparcie"]

TEMATY = ["ochrony zdrowia", "edukacji", "bezpieczeństwa publicznego", "ochrony środowiska",
          "infrastruktury", "cyfryzacji", "energetyki", "zatrudnienia"]

CZASOPISMA = ["Nature", "Science", "The Lancet", "polskim czasopiśmie naukowym", "JAMA"]

UNIWERSYTETY = ["Uniwersytet Warszawski", "Uniwersytet Jagielloński", "Politechnika Warszawska",
                "Uniwersytet im. Adama Mickiewicza", "Uniwersytet Wrocławski"]

ODKRYCIA = ["związek między stylem życia a zdrowiem", "nowy biomarker choroby",
            "poprawę wyników leczenia", "czynniki ryzyka choroby"]

LEKI = ["leku onkologicznego", "szczepionki", "terapii genowej", "antybiotyku"]

LECZENIA = ["leczenia nowotworów", "terapii regeneracyjnej", "immunoterapii"]

PROGRAMY = ["program stypendialny", "program wymiany", "reformę programową"]

PRZEDMIOTY = ["matematyki", "fizyki", "informatyki", "języków obcych"]

SEKTORY = ["technologicznym", "budowlanym", "finansowym", "energetycznym", "medycznym"]

KRAJE = ["Niemcami", "Francją", "USA", "Japonią", "Chinami"]

STATYSTYKI = ["Bezrobocie spadło", "Inflacja wyniosła", "PKB wzrosło", "Eksport zwiększył się"]

OKRESY = ["lipcu 2025", "drugim kwartale", "pierwszym półroczu", "ubiegłym miesiącu"]

PROJEKTY = ["modernizację", "renowację", "budowę", "rozwój"]

ZDARZENIA = ["pożarze budynku", "wycieku gazu", "kolizji", "awarii"]

DZIELNICE = ["Śródmieściu", "Mokotowie", "Woli", "Pradze", "Ursynowie"]

ULICE = ["ul. Marszałkowskiej", "al. Jerozolimskich", "ul. Głównej", "ul. Polnej"]

ORGANIZACJE = ["masoneria", "wielki kapitał", "lobby farmaceutyczne", "elity globalne"]

CHOROBY = ["raka", "cukrzycy", "choroby Alzheimera", "COVID-19", "grypy"]

METODY = ["szczepionki", "5G", "chemtrails", "fluor w wodzie", "GMO"]

SPISKI = ["wprowadzić euro siłą", "zakazać polskiego mięsa", "odebrać suwerenność",
          "wprowadzić chip pod skórę", "zniszczyć polskie rodziny"]

INSTYTUCJE = ["NBP", "Sejm", "media", "sądy", "szkoły"]

JEDZENIA = ["czosnek", "miód", "sok z buraka", "olej kokosowy", "kurkuma", "ocet jabłkowy"]

NAPOJE = ["woda z cytryną", "napar z pokrzywy", "sok z aloesu", "herbata ziołowa"]

PRZEDMIOTY = ["bransoletka miedziana", "naszyjnik bursztynowy", "amulet", "piramida energetyczna"]

OBIEKTY = ["piramida", "kryształ", "magnes", "drzewo", "świeca"]

ZDOLNOSCI = ["wzrok", "pamięć", "koncentrację", "intuicję", "odporność"]

ZAGROZENIA = ["promieniowanie 5G", "smog", "toksyny", "negatywną energię", "chemtrails"]

EFEKTY = ["usuwa toksyny", "wzmacnia odporność", "dodaje energii", "leczy choroby"]

NIEMOZLIWE_WYDARZENIA = ["kot nauczył się mówić", "człowiek przeżył bez jedzenia rok",
                          "znaleziono portal czasoprzestrzenny", "UFO lądowało na Podlasiu"]

NIEMOZLIWE_RZECZY = ["perpetuum mobile", "maszynę do podróży w czasie", "portal do równoległego wszechświata"]

PODSTAWOWE_POTRZEBY = ["jedzenia", "wody", "snu", "tlenu"]

OKRESY = ["20 lat", "dekady", "pięciu lat", "kilku miesięcy"]

PROBLEMY = ["zmian klimatycznych", "głodu na świecie", "chorób cywilizacyjnych", "bezrobocia"]

ZLE_PLANY = ["ukraść", "skonfiskować", "kontrolować", "śledzić", "zabronić"]

ZWYKLE_RZECZY = ["gotówka", "samochody spalinowe", "mięso", "cukier", "prywatność"]


# ============================================================================
# TRUDNE PRZYKŁADY - Clickbait/Pseudonauka
# ============================================================================

HARD_REAL_TEMPLATES = [
    "Nie uwierzysz co {autoryt} odkrył o {temat}",
    "Naukowcy w szoku przez nieoczekiwane {odkrycie} w badaniach {dziedzina}",
    "Badanie ujawnia zaskakującą prawdę o {temat}",
    "Eksperci ostrzegają przed niepokojącym trendem w {temat}",
    "Rewolucyjna {technologia} obiecuje zmienić {dziedzina}",
    "Przełomowe badania podważają powszechne przekonania o {temat}",
    "Śledztwo ujawnia niepokojące wzorce w {temat}",
    "Badania pokazują sprzeczne z intuicją wyniki dotyczące {temat}",
    "Analiza wykazuje zaskakujące połączenie między {temat1} a {temat2}",
    "Badacze obserwują niezwykłe zjawisko w {dziedzina}",
]

HARD_FAKE_TEMPLATES = [
    "Badania pokazują że {technologia} może wpływać na {efekt_zdrowotny}",
    "Eksperci coraz bardziej zaniepokojeni {zwykla_rzecz}",
    "Nowe badania sugerują związek między {temat1} a {negatywny_efekt}",
    "Naukowcy debatują nad kontrowersyjnymi odkryciami o {temat}",
    "Alternatywni {zawod} raportują sukces z {pseudonauka}",
    "Badacze kwestionują główny nurt nauki o {temat}",
    "Badanie znajduje korelację między {zwykla_rzecz} a {efekt_zdrowotny}",
    "Śledztwo ujawnia że {autoryt} może ukrywać {sekret}",
    "Badania sugerują że główny nurt {dziedzina} tłumi {alternatywa}",
    "Eksperci ostrzegają że {zwykla_rzecz} wpływa na {efekt_zdrowotny}",
    "Badanie pokazuje możliwy związek między {temat1} a {problem}",
    "Śledztwo odkrywa konflikty interesów w {dziedzina}",
]

AUTORYTETY = ["polscy naukowcy", "badacze", "lekarze", "eksperci", "specjaliści"]

DZIEDZINY = ["medycyny", "fizyki", "biologii", "psychologii", "neurologii", "ekologii"]

TECHNOLOGIE = ["sztuczna inteligencja", "5G", "urządzenie medyczne", "metoda leczenia"]

EFEKTY_ZDROWOTNE = ["aktywność mózgu", "poziom hormonów", "odpowiedź immunologiczną", 
                     "jakość snu", "funkcje poznawcze"]

NEGATYWNE_EFEKTY = ["zwiększone ryzyko", "niepożądane skutki", "powikłania", "skutki uboczne"]

PSEUDONAUKI = ["uzdrawianie energią", "naturalne metody", "starożytne praktyki", "detoks"]

SEKRETY = ["naturalne lekarstwa", "prawdziwe dane", "rzeczywiste odkrycia", "prawdę"]

ALTERNATYWY = ["terapie alternatywne", "podejścia holistyczne", "metody naturalne"]

PROBLEMY_ZDROWOTNE = ["choroby przewlekłe", "problemy ze zdrowiem psychicznym", "zaburzenia"]


# ============================================================================
# EKSTREMALNE - Satira, Propaganda, Manipulacja Kontekstem  
# ============================================================================

EXTREME_REAL_TEMPLATES = [
    # Satira (wyraźnie oznaczona)
    "Satyra: {absurdalny_naglowek} parodia wyśmiewa {temat}",
    "Program komediowy prezentuje satyryczne spojrzenie na {temat}",
    "Strona humorystyczna publikuje wyraźnie fałszywą {historie} dla rozrywki",
    
    # Ujawnione konflikty
    "Badanie finansowane przez {przemysl} z ujawnionymi konfliktami pokazuje {odkrycie}",
    "Artykuł naukowy wyraźnie określa ograniczenia i {ujawnienie}",
    "Wyniki badań klinicznych opublikowane z przejrzystym {ujawnienie}",
    
    # Właściwy kontekst
    "Ekspert cytowany w kontekście wyjaśnia zarówno {aspekt1} jak i {aspekt2}",
    "Lekarz w wywiadzie podaje pełne wyjaśnienie {termin_statystyczny}",
    "Naukowiec podkreśla niepewność i potrzebę dalszych badań",
    
    # Niuansowane odkrycia
    "Dane zdrowotne pokazują mieszane wyniki z {niuans}",
    "Badanie znajduje złożoną relację między zmiennymi z {warunki}",
]

EXTREME_FAKE_TEMPLATES = [
    # Nieoznaczona satira
    "Lokalny {zawod} {absurdalne_osiagniecie} szokujące rewelacje",
    "Mieszkaniec {miasto} wciąż nie {przyziemne_zadanie} wiadomość dnia",
    "Naród podzielony przez {trywialna_rzecz} kontrowersje trwają",
    
    # Ukryte konflikty
    "Badanie opłacone przez {przemysl} stwierdza {wygodne_odkrycie}",
    "Sponsorowane przez {przemysl} badanie pokazuje że {produkt} jest lepszy",
    "Śledztwo finansowane przez korporacje nie znajduje problemów z {produkt}",
    
    # Mylący kontekst
    "Lekarz poleca {niepotrzebne_leczenie} na {drobna_dolegliwosc}",
    "Jeden pacjent miał {reakcja} więc leczenie musi być niebezpieczne",
    "Dowody anegdotyczne sugerują że {niesprawdzony_srodek} działa",
    
    # Ramowanie spisku
    "Nowe badanie ujawnia szokującą prawdę którą {autoryt} chce ukryć",
    "Badania odkrywają co wielki {przemysl} ukrywa",
    "Śledztwo demaskuje główny nurt {dziedzina} tuszujący odkrycia",
    
    # Fałszywa równowaga
    "Eksperci kwestionują wszystko co sądziliśmy o {temat}",
    "Naturalne lekarstwo leczy {choroba} lepiej niż leki",
    "Starożytna {praktyka} okazuje się lepsza od nowoczesnej {dziedzina}",
]

ABSURDALNE_NAGLOWKI = ["Kowal z Krakowa rozwiązał problem głodu", "Babcia z Podlasia wynalazła warp drive",
                       "Kot został prezydentem miasta", "Pies nauczył się programować"]

HISTORIE = ["historię o kosmitach", "bajkę o cudzie", "opowieść o niemożliwości"]

ASPEKTY = ["korzyści", "ryzyko", "niepewność", "ograniczenia"]

TERMINY_STATYSTYCZNE = ["istotność statystyczna", "przedziały ufności", "wielkość efektu"]

NIUANSE = ["efekty zależne od kontekstu", "wyniki specyficzne dla populacji"]

WARUNKU = ["określonymi warunkami", "konkretnymi populacjami", "kontrolowanym środowiskiem"]

ZAWODY = ["hydraulik", "księgowy", "bibliotekarz", "mechanik", "sprzedawca"]

ABSURDALNE_OSIAGNIECIA = ["odkrył lekarstwo na raka", "rozwiązał problem zmian klimatu", "wynalazł perpetuum mobile"]

MIASTA = ["Radomia", "Sosnowca", "Lublina", "Kielc", "Olsztyna"]

PRZYZIEMNE_ZADANIA = ["przeczytał regulaminu", "zrobił aktualizacji Windows", "naprawił drukarki"]

TRYWIALNE_RZECZY = ["kolor guzików", "długość sznurowadeł", "rodzaj kawy"]

PRZEMYSLY = ["farmaceutyczny", "tytoniowy", "naftowy", "chemiczny", "spożywczy"]

WYGODNE_ODKRYCIA = ["ich produkt jest bezpieczny", "konkurencja jest gorsza", "regulacje są niepotrzebne"]

PRODUKTY = ["produktem", "lekiem", "dodatkiem do żywności", "technologią"]

NIEPOTRZEBNE_LECZENIA = ["kosztowną terapię", "eksperymentalny zabieg", "suplement diety"]

DROBNE_DOLEGLIWOSCI = ["przeziębienie", "ból głowy", "zmęczenie", "suchość skóry"]

REAKCJE = ["wysypkę", "ból brzucha", "senność", "nudności"]

NIESPRAWDZONE_SRODKI = ["sok z aloesu", "homeopatia", "detoks", "oczyszczanie organizmu"]

PRAKTYKI = ["praktyka ajurwedy", "medycyna chińska", "leczenie ziołami"]


def generate_text(template, substitutions):
    """Generate text from template with random substitutions"""
    text = template
    for key, values in substitutions.items():
        if '{' + key + '}' in text:
            text = text.replace('{' + key + '}', random.choice(values))
    return text


def generate_dataset(real_templates, fake_templates, substitutions, real_count, fake_count):
    """Generate dataset with specified counts"""
    dataset = []
    
    # Generate real news
    for _ in range(real_count):
        template = random.choice(real_templates)
        text = generate_text(template, substitutions)
        dataset.append({'text': text, 'label': 1})  # 1 = real
    
    # Generate fake news
    for _ in range(fake_count):
        template = random.choice(fake_templates)
        text = generate_text(template, substitutions)
        dataset.append({'text': text, 'label': 0})  # 0 = fake
    
    random.shuffle(dataset)
    return dataset


def main():
    parser = argparse.ArgumentParser(description='Generate Polish fake news dataset')
    parser.add_argument('--easy_real', type=int, default=1000, help='Number of easy real examples')
    parser.add_argument('--easy_fake', type=int, default=1000, help='Number of easy fake examples')
    parser.add_argument('--hard_real', type=int, default=1000, help='Number of hard real examples')
    parser.add_argument('--hard_fake', type=int, default=1000, help='Number of hard fake examples')
    parser.add_argument('--extreme_real', type=int, default=500, help='Number of extreme real examples')
    parser.add_argument('--extreme_fake', type=int, default=500, help='Number of extreme fake examples')
    parser.add_argument('--output_prefix', type=str, default='fnn_pl', help='Output file prefix')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    
    args = parser.parse_args()
    random.seed(args.seed)
    
    # Prepare substitution dictionaries
    easy_subs = {
        'ministerstwo': MINISTERSTWA, 'polityka': POLITYKI, 'temat': TEMATY,
        'czasopismo': CZASOPISMA, 'uniwersytet': UNIWERSYTETY, 'odkrycie': ODKRYCIA,
        'lek': LEKI, 'leczenie': LECZENIA, 'program': PROGRAMY, 'przedmiot': PRZEDMIOTY,
        'sektor': SEKTORY, 'kraj': KRAJE, 'statystyka': STATYSTYKI, 'okres': OKRESY,
        'projekt': PROJEKTY, 'zdarzenie': ZDARZENIA, 'dzielnica': DZIELNICE, 'ulica': ULICE,
        'organizacja': ORGANIZACJE, 'choroba': CHOROBY, 'metoda': METODY, 'spisek': SPISKI,
        'instytucja': INSTYTUCJE, 'jedzenie': JEDZENIA, 'napoj': NAPOJE,
        'przedmiot': PRZEDMIOTY, 'obiekt': OBIEKTY, 'zdolnosc': ZDOLNOSCI,
        'zagrozenie': ZAGROZENIA, 'efekt': EFEKTY, 'niemozliwe_wydarzenie': NIEMOZLIWE_WYDARZENIA,
        'niemozliwa_rzecz': NIEMOZLIWE_RZECZY, 'podstawowa_potrzeba': PODSTAWOWE_POTRZEBY,
        'okres': OKRESY, 'problem': PROBLEMY, 'zly_plan': ZLE_PLANY,
        'zwykla_rzecz': ZWYKLE_RZECZY, 'niemozliwe_urzadzenie': ['perpetuum mobile', 'maszynę antygrawitacyjną']
    }
    
    hard_subs = {**easy_subs, **{
        'autoryt': AUTORYTETY, 'dziedzina': DZIEDZINY, 'technologia': TECHNOLOGIE,
        'efekt_zdrowotny': EFEKTY_ZDROWOTNE, 'negatywny_efekt': NEGATYWNE_EFEKTY,
        'pseudonauka': PSEUDONAUKI, 'sekret': SEKRETY, 'alternatywa': ALTERNATYWY,
        'problem_zdrowotny': PROBLEMY_ZDROWOTNE, 'zawod': ZAWODY,
        'temat1': TEMATY, 'temat2': TEMATY
    }}
    
    extreme_subs = {**hard_subs, **{
        'absurdalny_naglowek': ABSURDALNE_NAGLOWKI, 'historie': HISTORIE,
        'aspekt1': ASPEKTY, 'aspekt2': ASPEKTY, 'termin_statystyczny': TERMINY_STATYSTYCZNE,
        'niuans': NIUANSE, 'warunki': WARUNKU, 'absurdalne_osiagniecie': ABSURDALNE_OSIAGNIECIA,
        'miasto': MIASTA, 'przyziemne_zadanie': PRZYZIEMNE_ZADANIA, 
        'trywialna_rzecz': TRYWIALNE_RZECZY, 'przemysl': PRZEMYSLY,
        'wygodne_odkrycie': WYGODNE_ODKRYCIA, 'produkt': PRODUKTY,
        'niepotrzebne_leczenie': NIEPOTRZEBNE_LECZENIA, 'drobna_dolegliwosc': DROBNE_DOLEGLIWOSCI,
        'reakcja': REAKCJE, 'niesprawdzony_srodek': NIESPRAWDZONE_SRODKI, 'praktyka': PRAKTYKI,
        'ujawnienie': ['źródła finansowania', 'konflikty interesów']
    }}
    
    # Generate datasets
    if args.easy_real > 0 or args.easy_fake > 0:
        easy_dataset = generate_dataset(EASY_REAL_TEMPLATES, EASY_FAKE_TEMPLATES, 
                                        easy_subs, args.easy_real, args.easy_fake)
        with open(f'{args.output_prefix}_real_easy_{args.easy_real}.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['text', 'label'])
            for item in easy_dataset:
                if item['label'] == 1:
                    writer.writerow([item['text'], item['label']])
        
        with open(f'{args.output_prefix}_fake_easy_{args.easy_fake}.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['text', 'label'])
            for item in easy_dataset:
                if item['label'] == 0:
                    writer.writerow([item['text'], item['label']])
        
        print(f"Generated {args.easy_real} easy real and {args.easy_fake} easy fake Polish examples")
    
    if args.hard_real > 0 or args.hard_fake > 0:
        hard_dataset = generate_dataset(HARD_REAL_TEMPLATES, HARD_FAKE_TEMPLATES,
                                       hard_subs, args.hard_real, args.hard_fake)
        with open(f'{args.output_prefix}_real_hard_{args.hard_real}.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['text', 'label'])
            for item in hard_dataset:
                if item['label'] == 1:
                    writer.writerow([item['text'], item['label']])
        
        with open(f'{args.output_prefix}_fake_hard_{args.hard_fake}.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['text', 'label'])
            for item in hard_dataset:
                if item['label'] == 0:
                    writer.writerow([item['text'], item['label']])
        
        print(f"Generated {args.hard_real} hard real and {args.hard_fake} hard fake Polish examples")
    
    if args.extreme_real > 0 or args.extreme_fake > 0:
        extreme_dataset = generate_dataset(EXTREME_REAL_TEMPLATES, EXTREME_FAKE_TEMPLATES,
                                          extreme_subs, args.extreme_real, args.extreme_fake)
        with open(f'{args.output_prefix}_real_extreme_{args.extreme_real}.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['text', 'label'])
            for item in extreme_dataset:
                if item['label'] == 1:
                    writer.writerow([item['text'], item['label']])
        
        with open(f'{args.output_prefix}_fake_extreme_{args.extreme_fake}.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['text', 'label'])
            for item in extreme_dataset:
                if item['label'] == 0:
                    writer.writerow([item['text'], item['label']])
        
        print(f"Generated {args.extreme_real} extreme real and {args.extreme_fake} extreme fake Polish examples")
    
    print("\n✅ Polish dataset generation completed!")


if __name__ == '__main__':
    main()
