import pandas as pd
import streamlit as st
import requests
import json

st.set_page_config(page_title='ES添削ツール', layout='wide')

OPENROUTER_API_KEY = st.secrets["openrouter_api_key"]

MODEL_ID = "google/gemma-3-27b-it:free" 

# --- CSS適用 (省略なし) ---
st.markdown("""
<style>
    body { font-family: 'Arial', sans-serif; background-color: #b0c4de; color: #333; }
    .stRadio > label { display: inline-block; background-color: #FFFFFF; border-radius: 10px; }
    /* ...その他のスタイル... */
</style>
""", unsafe_allow_html=True)

industry = st.text_input("業界と業種を入力してください", "", placeholder="広告業界・人材業界｜営業職・事務職")
content_type = st.radio("添削内容選択", options=['自己PR', '志望動機', 'ガクチカ', '長所短所'], horizontal=True)
content = st.text_area("こちらに内容を入力してください", height=300)

if st.button('添削する'):
    if content:
        question_text = f"{industry}の{content_type}として、以下の内容を添削してください。\n\n点数100点満点中採点をして、改善案を３つ提示してその改善案を反映した{content_type}を教えてください。\n\n{content}。"
        
        # ぐるぐる回るローディング表示
        with st.spinner('分析中...'):
            try:
                # OpenRouter APIへのリクエスト
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    data=json.dumps({
                        "model": MODEL_ID,
                        "messages": [
                            {"role": "user", "content": question_text}
                        ]
                    })
                )
                
                # 結果の解析
                result = response.json()
                answer = result['choices'][0]['message']['content']
                
                st.subheader("添削結果")
                st.write(answer)
                
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
    else:
        st.error('内容を入力してください。')
