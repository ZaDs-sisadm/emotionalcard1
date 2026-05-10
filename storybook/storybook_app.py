"""
storybook/storybook_app.py
==========================

EmotionalCards — Component Storybook
--------------------------------------

A Streamlit-based Storybook that showcases the two main components:

1. :class:`~components.card.Card`            — basic card component
2. :class:`~components.emotional_card.EmotionalCard` — complex emotion-aware card

Run with::

    streamlit run storybook/storybook_app.py
"""

import sys
import os
import datetime

# Allow imports from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st

from components.card import Card
from components.emotional_card import EmotionalCard, Emotion
from cookie_popup.gdpr_cookie import show_cookie_banner

# ============================================================
# Page config
# ============================================================

st.set_page_config(
    page_title="EmotionalCards Storybook",
    page_icon="📖",
    layout="wide",
)

# Show GDPR cookie banner first
show_cookie_banner()

# ============================================================
# Sidebar — navigation
# ============================================================

st.sidebar.title("📖 Storybook")
st.sidebar.markdown("---")
component = st.sidebar.radio(
    "Select component",
    ["🏠 Overview", "🃏 Card (Basic)", "🎭 EmotionalCard (Complex)"],
)

# ============================================================
# Overview page
# ============================================================

if component == "🏠 Overview":
    st.title("📖 EmotionalCards — Storybook")
    st.markdown(
        """
        Welcome to the **EmotionalCards Storybook** — a live component explorer
        for the EmotionalCards project.

        Use the **sidebar** to navigate between components.

        ---

        ### Components

        | Component | Type | Description |
        |-----------|------|-------------|
        | `Card` | Basic | A simple, configurable card with title, body and optional footer |
        | `EmotionalCard` | Complex | Emotion-aware card with emoji, intensity, tags, and buttons |

        ---

        ### How to use

        Each component page shows **2–3 story variations** with live property controls
        in the sidebar. Change the sliders and inputs to see how the component reacts.
        """
    )

# ============================================================
# BASIC COMPONENT — Card
# ============================================================

elif component == "🃏 Card (Basic)":

    st.title("🃏 Card — Basic Component")
    st.markdown(
        """
        `Card` is the foundational display element of EmotionalCards.
        It accepts a **title**, **body text**, a **background colour**, and an optional **footer**.

        **Properties:**
        - `title` (str) — heading text
        - `body` (str) — main content
        - `color` (str) — background colour
        - `text_color` (str) — text colour
        - `footer` (str | None) — optional footer
        - `elevation` (int 0–5) — shadow depth
        """
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Card Props")

    title      = st.sidebar.text_input("title",      value="Hello, World!")
    body       = st.sidebar.text_area("body",        value="This is a simple card component.")
    color      = st.sidebar.color_picker("color",    value="#ffffff")
    text_color = st.sidebar.color_picker("text_color", value="#333333")
    footer     = st.sidebar.text_input("footer (optional)", value="")
    elevation  = st.sidebar.slider("elevation", 0, 5, 2)

    st.markdown("---")

    # ----------------------------------------------------------
    # Story 1 — Default
    # ----------------------------------------------------------
    st.subheader("Story 1 — Default")
    st.markdown("A plain card with default white background and no footer.")

    Card(
        title="Default Card",
        body="This is a standard card with no footer.",
    ).render()

    st.markdown("---")

    # ----------------------------------------------------------
    # Story 2 — Coloured with footer
    # ----------------------------------------------------------
    st.subheader("Story 2 — Coloured with footer")
    st.markdown("Card with a custom background colour and footer text.")

    Card(
        title="Coloured Card",
        body="Cards support any CSS colour for the background.",
        color="#e8f5e9",
        footer="Created: May 2025",
        elevation=3,
    ).render()

    st.markdown("---")

    # ----------------------------------------------------------
    # Story 3 — Interactive (controlled by sidebar)
    # ----------------------------------------------------------
    st.subheader("Story 3 — ⚙️ Interactive (use sidebar controls)")
    st.markdown("Adjust the props in the sidebar to see the card update live.")

    Card(
        title=title,
        body=body,
        color=color,
        text_color=text_color,
        footer=footer if footer else None,
        elevation=elevation,
    ).render()

# ============================================================
# COMPLEX COMPONENT — EmotionalCard
# ============================================================

elif component == "🎭 EmotionalCard (Complex)":

    st.title("🎭 EmotionalCard — Complex Component")
    st.markdown(
        """
        `EmotionalCard` extends `Card` with:

        - **Emotion** — one of Joy, Sadness, Anger, Fear, Surprise, Disgust, Calm
        - **Intensity** — a 1–5 rating visualised as filled dots
        - **Tags** — keyword chips
        - **Timestamp** — creation time
        - **Like / Dislike** buttons (optional)
        """
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ EmotionalCard Props")

    emotion_name = st.sidebar.selectbox(
        "emotion",
        [e.name for e in Emotion],
        index=0,
    )
    emotion = Emotion[emotion_name]

    ec_title    = st.sidebar.text_input("title", value="A wonderful afternoon")
    ec_body     = st.sidebar.text_area(
        "body",
        value="The sun was bright and the air smelled of spring flowers.",
    )
    intensity   = st.sidebar.slider("intensity", 1, 5, 3)
    tags_raw    = st.sidebar.text_input("tags (comma-separated)", value="nature, spring")
    show_btns   = st.sidebar.checkbox("show_buttons", value=True)

    tags = [t.strip() for t in tags_raw.split(",") if t.strip()]

    st.markdown("---")

    # ----------------------------------------------------------
    # Story 1 — Joy (default example)
    # ----------------------------------------------------------
    st.subheader("Story 1 — Joy")
    st.markdown("A happy card with intensity 4 and tags.")

    EmotionalCard(
        emotion=Emotion.JOY,
        title="Best day of the week!",
        body="Had a great team meeting, finished a big feature, and the coffee was perfect.",
        intensity=4,
        tags=["work", "coffee", "teamwork"],
        timestamp=datetime.datetime(2025, 5, 10, 14, 30),
        show_buttons=True,
    ).render()

    st.markdown("---")

    # ----------------------------------------------------------
    # Story 2 — Sadness (minimal)
    # ----------------------------------------------------------
    st.subheader("Story 2 — Sadness (minimal)")
    st.markdown("A subdued card with low intensity and no tags or buttons.")

    EmotionalCard(
        emotion=Emotion.SADNESS,
        title="Missing old friends",
        body="Sometimes nostalgia hits out of nowhere. Just a quiet evening reflection.",
        intensity=2,
        show_buttons=False,
    ).render()

    st.markdown("---")

    # ----------------------------------------------------------
    # Story 3 — Interactive
    # ----------------------------------------------------------
    st.subheader("Story 3 — ⚙️ Interactive (use sidebar controls)")
    st.markdown("Adjust the props in the sidebar to see the card update live.")

    EmotionalCard(
        emotion=emotion,
        title=ec_title,
        body=ec_body,
        intensity=intensity,
        tags=tags,
        show_buttons=show_btns,
    ).render()
