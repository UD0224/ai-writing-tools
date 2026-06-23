import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gemini_client import generate
from prompts.grammar_checker import GRAMMAR_PROMPT

st.header("文法・スタイルチェック")
st.caption("テキストを貼り付けると、修正版と変更点の説明を並べて表示します。")

text = st.text_area("チェックするテキストを貼り付けてください", height=250,
                    placeholder="ここにテキストを貼り付けてください...")

checks = st.multiselect(
    "チェック項目",
    ["文法・スペル", "明確さ・簡潔さ", "受動態", "冗長な表現", "トーンの一貫性"],
    default=["文法・スペル", "明確さ・簡潔さ", "冗長な表現"]
)

if st.button("チェック・改善する", type="primary"):
    if not text.strip():
        st.warning("テキストを入力してください。")
    elif not checks:
        st.warning("チェック項目を1つ以上選択してください。")
    else:
        with st.spinner("チェック中..."):
            checks_str = "・".join(checks)
            prompt = GRAMMAR_PROMPT.format(checks=checks_str, text=text)
            try:
                result = generate(prompt, temperature=0.2)
            except Exception as e:
                st.error(f"APIエラー: {e}")
                st.stop()

        if "CHANGES:" in result:
            corrected_part, changes_part = result.split("CHANGES:", 1)
            corrected = corrected_part.replace("CORRECTED:", "").strip()
            changes = changes_part.strip()
        else:
            corrected = result
            changes = "変更点の詳細を取得できませんでした。"

        change_count = changes.count("\n1.") + changes.count("1.")
        lines = [l for l in changes.split("\n") if l.strip() and l.strip()[0].isdigit()]
        st.success("完了！")
        st.metric("指摘件数", f"{len(lines)} 件")
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("修正後のテキスト")
            st.markdown(corrected)
        with col2:
            st.subheader("変更点一覧")
            st.markdown(changes)
