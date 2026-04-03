import streamlit as st
import requests

st.set_page_config(page_title="HKJC 半場大助手")
st.title("⚽ HKJC 半場入球分析儀")

# 側邊欄
with st.sidebar:
    api_key = st.text_input("輸入 API-Football Key", type="password")
    min_pi = st.slider("最低 PI 指數門檻", 10, 40, 20)

if st.button("🔄 刷新即時數據"):
    if not api_key:
        st.error("請輸入 Key")
    else:
        headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': api_key}
        url = "https://v3.football.api-sports.io/fixtures?live=all"
        try:
            res = requests.get(url, headers=headers).json()
            games = res.get('response', [])
            found = False
            for g in games:
                time = g['fixture']['status']['elapsed']
                # 篩選 15-40 分鐘 0:0
                if 15 <= time <= 40 and g['goals']['home'] == 0 and g['goals']['away'] == 0:
                    f_id = g['fixture']['id']
                    # 獲取統計
                    s_url = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={f_id}"
                    s_res = requests.get(s_url, headers=headers).json()
                    stats = s_res.get('response', [])
                    if len(stats) >= 2:
                        def gv(t, n):
                            for s in stats[t]['statistics']:
                                if s['type'] == n: return int(s['value']) if s['value'] else 0
                            return 0
                        sot = gv(0, "Shots on Target") + gv(1, "Shots on Target")
                        cor = gv(0, "Corner Kicks") + gv(1, "Corner Kicks")
                        da = gv(0, "Dangerous Attacks") + gv(1, "Dangerous Attacks")
                        pi = (sot * 3) + (cor * 1.5) + (da * 0.5)
                        if pi >= min_pi:
                            st.success(f"🔥 {g['teams']['home']['name']} vs {g['teams']['away']['name']} | {time}'")
                            st.write(f"PI 指數: {pi:.1f} (射正:{sot} 角:{cor} 危攻:{da})")
                            found = True
            if not found: st.info("暫無符合條件賽事")
        except Exception as e: st.error(f"錯誤: {e}")

