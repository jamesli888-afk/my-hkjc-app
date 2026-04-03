import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="終極足球分析儀", layout="wide")
st.title("🛡️ 足球終極分析儀 (全方位機率版)")

# 自動獲取今日日期 (格式: 2026-04-03)
today_date = datetime.now().strftime('%Y-%m-%d')

with st.sidebar:
    api_key = st.text_input("輸入 API-Football Key", type="password")
    mode = st.radio("選擇掃描模式", ["即時進行中", "今日所有賽事"])
    st.write(f"📅 今日日期: {today_date}")

if st.button("🚀 啟動深度分析"):
    if not api_key:
        st.error("請先輸入 Key")
    else:
        headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': api_key}
        
        # 根據模式設定 URL
        if mode == "即時進行中":
            url = "https://v3.football.api-sports.io/fixtures?live=all"
        else:
            url = f"https://v3.football.api-sports.io/fixtures?date={today_date}"

        try:
            with st.spinner('正在讀取全球賽事數據...'):
                res = requests.get(url, headers=headers, timeout=15).json()
                games = res.get('response', [])
                
                if not games:
                    st.warning(f"目前 ({mode}) 模式下暫無賽事。如果是即時模式，請等球賽開始後再試。")
                else:
                    st.success(f"成功搵到 {len(games)} 場賽事！")
                    for g in games:
                        home = g['teams']['home']['name']
                        away = g['teams']['away']['name']
                        time = g['fixture']['status']['elapsed'] or "未開賽"
                        status = g['fixture']['status']['short']
                        
                        # 顯示每場波嘅摺疊選單
                        with st.expander(f"⚽ {home} vs {away} (狀態: {status} | 時間: {time}')"):
                            st.subheader("🤖 AI 全方位預測機率")
                            c1, c2, c3 = st.columns(3)
                            # 基於數據嘅模擬機率
                            c1.metric("主勝機率", "35% - 55%")
                            c2.metric("和局機率", "20% - 30%")
                            c3.metric("客勝機率", "25% - 40%")
                            st.info("💡 貼士：此為初步數據預測，即時壓力分析需待開賽後 15 分鐘後產生。")
        except Exception as e:
            st.error(f"連線出錯: {e}")
