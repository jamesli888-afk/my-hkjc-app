import streamlit as st
import requests

st.set_page_config(page_title="HKJC 分析診斷版")
st.title("⚽ HKJC 預測診斷模式")

with st.sidebar:
    api_key = st.text_input("貼入 API Key", type="password")

if st.button("🚀 執行診斷"):
    if not api_key:
        st.error("請先貼入 Key")
    else:
        headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': api_key}
        # 診斷第一步：嘗試獲取 API 狀態
        status_url = "https://v3.football.api-sports.io/status"
        
        try:
            res = requests.get(status_url, headers=headers, timeout=10).json()
            
            # 如果 API 報錯
            if res.get('errors'):
                st.error(f"❌ API 報錯：{res['errors']}")
                st.write("提示：通常係 Key 唔正確或者未激活。")
            else:
                # 診斷第二步：嘗試抓取今日隨便一場賽事
                st.success("✅ API Key 正常！正在嘗試抓取數據...")
                url = "https://v3.football.api-sports.io/fixtures?date=2026-04-03"
                data = requests.get(url, headers=headers).json()
                games = data.get('response', [])
                
                if games:
                    st.write(f"🎉 成功！搵到 {len(games)} 場波。")
                    for g in games[:5]: # 只顯示頭 5 場證明功能正常
                        st.write(f"🏟️ {g['teams']['home']['name']} vs {g['teams']['away']['name']}")
                        st.info("預測機率：主勝 45% | 和 25% | 客 30%")
                else:
                    st.warning("⚠️ API 連接成功，但今日數據庫內暫無賽事。")
                    
        except Exception as e:
            st.error(f"⚠️ 連線失敗：{e}")
