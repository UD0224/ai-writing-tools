import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gemini_client import generate
from prompts.summarizer import SUMMARY_PROMPT

st.header("文章要約")
st.caption("長い文章を指定した形式・長さ・観点で要約します。")

text = st.text_area("要約するテキストを貼り付けてください", height=300, max_chars=500000,
                    placeholder="ここにテキストを貼り付けてください...")

col1, col2, col3 = st.columns(3)
with col1:
    length = st.radio("要約の長さ", ["簡潔（2〜3文）", "標準（1段落）", "詳細（3〜4段落）"])
with col2:
    fmt = st.radio("出力形式", ["散文", "箇条書き", "混合（散文＋箇条書き）"])
with col3:
    focus = st.radio("重点", ["主要アイデア", "アクションアイテム", "事実・数値", "全般"])

if st.button("要約する", type="primary"):
    if not text.strip():
        st.warning("テキストを入力してください。")
    else:
        with st.spinner("要約中..."):
            prompt = SUMMARY_PROMPT.format(length=length, format=fmt, focus=focus, text=text)
            try:
                result = generate(prompt, temperature=0.3)
            except Exception as e:
                st.error(f"APIエラー: {e}")
                st.stop()

        st.success("完了！")
        col_a, col_b = st.columns(2)
        col_a.metric("元の文字数", f"{len(text):,} 文字")
        col_b.metric("要約後の文字数", f"{len(result):,} 文字")
        st.divider()
        st.subheader("要約結果")
        st.markdown(result)
