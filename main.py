import streamlit as st
import datetime
import sys
import os

# Дозволяємо імпорти з кореня проєкту
sys.path.insert(0, os.path.dirname(__file__))

from components.card import Card
from components.emotional_card import EmotionalCard, Emotion
from cookie_popup.gdpr_cookie import show_cookie_banner, get_consent

# ============================================================
# Конфігурація сторінки
# ============================================================

st.set_page_config(
    page_title="EmotionalCards",
    page_icon="🎴",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# GDPR Cookie Banner
# ============================================================

show_cookie_banner()

# ============================================================
# Sidebar — панель створення картки
# ============================================================

st.sidebar.title("🎴 EmotionalCards")
st.sidebar.markdown("Створи свою емоційну картку")
st.sidebar.markdown("---")

emotion_name = st.sidebar.selectbox(
    "Оберіть емоцію",
    [e.name for e in Emotion],
    format_func=lambda n: f"{Emotion[n].emoji}  {Emotion[n].label}",
)
emotion = Emotion[emotion_name]

title = st.sidebar.text_input("Заголовок картки", placeholder="Як ти себе почуваєш?")
body  = st.sidebar.text_area(
    "Опис",
    placeholder="Розкажи про свій стан...",
    height=120,
)
intensity = st.sidebar.slider("Інтенсивність", 1, 5, 3)
tags_raw  = st.sidebar.text_input("Теги (через кому)", placeholder="настрій, погода, робота")
show_btns = st.sidebar.checkbox("Показувати кнопки лайку", value=True)

add_card = st.sidebar.button("➕ Додати картку", use_container_width=True)

# ============================================================
# Session state — список карток
# ============================================================

if "cards" not in st.session_state:
    st.session_state["cards"] = []

if add_card:
    if not title.strip():
        st.sidebar.warning("Будь ласка, введіть заголовок картки.")
    else:
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
        st.session_state["cards"].append(
            EmotionalCard(
                emotion=emotion,
                title=title,
                body=body or "Без опису.",
                intensity=intensity,
                tags=tags,
                timestamp=datetime.datetime.now(),
                show_buttons=show_btns,
            )
        )
        st.rerun()

# ============================================================
# Головна сторінка
# ============================================================

st.title("🎴 EmotionalCards")
st.markdown("Твій щоденник емоцій — записуй, переглядай, рефлексуй.")
st.markdown("---")

consent = get_consent()
if consent["analytics"]:
    st.caption("📊 Аналітика увімкнена — дякуємо за підтримку!")

# Статистика
if st.session_state["cards"]:
    total     = len(st.session_state["cards"])
    avg_int   = sum(c.intensity for c in st.session_state["cards"]) / total
    top_emote = max(
        set(c.emotion for c in st.session_state["cards"]),
        key=lambda e: sum(1 for c in st.session_state["cards"] if c.emotion == e),
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("📝 Всього карток", total)
    col2.metric("📊 Середня інтенсивність", f"{avg_int:.1f} / 5")
    col3.metric("🏆 Топ-емоція", f"{top_emote.emoji} {top_emote.label}")
    st.markdown("---")

# Відображення карток
if not st.session_state["cards"]:
    st.info("Поки що немає карток. Створи першу за допомогою панелі зліва! 👈")
else:
    # Фільтр за емоцією
    all_emotions = list({c.emotion for c in st.session_state["cards"]})
    filter_options = ["Всі"] + [f"{e.emoji} {e.label}" for e in all_emotions]
    selected = st.selectbox("🔍 Фільтр за емоцією", filter_options)

    filtered = (
        st.session_state["cards"]
        if selected == "Всі"
        else [
            c for c in st.session_state["cards"]
            if f"{c.emotion.emoji} {c.emotion.label}" == selected
        ]
    )

    # Сортування — найновіші першими
    filtered_sorted = sorted(filtered, key=lambda c: c.timestamp, reverse=True)

    cols = st.columns(2)
    for i, card in enumerate(filtered_sorted):
        with cols[i % 2]:
            card.render()

    st.markdown("---")
    if st.button("🗑️ Очистити всі картки"):
        st.session_state["cards"] = []
        st.rerun()

# ============================================================
# Footer
# ============================================================

st.markdown(
    """
    <div style='text-align:center; color:#999; font-size:0.82em; margin-top:32px;'>
        EmotionalCards · Lab 1 · MIT License ·
        <a href='PRIVACY_POLICY.md' style='color:#4f9cf9;'>Політика конфіденційності</a>
    </div>
    """,
    unsafe_allow_html=True,
)
