import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일을 읽어올 때 header=1로 지정하여 첫 번째 행을 열 이름으로 설정
df = pd.read_csv('your_file.csv', header=1)

# 'Date' 열을 datetime 형식으로 변환
df['Date'] = pd.to_datetime(df['Date'])

# 데이터프레임 확인 (열 이름 확인)
print(df.head())

# 그래프 그리기
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Close'], label='Close Price', color='blue')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.title('Stock Price Over Time')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()