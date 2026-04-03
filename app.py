import streamlit as st
import requests

# --- App 頁面設定 ---
st.set_page_config(page_title="HKJC 半場大助手", layout="centered")
st.title("⚽ HKJC 半場入球大細分析儀")

# --- 側邊欄設定 ---
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("輸入 API-Football Key", type="password")
    min_pi = st.slider("最低壓力門檻 (PI)", 10, 40, 20)
    st.info("PI 越高代表進攻越猛烈。通常 >22 視為高機會。")

# --- 核心邏輯 ---
if st.button("🔄 刷新即時數據"):
    if not api_key:
        st.warning("請先輸入 API Key！")
    else:
        HEADERS = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': api_key}
        
        with st.spinner('正在分析馬會相關賽事...'):
            url = "https://v3.football.api-sports.io/fixtures?live=all"
            try:
                res = requests.get(url, headers=HEADERS, timeout=15).json()
                all_live = res.get('response', [])
                found = False
                
                for game in all_live:
                    league_name = game['league']['name']
                    country = game['league']['country']
                    
                    # 馬會常用聯賽過濾
                    hkjc_leagues = ["Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1", 
                                    "J1 League", "K League 1", "Super League", "A-League", "Championship"]
                    is_major = any(l in league_name for l in hkjc_leagues) or country in ["England", "Spain", "Germany", "Italy", "France", "Japan", "Brazil", "Portugal", "Netherlands"]
                    
                    time_elapsed = game['fixture']['status']['elapsed']
                    score_home = game['goals']['home']
                    score_away = game['goals']['away']
                    
                    # 篩選上半場 15-40 分鐘 0:0 的熱門場次
                    if is_major and 15 <= time_elapsed <= 40 and score_home == 0 and score_away == 0:
                        fix_id = game['fixture']['id']
                        
                        # 獲取統計數據
                        stats_url = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={fix_id}"
                        s_res = requests.get(stats_url, headers=HEADERS, timeout=10).json()
                        stats = s_res.get('response', [])
                        
                        if len(stats) >= 2:
                            def get_v(t_idx, name):
                                try:
                                    for s in stats[t_idx]['statistics']:
                                        if s['type'] == name: return int(s['value']) if s['value'] else 0
                                except: return 0
                                return 0
                            
                            sot = get_v(0, "Shots on Target") + get_v(1, "Shots on Target")
                            cor = get_v(0, "Corner Kicks") + get_v(1, "Corner Kicks")
                            da = get_v(0, "Dangerous Attacks") + get_v(1, "Dangerous Attacks")
                            
                            # PI 指數公式
                            pi = (sot * 3.0) + (cor * 1.5) + (da * 0.5)
                            
                            if pi >= min_pi:
                                found = True
                                st.success(f"🔥 {game['teams']['home']['name']} vs {game['teams']['away']['name']}")
                                st.write(f"🕒 {time_elapsed} 分鐘 | PI 壓力指數: **{pi:.1f}**")
                                st.write(f"📊 射正:{sot} | 角球:{cor} | 危險進攻:{da}")
                                st.divider()
                
                if not found:
                    st.info("目前暫無符合條件的馬會賽事。")
            except Exception as e:
                st.error(f"連線出錯: {e}")

st.caption("建議：PI > 22 且半場大 0.5 賠率高於 1.6 時考慮。")

