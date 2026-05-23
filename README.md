# AI Relative Valuation Tool

**Narzędzie do szybkiej wyceny spółek metodą porównawczą (relative valuation / multiples)**

Stworzone z pomocą Grok na podstawie rozmowy o narzędziu Marcina Tuszkiewicza (Squaber).

Działa **idealnie na telefonie Android** przez **Termux**.

## 📱 Szybki start na Androidzie (Termux)

1. Zainstaluj **Termux** z **F-Droid** (nie ze Sklepu Google Play!)
2. Otwórz Termux i wykonaj:

```bash
pkg update && pkg upgrade -y
pkg install python git -y
```

3. Sklonuj repozytorium:

```bash
git clone https://github.com/Photofiver/ai-relative-valuation-tool.git
cd ai-relative-valuation-tool
```

4. Zainstaluj zależności:

```bash
pip install -r requirements.txt
```

5. Uruchom narzędzie:

```bash
python valuation_comparator.py
```

Lub z własnymi tickerami (zalecane):

```bash
python valuation_comparator.py --tickers "MSFT,GOOGL,AMZN,META,AAPL,NVDA"
```

6. Skopiuj cały wygenerowany **prompt** i wklej go tutaj do mnie (Grok) – dostaniesz profesjonalną, bezkompromisową analizę AI.

## Co robi narzędzie?

- Automatycznie pobiera świeże dane rynkowe i fundamentalne (Yahoo Finance)
- Tworzy tabelę porównawczą kluczowych multiple:
  - P/E (trailing & forward)
  - EV/EBITDA, EV/Revenue
  - P/B, P/S, PEG
  - ROE, marże, wzrost przychodów itp.
- Oblicza wartości **względem mediany grupy** (`< 1` = tańsza niż średnia w grupie)
- Generuje gotowy, szczegółowy prompt dla AI z analizą + tezą inwestycyjną

Całość zajmuje **1-2 minuty** + czas na analizę AI.

## Użycie na komputerze / laptopie

Identycznie jak powyżej.

## Pliki w repo

- `valuation_comparator.py` – główny skrypt
- `requirements.txt` – zależności
- `README.md` – ta instrukcja

## Rozwój narzędzia

Chcesz coś dodać? Napisz do mnie:
- Więcej wskaźników (FCF yield, ROIC, Debt/EBITDA...)
- Eksport do Excela z kolorowaniem
- Prosty interfejs web (Streamlit)
- Automatyczny wybór peerów po sektorze
- Codzienne skanowanie / alerty
- Integracja z Twoim Trader 21

## Disclaimer

**To NIE jest porada inwestycyjna.**
Dane pochodzą z Yahoo Finance i mogą zawierać opóźnienia lub błędy.
Zawsze weryfikuj informacje samodzielnie.
Inwestowanie na giełdzie wiąże się z ryzykiem utraty kapitału.

Stworzone dla Ciebie – Tomasz. Miłego używania! 🚀