import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gemini_client import generate
from prompts.social_media import SOCIAL_PROMPT

PLATFORM_KEYS = ["Twitter/X", "LinkedIn", "Instagram"]

st.header("SNS投稿生成")
st.caption("トピックや既存コンテンツをもとに、各SNS向けの投稿文を生成します。")

input_type = st.radio("入力タイプ", ["トピック・アイデア", "既存コンテンツを流用"], horizontal=True)
content = st.text_area(
    "トピックまたはコンテンツ" if input_type == "トピック・アイデア" else "流用したいコンテンツ",
    height=150,
    placeholder="例: 朝のルーティンを変えたら生産性が3倍になった話" if input_type == "トピック・アイデア"
    else "ここに既存の文章を貼り付けてください..."
)

platforms = st.multiselect("生成するプラットフォーム", PLATFORM_KEYS, default=PLATFORM_KEYS)

col1, col2 = st.columns(2)
with col1:
    include_hashtags = st.toggle("ハッシュタグを含める", value=True)
with col2:
    include_emoji = st.toggle("絵文字を含める", value=True)

if st.button("投稿文を生成", type="primary"):
    if not content.strip():
        st.warning("コンテンツを入力してください。")
    elif not platforms:
        st.warning("プラットフォームを1つ以上選択してください。")
    else:
        results = {}
        with st.spinner("生成中..."):
            for platform in platforms:
                prompt = SOCIAL_PROMPT.format(
                    platform=platform,
                    content=content,
                    hashtags="含める" if include_hashtags else "含めない",
                    emoji="含める" if include_emoji else "含めない",
                )
                try:
                    results[platform] = generate(prompt, temperature=0.85)
                except Exception as e:
                    results[platform] = f"エラー: {e}"

        st.success("完了！")
        st.divider()
        tabs = st.tabs(platforms)
        for tab, platform in zip(tabs, platforms):
            with tab:
                post_text = results[platform]
                char_count = len(post_text)
                st.caption(f"文字数: {char_count}")
                if platform == "Twitter/X" and char_count > 280:
                    st.warning(f"280文字を超えています（{char_count}文字）。投稿前に編集してください。")
                st.text_area("投稿文（編集可能）", value=post_text, height=150,
                             key=f"post_{platform}", label_visibility="collapsed")
