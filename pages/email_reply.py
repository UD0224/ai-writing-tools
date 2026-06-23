import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gemini_client import generate
from prompts.email_reply import EMAIL_PROMPT

st.header("メール返信生成")
st.caption("元のメールを貼り付けると、返信文を自動で下書きします。")

original_email = st.text_area("元のメールを貼り付けてください", height=200,
                               placeholder="返信したいメールをここに貼り付けてください...")

col1, col2 = st.columns(2)
with col1:
    intent = st.selectbox("返信の意図", [
        "同意・承諾する", "断る・辞退する", "詳細情報を要求する",
        "お礼を伝える", "フォローアップする", "受領確認のみ"
    ])
with col2:
    tone = st.selectbox("トーン", [
        "丁寧・フォーマル", "フレンドリー・親しみやすい",
        "簡潔・ダイレクト", "外交的・穏やか"
    ])

name = st.text_input("署名（任意）", placeholder="例: 北田 勇大")

col_btn1, col_btn2 = st.columns([1, 5])
generate_btn = col_btn1.button("返信を生成", type="primary")
regen_btn = col_btn2.button("再生成")

if generate_btn or regen_btn:
    if not original_email.strip():
        st.warning("元のメールを入力してください。")
    else:
        with st.spinner("返信文を生成中..."):
            prompt = EMAIL_PROMPT.format(
                original_email=original_email,
                intent=intent,
                tone=tone,
                name=name if name.strip() else "（署名なし）"
            )
            try:
                result = generate(prompt, temperature=0.6)
            except Exception as e:
                st.error(f"APIエラー: {e}")
                st.stop()

        parts = result.split("\n", 1)
        subject_line = ""
        body = result
        if parts[0].startswith("Subject:"):
            subject_line = parts[0].replace("Subject:", "").strip()
            body = parts[1].strip() if len(parts) > 1 else ""

        st.success("完了！")
        if subject_line:
            st.info(f"**件名:** {subject_line}")
        st.divider()
        st.subheader("返信文（編集可能）")
        st.text_area("生成された返信", value=body, height=250, label_visibility="collapsed")
