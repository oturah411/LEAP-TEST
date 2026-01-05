import streamlit as st
import csv
import random

st.set_page_config(page_title="英単語クイズ", page_icon="📘")
st.title("📘 日本語 → 英語クイズ（LEAP対応）")

# ============================
# CSV読み込み
# ============================
uploaded_file = st.file_uploader(
    "単語CSV（LEAP形式）をアップロードしてください",
    type="csv"
)

if uploaded_file:
    words = []
    reader = csv.DictReader(uploaded_file.read().decode("utf-8").splitlines())

    for row in reader:
        try:
            no = int(row["番号"])
            jp = row["意味"].strip()
            eng = row["単語"].strip()
            if jp and eng:
                words.append((no, jp, eng))
        except:
            continue

    st.success(f"{len(words)}語 読み込みました")

    # ============================
    # 出題範囲
    # ============================
    min_no = min(w[0] for w in words)
    max_no = max(w[0] for w in words)

    start_no, end_no = st.slider(
        "出題範囲を選択",
        min_value=min_no,
        max_value=max_no,
        value=(min_no, max_no)
    )

    filtered = [w for w in words if start_no <= w[0] <= end_no]

    st.write(f"出題候補：{len(filtered)}語")

    # ============================
    # 問題数選択
    # ============================
    num_questions = st.radio(
        "問題数を選択",
        [3, 5, 10],
        horizontal=True
    )

    # ============================
    # セッション初期化
    # ============================
    if "index" not in st.session_state:
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.questions = []

    # ============================
    # クイズ開始
    # ============================
    if st.button("クイズ開始"):
        if len(filtered) < num_questions:
            st.error("出題範囲内の単語数が足りません")
        else:
            st.session_state.questions = random.sample(filtered, num_questions)
            st.session_state.index = 0
            st.session_state.score = 0

    # ============================
    # 出題
    # ============================
    if st.session_state.questions:
        no, jp, eng = st.session_state.questions[st.session_state.index]

        st.subheader(f"問題 {st.session_state.index + 1} / {num_questions}")
        st.markdown(f"### {jp}")

        answer = st.text_input("英単語を入力", key=f"ans_{st.session_state.index}")

        if st.button("回答"):
            if answer.strip().lower() == eng.lower():
                st.success("◎ 正解！")
                st.session_state.score += 1
            else:
                st.error(f"× 不正解：**{eng}**")

            st.session_state.index += 1

            if st.session_state.index >= num_questions:
                st.balloons()
                st.markdown(
                    f"## 🎉 結果：{st.session_state.score} / {num_questions} 正解"
                )
                st.session_state.questions = []
