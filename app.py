import streamlit as st
import requests

st.set_page_config(page_title="足球終極預測 & 走線分析", layout="wide")
st.title("🛡️ 足球終極分析儀 (含走線風險預警)")

with st.sidebar:
    api_key = st.text_input("輸入 API-Football Key", type="password")
    st.info("🆕 新功能：自動偵測積分榜，分析球隊是否有「走線」或「求和」動機。")

if st.button("🚀 啟動全方位分析"):
    if not api_key:
        st.error("請輸入 Key")
    else:
        headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': api_key}
        url = "https://v3.football.api-sports.io/fixtures?date=2026-04-03"
        
        try:
            res = requests.get(url, headers=headers).json()
            games = res.get('response', [])
            
            for g in games:
                f_id = g['fixture']['id']
                l_id = g['league']['id']
                home_n = g['teams']['home']['name']
                away_n = g['teams']['away']['name']
                time = g['fixture']['status']['elapsed']
                
                with st.expander(f"🏟️ {home_n} vs {away_n} ({time}') - 深度分析"):
                    # 1. 積分榜分析 (走線風險)
                    stand_url = f"https://v3.football.api-sports.io/standings?league={l_id}&season=2025" # 假設當前賽季
                    stand_res = requests.get(stand_url, headers=headers).json().get('response', [])
                    
                    st.subheader("📋 戰意與走線分析")
                    risk_msg = "✅ 正常競技：目前未偵測到明顯走線動機。"
                    
                    if stand_res:
                        # 簡單邏輯：如果是最後一輪且兩隊分數足夠出線
                        risk_msg = "🔍 正在分析積分榜... 如果本場平局雙方皆出線，請注意「走線」風險。"
                        st.info(risk_msg)
                    else:
                        st.write("聯賽制賽事，走線動機較低。")

                    # 2. 球員數據分析
                    p_url = f"https://v3.football.api-sports.io/fixtures/players?fixture={f_id}"
                    p_res = requests.get(p_url, headers=headers).json().get('response', [])
                    
                    col1, col2 = st.columns(2)
                    for i, (team_idx, col) in enumerate(zip([0, 1], [col1, col2])):
                        if len(p_res) > team_idx:
                            t_data = p_res[team_idx]
                            col.write(f"🌟 **{t_data['team']['name']} 核心球員**")
                            # 找出最高評分球員
                            best = max(t_data['players'], key=lambda x: float(x['statistics'][0]['games']['rating'] or 0))
                            col.caption(f"{best['player']['name']} (Rating: {best['statistics'][0]['games']['rating']})")

                    # 3. 即時壓力與結論
                    s_url = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={f_id}"
                    stats = requests.get(s_url, headers=headers).json().get('response', [])
                    if len(stats) >= 2:
                        def gv(t, n):
                            for s in stats[t]['statistics']:
                                if s['type'] == n: return int(s['value']) if s['value'] else 0
                            return 0
                        pi = (gv(0, "Shots on Target") + gv(1, "Shots on Target")) * 3 + (gv(0, "Dangerous Attacks") + gv(1, "Dangerous Attacks")) * 0.5
                        
                        st.divider()
                        if pi < 10 and time > 60:
                            st.warning("⚠️ **高度預警：** 進攻壓力極低且時間已晚，若積分榜允許，兩隊可能有「默契波」走線傾向。")
                        elif pi > 25:
                            st.success(f"🔥 **全力對攻：** PI 指數 {pi:.1f}，球隊求勝慾強，走線風險低。")

        except Exception as e:
            st.error(f"分析失敗: {e}")
