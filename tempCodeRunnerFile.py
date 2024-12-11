
# # 제목
# st.title("📈 주식 데이터 분석 대시보드")

# # 파일 업로드
# uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])

# if uploaded_file is not None:
#     # 데이터 로드
#     df = pd.read_csv(uploaded_file)
#     st.write("### 업로드된 데이터")
#     st.write(df.head())

#     # 열 선택
#     numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns
#     st.sidebar.header("📊 분석 옵션")
#     column_to_analyze = st.sidebar.selectbox("분석할 열을 선택하세요", numeric_columns)

#     # 기본 통계
#     st.write("### 기본 통계")
#     st.write(df[column_to_analyze].describe())

#     # 히스토그램
#     st.write("### 히스토그램")
#     fig, ax = plt.subplots()
#     ax.hist(df[column_to_analyze], bins=20, color="skyblue", edgecolor="black")
#     ax.set_title(f"{column_to_analyze} 분포")
#     ax.set_xlabel(column_to_analyze)
#     ax.set_ylabel("빈도수")
#     st.pyplot(fig)

#     # 날짜 기반 시계열 분석
#     if "Date" in df.columns:
#         df["Date"] = pd.to_datetime(df["Date"])
#         df = df.sort_values("Date")

#         st.write("### 시계열 데이터")
#         st.line_chart(df.set_index("Date")[column_to_analyze])

# else:
#     st.info("데이터를 업로드하면 분석 결과를 확인할 수 있습니다.")