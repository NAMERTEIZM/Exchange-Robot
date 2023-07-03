import pandas as pd
import ta
import requests

# Sembollerin bulunduğu liste
symbols = ['AAPL', 'IBM', 'GOOGL', 'MSFT']

# RSI sınıra göre satın alma sinyali verilen sembollerin tutulacağı DataFrame
buy_signals = pd.DataFrame(columns=['Symbol', 'Close', 'Dividend', 'RSI'])

# Sembollerin verilerini döngü ile işleme
for symbol in symbols:
    # Verilerin alınacağı API URL'si
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=full&apikey=869F2UFFKLP2LQKY'

    # Verileri DataFrame'e dönüştürme
    response = requests.get(url)
    symbols_data = response.json()
    df = pd.DataFrame(symbols_data['Time Series (Daily)']).T

    # Gerekli sütunları seçme ve tarih sırasına göre sıralama
    df = df[['4. close', '7. dividend amount']]
    df.columns = ['Close', 'Dividend']
    df.sort_index(ascending=True, inplace=True)

    # Sütun veri tiplerini sayısal değere dönüştürme
    df['Close'] = df['Close'].astype(float)
    df['Dividend'] = df['Dividend'].astype(float)

    # RSI hesaplama
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()

    # Satın alma sinyali olan hisseleri belirleme
    rolling_mean = df['Close'].rolling(window=50).mean()
    symbol_buy_signals = df[(df['RSI'] < 35) & (df['Close'] > rolling_mean.shift())]

    # Satın alma sinyali verilen sembolün bilgilerini buy_signals DataFrame'ine ekleme
    if symbol_buy_signals.empty:
        print(f"Satın alma sinyali üretilen hisse bulunmamaktadır: {symbol}")
    else:
        symbol_buy_signals.loc[:, 'Symbol'] = symbol
        buy_signals = pd.concat([buy_signals, symbol_buy_signals], axis=0)

# Sonuçları görüntüleme
print(buy_signals)
