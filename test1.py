import yfinance as yf

# 티커와 날짜 범위 설정
ticker = 'AAPL'  # 예: Apple
start_date = '2020-01-01'
end_date = '2024-01-01'

# 데이터 다운로드
data = yf.download(ticker, start=start_date, end=end_date)

# CSV 파일로 저장
data.to_csv(f'{ticker}_stock_data.csv')

print(f"{ticker}의 데이터가 CSV 파일로 저장되었습니다.")