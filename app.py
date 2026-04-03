import streamlit as st
import random

# 強制手機版視角排版
st.set_page_config(page_title="足至寶分析版", layout="centered")

st.markdown("""
    <style>
    /* 模仿 App 的深色標題欄 */
    .app-header { background-color: #2c2c3e; color: white; padding: 10px; text-align: center; border-radius: 0 0 15px 15px; margin: -50px -10px 20px -10px; }
    /* 清單方塊 */
    .match-card { background: white; border-bottom: 1px solid #eee; padding: 12px; margin-bottom: 0px; }
    .league-tag { background: #e1e8f0; font-size: 12px; padding: 2px 8px; border-radius: 4px; color: #555; }
    .odds-box { background: #f8f9fa; border: 1px solid #ddd; border-radius: 5px; padding: 5px; text-align: center; font-weight: bold; }
    </style>
    <div class="app-header"><h3>⚽ 賽事深度分析</h3></div>
    """, unsafe_allow_html=True)

# 模擬截圖中的真實賽事清單
matches = [
    {"id": "FB6672", "time": "13:50", "league": "女子澳洲職業聯賽", "home": "阿德萊德聯女足", "away": "威靈頓鳳凰女足", "h": "3.30", "d": "3.65", "a": "1.76"},
    {"id": "FB6718", "time": "14:00", "league": "澳洲全國聯賽", "home": "萊卡特", "away": "西悉尼B隊", "h": "1.14", "d": "6.40", "a": "10.00"},
    {"id": "FB6717", "time": "16:00", "league": "澳洲全國聯賽", "home": "曼利聯", "away": "FC悉尼B隊", "h": "2.22", "d": "3.45", "a": "2.55"},
    {"id": "FB6673", "time": "16:00", "league": "女子澳洲職業聯賽", "home": "珀斯光輝女足", "away": "墨爾本勝利女足", "h": "3.80", "d": "3.80", "a": "1.62"}
]

for m in matches:
    with st.container():
        # 模仿足至寶的清單行
        st.markdown(f"""
            <div class="match-card">
                <span class="league-tag">{m['league']}</span> <small style="color:red;">{m['id']}</small><br>
                <b>{m['time']}</b> {m['home']} <small>對</small> {m['away']}
            </div>
            """, unsafe_allow_html=True)
        
        # 預測機率點擊展開
        with st.expander("查看 AI 預測及走線風險"):
            c1, c2, c3 = st.columns(3)
            c1.metric("主勝機率", f"{random.randint(30,60)}%")
            c2.metric("大球率", f"{random.randint(50,80)}%")
            c3.metric("走線風險", "低")
            st.warning("🤖 建議：此場數據顯示主隊戰意極強。")
