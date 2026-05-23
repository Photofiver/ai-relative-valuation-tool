#!/usr/bin/env python3
"""AI Relative Valuation Tool - wycena porownawcza spolek (multiples)"""

import yfinance as yf
import pandas as pd
import argparse
import sys
from typing import List, Dict
warnings.filterwarnings('ignore')

def pobierz_metryki(ticker: str) -> Dict:
    try:
        stock = yf.Ticker(ticker.upper().strip())
        info = stock.info
        if not info or info.get('regularMarketPrice') is None:
            return {'Ticker': ticker, 'Blad': 'Brak danych'}
        def safe(val, div=1, ndigits=2):
            if val is None or val == 0: return None
            try: return round(float(val) / div, ndigits)
            except: return None
        return {
            'Ticker': ticker.upper(),
            'Nazwa': info.get('longName') or info.get('shortName', 'N/A'),
            'Sektor': info.get('sector', 'N/A'),
            'Branza': info.get('industry', 'N/A'),
            'Cena': info.get('regularMarketPrice'),
            'Market Cap (mln $)': safe(info.get('marketCap'), 1_000_000, 0),
            'EV (mln $)': safe(info.get('enterpriseValue'), 1_000_000, 0),
            'P/E (trailing)': info.get('trailingPE'),
            'P/E (forward)': info.get('forwardPE'),
            'PEG': info.get('pegRatio'),
            'P/B (C/WK)': info.get('priceToBook'),
            'P/S (C/Przychod)': info.get('priceToSalesTrailing12Months'),
            'EV/EBITDA': info.get('enterpriseToEbitda'),
            'EV/Revenue': info.get('enterpriseToRevenue'),
            'ROE (%)': safe(info.get('returnOnEquity'), 0.01, 1),
            'Marza netto (%)': safe(info.get('profitMargins'), 0.01, 1),
            'Wzrost przych. (%)': safe(info.get('revenueGrowth'), 0.01, 1),
            'Dlug/Kapital': info.get('debtToEquity'),
        }
    except Exception as e:
        return {'Ticker': ticker, 'Blad': str(e)[:80]}

def stworz_tabele_porownawcza(tickery: List[str]) -> pd.DataFrame:
    print(f"Pobieram dane dla {len(tickery)} spolek...")
    dane = [pobierz_metryki(t) for t in tickery]
    df = pd.DataFrame(dane)
    if 'Blad' in df.columns:
        bledy = df[df['Blad'].notna()]
        if not bledy.empty: print(f"Problemy: {list(bledy['Ticker'])}")
        df = df[df['Blad'].isna()].drop(columns=['Blad'], errors='ignore')
    if df.empty: return df
    kluczowe = ['P/E (trailing)', 'P/E (forward)', 'PEG', 'P/B (C/WK)', 'P/S (C/Przychod)', 'EV/EBITDA', 'EV/Revenue']
    for col in kluczowe:
        if col in df.columns:
            med = df[col].median()
            if pd.notna(med) and med > 0:
                df[f'{col} vs Med'] = (df[col] / med).round(2)
    vs_cols = [c for c in df.columns if 'vs Med' in c]
    reszta = [c for c in df.columns if c not in vs_cols]
    return df[reszta + vs_cols]

def main():
    parser = argparse.ArgumentParser(description='AI Relative Valuation Tool')
    parser.add_argument('--tickers', type=str, default='MSFT,GOOGL,AMZN,META,AAPL,NVDA', help='Tickery oddzielone przecinkami')
    args = parser.parse_args()
    tickery = [t.strip().upper() for t in args.tickers.split(',') if t.strip()]
    if not tickery: sys.exit(1)
    df = stworz_tabele_porownawcza(tickery)
    if df.empty: return
    print("\n" + "="*90)
    print("TABELA WYCENY POROWNAWCZEJ")
    print("="*90)
    try: print(df.to_markdown(index=False, floatfmt='.2f'))
    except: print(df.to_string(index=False))
    print("\n" + "="*90)
    print("SKOPIUJ PROMPT PONIZEJ I WKLEJ DO GROK")
    print("="*90)
    prompt = f"""Jestes doswiadczonym analitykiem inwestycyjnym (styl Buffett + surowa szczerosc).

Przeanalizuj tabele wyceny porownawczej ponizej.

Cel: Ktore spolki sa wzglednie tanie/drogie? Zwroc uwage na jakosc fundamentow (marze, wzrost, ROE, dlug). Dla kazdej spolki wskaz kluczowe multiple + teze inwestycyjna + ryzyka.

Format:
1. Podsumowanie grupy
2. Analiza spolka po spolce (Ticker - tania/droga + dlaczego + ryzyka)
3. Najciekawsze okazje / czerwone flagi
4. Wnioski (z disclaimerem)

Dane:
{df.to_markdown(index=False, floatfmt='.2f') if not df.empty else 'Brak danych'}
"""
    print(prompt)

if __name__ == "__main__":
    main()
