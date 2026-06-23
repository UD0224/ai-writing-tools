import streamlit as st

st.set_page_config(page_title="AI Writing Tools", page_icon="✍️", layout="wide")

with st.sidebar:
    st.title("✍️ AI Writing Tools")
    st.caption("Powered by Gemini 2.5 Flash")
    st.divider()

pages = [
    st.Page("pages/blog_writer.py",     title="ブログライター",         icon=":material/article:"),
    st.Page("pages/email_reply.py",     title="メール返信",             icon=":material/mail:"),
    st.Page("pages/summarizer.py",      title="文章要約",               icon=":material/summarize:"),
    st.Page("pages/tone_rewriter.py",   title="トーン変換",             icon=":material/tune:"),
    st.Page("pages/social_media.py",    title="SNS投稿生成",            icon=":material/share:"),
    st.Page("pages/grammar_checker.py", title="文法・スタイルチェック", icon=":material/spellcheck:"),
]

pg = st.navigation(pages)
pg.run()
