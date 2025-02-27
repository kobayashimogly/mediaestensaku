import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import streamlit as st
import google.generativeai as genai

# APIキーの設定
api_key = st.secrets["gemini_api_key"]
genai.configure(api_key=api_key)

# モデルの設定
model = genai.GenerativeModel('gemini-2.0-flash')

# タイトルと画像
st.set_page_config(page_title='ES添削ツール', layout='wide')


# CSSを適用
st.markdown("""
<style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #b0c4de;
        color: #333;
    }
    .css-1aumxhk, .css-hi6a2p, .st-bq, .st-b7 {
        font-weight: bold; /* ラベルの文字を太く */
    }
    .stRadio > label {
        display: inline-block;
        background-color: #FFFFFF;
        color: #333;
        border-radius: 10px;
    }
    .stTextArea > div > div > textarea {
        background-color: #FFFFFF;
        border-color: #CCCCCC;
    }
    button.css-2trqyj {
        background-color: #007BFF; /* ボタンの基本色 */
        color: #FFFFFF;
        border: none;
        border-radius: 5px;
        padding: 10px 24px;
        font-size: 16px;
        font-weight: bold;
        transition: background-color 0.3s, box-shadow 0.3s;
    }
    button.css-2trqyj:hover {
        background-color: #0056b3; /* ホバー時の色 */
        box-shadow: 0 2px 10px 0 rgba(0,123,255,0.5); /* ホバー時の影 */
    }
</style>
""", unsafe_allow_html=True)

# 業界のテキスト入力
industry = st.text_input("業界と業種を入力してください（片方だけでも可）", "", placeholder="広告業界・人材業界｜営業職・事務職")

# 添削内容選択
content_type = st.radio(
    "添削内容選択",
    options=['自己PR', '志望動機', 'ガクチカ', '長所短所'],
    horizontal=True
)

# 内容入力エリア
content = st.text_area("こちらに内容を入力してください", height=300)


# 添削するボタン
if st.button('添削する'):
    if content:
        # テキスト生成
        question_text = f"{industry}の{content_type}として、以下の内容を添削してください。\n\n点数100点満点中採点をして、改善案を３つ提示してその改善案を反映した{content_type}を教えてください。\n\n{content}。"
        response = model.generate_content(question_text)
        st.write("添削結果:", response.text)
    else:
        st.error('内容を入力してください。')
