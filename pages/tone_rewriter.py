import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gemini_client import generate
from prompts.tone_rewriter import TONE_PROMPT

st.header("トーン変換")
st.caption("テキストのトーン（文体）を変換します。内容・事実はそのまま保持します。")

text = st.text_area("元のテキスト", height=200,
                    placeholder="トーンを変換したいテキストをここに貼り付けてください...")

col1, col2 = st.columns(2)
with col1:
    tone = st.selectbox("変換後のトーン", [
        "プロフェッショナル・フォーマル",
        "カジュアル・フレンドリー",
        "説得力のある",
        "共感的・温かみのある",
        "簡潔・ダイレクト",
        "ユーモラス"
    ])
with col2:
    preserve_structure = st.checkbox("見出し・リストなどの構造を保持する", value=True)

if st.button("変換する", type="primary"):
    if not text.strip():
        st.warning("テキストを入力してください。")
    else:
        structure_rule = (
            "見出し・箇条書き・リストなどの構造をそのまま保持する"
            if preserve_structure
            else "必要に応じて構造を変えても構わない"
        )
        with st.spinner("変換中..."):
            prompt = TONE_PROMPT.format(tone=tone, structure_rule=structure_rule, text=text)
            try:
                result = generate(prompt, temperature=0.7)
            except Exception as e:
                st.error(f"APIエラー: {e}")
                st.stop()

        st.success("完了！")
        st.divider()
        col_orig, col_new = st.columns(2)
        with col_orig:
            st.subheader("元のテキスト")
            st.markdown(text)
        with col_new:
            st.subheader(f"変換後（{tone}）")
            st.markdown(result)
