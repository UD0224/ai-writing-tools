import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gemini_client import generate
from prompts.blog_writer import BLOG_PROMPT

st.header("ブログライター")
st.caption("トピックとキーワードを入力するだけで、完全なブログ記事を生成します。")

col_left, col_right = st.columns([1, 1])

with col_left:
    topic = st.text_input("トピック", placeholder="例: リモートワークの未来")
    keywords = st.text_input("キーワード（カンマ区切り）", placeholder="例: 生産性, 非同期, ツール")
    tone = st.selectbox("トーン", ["情報提供型", "会話調", "説得力のある", "主張型"])
    length = st.selectbox("目標文字数", ["短め（約400文字）", "普通（約800文字）", "長め（約1200文字）"])
    audience = st.selectbox("対象読者", ["一般読者", "ビジネスパーソン", "初心者", "エンジニア"])
    generate_btn = st.button("記事を生成する", type="primary")

with col_right:
    if generate_btn:
        if not topic.strip():
            st.warning("トピックを入力してください。")
        else:
            with st.spinner("記事を生成中..."):
                prompt = BLOG_PROMPT.format(
                    topic=topic, keywords=keywords or "なし",
                    tone=tone, length=length, audience=audience
                )
                try:
                    result = generate(prompt, temperature=0.8)
                except Exception as e:
                    st.error(f"APIエラー: {e}")
                    st.stop()

            parts = result.split("Meta:")
            article = parts[0].strip()
            meta = parts[1].strip() if len(parts) > 1 else ""

            if meta:
                st.info(f"**メタディスクリプション:** {meta}")

            st.download_button(
                label="テキストをダウンロード (.txt)",
                data=result,
                file_name="blog_post.txt",
                mime="text/plain",
            )
            st.divider()
            st.markdown(article)
