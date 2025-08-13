import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import seaborn as sns
import numpy as np
import io
import warnings

warnings.filterwarnings('ignore')


st.set_page_config(page_title="Tips dashboard", layout="wide")
st.title("Аналитика чаевых")

uploaded_file = st.sidebar.file_uploader("Загрузите CSV", type=["csv"])

# Если файл не загружен — останавливаем скрипт, чтобы ниже код не выполнялся
if uploaded_file is None:
    st.info("Выберите CSV слева, чтобы продолжить.")
    st.stop()

# Читаем CSV в DataFrame
try:
    # при необходимости: pd.read_csv(uploaded_file, sep=";", encoding="utf-8")
    df = pd.read_csv(uploaded_file)
    start_date = pd.to_datetime('2023-01-01')

    rnd_day = np.random.randint(0, 31, size=len(df))

    df['time_order'] = start_date + pd.to_timedelta(rnd_day, unit="D")

except Exception as e:
    st.error(f"Не удалось прочитать CSV: {e}")
    st.stop()

st.success(f"Файл загружен: {uploaded_file.name}")
#st.dataframe(df, use_container_width=True)
st.write("Первые 5 строк:")
st.write(df.head(5))

# Кнопка строит динамику
if st.sidebar.button("Динамика чаевых во времени"):
    # Проверяем необходимые колонки
    required = {"time_order", "tip"}
    if not required.issubset(df.columns):
        st.error(f"В CSV должны быть колонки: {required}. Найдено: {set(df.columns)}")
    else:
        # Убедимся, что время в правильном формате
        df["time_order"] = pd.to_datetime(df["time_order"], errors="coerce")
        df = df.dropna(subset=["time_order", "tip"])

        # Строим график с seaborn
        g = sns.relplot(
            data=df,
            x="time_order",
            y="tip",
            hue="day",
            kind="line",
            height=5,
            aspect=2
        )
    st.pyplot(g.fig)

    #сохраняем график в формате картинке png, чтобы потом скачать его
    buf = io.BytesIO()
    g.fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    buf.seek(0)


    st.sidebar.download_button(label='Скачать график',
                                             data=buf,
                                             file_name='download png',
                                             mime="image/png"
                                             )



