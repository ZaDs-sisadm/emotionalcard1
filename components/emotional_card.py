"""
components/emotional_card.py
============================

Complex **EmotionalCard** component for the EmotionalCards application.

An :class:`EmotionalCard` extends the base :class:`~components.card.Card` with:

* An emotion label and matching emoji
* An intensity slider (1–5)
* A timestamp
* Optional tags / keywords
* Interactive Like / Dislike buttons

Example usage::

    from components.emotional_card import EmotionalCard, Emotion

    ec = EmotionalCard(
        emotion=Emotion.JOY,
        title="A great day!",
        body="Today was sunny and productive.",
        intensity=4,
        tags=["nature", "work"],
    )
    ec.render()
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

import streamlit as st

from components.card import Card, DEFAULT_BORDER_RADIUS


# ---------------------------------------------------------------------------
# Emotion enum
# ---------------------------------------------------------------------------

class Emotion(str, Enum):
    """Enumeration of supported emotion types.

    Each member stores a ``(label, emoji, hex_colour)`` tuple as its value,
    which is used to style the card automatically.

    Members:
        JOY:       Positive emotion — bright yellow.
        SADNESS:   Negative emotion — muted blue.
        ANGER:     Intense negative emotion — vivid red.
        FEAR:      Cautious negative emotion — deep purple.
        SURPRISE:  Neutral/positive emotion — warm orange.
        DISGUST:   Negative emotion — olive green.
        CALM:      Positive emotion — soft teal.
    """

    JOY      = ("Joy",      "😊", "#FFF9C4")
    SADNESS  = ("Sadness",  "😢", "#BBDEFB")
    ANGER    = ("Anger",    "😡", "#FFCDD2")
    FEAR     = ("Fear",     "😨", "#E1BEE7")
    SURPRISE = ("Surprise", "😲", "#FFE0B2")
    DISGUST  = ("Disgust",  "🤢", "#DCEDC8")
    CALM     = ("Calm",     "😌", "#B2DFDB")

    # ------------------------------------------------------------------
    # Convenience properties
    # ------------------------------------------------------------------

    @property
    def label(self) -> str:
        """Human-readable emotion label (e.g. ``"Joy"``)."""
        return self.value[0]

    @property
    def emoji(self) -> str:
        """Unicode emoji for the emotion (e.g. ``"😊"``)."""
        return self.value[1]

    @property
    def color(self) -> str:
        """Background hex colour for the emotion (e.g. ``"#FFF9C4"``)."""
        return self.value[2]


# ---------------------------------------------------------------------------
# EmotionalCard dataclass
# ---------------------------------------------------------------------------

@dataclass
class EmotionalCard:
    """A rich, emotionally-aware card component.

    Extends the concept of :class:`~components.card.Card` with emotion
    metadata, intensity rating, tags, a timestamp, and interactive buttons.

    Attributes:
        emotion (Emotion): The primary emotion this card represents.
        title (str): Short headline for the card.
        body (str): Main descriptive text.
        intensity (int): Emotion intensity on a scale of 1 (mild) to 5 (extreme).
            Defaults to ``3``.
        tags (List[str]): Optional list of keyword tags.
            Defaults to an empty list.
        timestamp (datetime.datetime): Creation time of the card.
            Defaults to **now** (``datetime.datetime.now()``).
        show_buttons (bool): Whether to render Like / Dislike action buttons.
            Defaults to ``True``.
        border_radius (str): CSS border-radius value.
            Defaults to ``"12px"``.
    """

    emotion: Emotion
    title: str
    body: str
    intensity: int = 3
    tags: List[str] = field(default_factory=list)
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)
    show_buttons: bool = True
    border_radius: str = DEFAULT_BORDER_RADIUS

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _intensity_bar(self) -> str:
        """Build an HTML intensity indicator (filled dots).

        Returns:
            str: HTML string with 5 dots, filled up to ``self.intensity``.
        """
        dots = ""
        for i in range(1, 6):
            filled = self.intensity >= i
            color = "#555" if filled else "#ddd"
            dots += f'<span style="font-size:1.1em; color:{color};">●</span> '
        return dots

    def _tags_html(self) -> str:
        """Render tag chips as inline HTML spans.

        Returns:
            str: HTML string with badge-style chips for each tag, or ``""`` if no tags.
        """
        if not self.tags:
            return ""
        chips = " ".join(
            f'<span style="'
            f"background:{self.emotion.color}; "
            f"border:1px solid #aaa; "
            f"border-radius:20px; "
            f"padding:2px 10px; "
            f'font-size:0.78em; margin-right:4px;"'
            f">{tag}</span>"
            for tag in self.tags
        )
        return f'<div style="margin-top:10px;">{chips}</div>'

    def _build_html(self) -> str:
        """Assemble the complete HTML for the emotional card.

        Returns:
            str: Full HTML snippet for use with ``st.markdown(unsafe_allow_html=True)``.
        """
        ts = self.timestamp.strftime("%d %b %Y, %H:%M")
        return f"""
        <div style="
            background: {self.emotion.color};
            border-radius: {self.border_radius};
            box-shadow: 0 4px 12px rgba(0,0,0,0.10);
            padding: 20px 24px;
            margin: 10px 0;
            font-family: 'Segoe UI', sans-serif;
        ">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:2em;">{self.emotion.emoji}</span>
                <span style="font-size:0.78em; color:#666;">{ts}</span>
            </div>
            <div style="margin:4px 0 2px 0; font-weight:600; color:#555; font-size:0.85em;">
                {self.emotion.label} &nbsp;·&nbsp; Intensity: {self._intensity_bar()}
            </div>
            <h3 style="margin: 8px 0 4px 0; color:#222;">{self.title}</h3>
            <p  style="margin:0; line-height:1.6; color:#333;">{self.body}</p>
            {self._tags_html()}
        </div>
        """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def render(self) -> None:
        """Render the emotional card in the current Streamlit context.

        Also renders Like / Dislike buttons below the card if
        ``self.show_buttons`` is ``True``.

        Example::

            ec = EmotionalCard(emotion=Emotion.CALM, title="Zen", body="All good.")
            ec.render()
        """
        st.markdown(self._build_html(), unsafe_allow_html=True)

        if self.show_buttons:
            col1, col2, _ = st.columns([1, 1, 6])
            with col1:
                if st.button("👍 Like", key=f"like_{self.title}_{id(self)}"):
                    st.toast("You liked this card! ❤️")
            with col2:
                if st.button("👎", key=f"dislike_{self.title}_{id(self)}"):
                    st.toast("Feedback noted.")

    def to_base_card(self) -> Card:
        """Convert this :class:`EmotionalCard` to a plain :class:`~components.card.Card`.

        Useful when a simplified representation is needed.

        Returns:
            Card: A base card with the emotion's colour and a footer showing the emotion label.

        Example::

            ec = EmotionalCard(emotion=Emotion.JOY, title="Hi", body="There")
            simple = ec.to_base_card()
            simple.render()
        """
        return Card(
            title=f"{self.emotion.emoji} {self.title}",
            body=self.body,
            color=self.emotion.color,
            footer=f"Emotion: {self.emotion.label} | Intensity: {self.intensity}/5",
            border_radius=self.border_radius,
        )

    def to_dict(self) -> dict:
        """Serialise the card to a plain dictionary.

        Returns:
            dict: All fields as key-value pairs.
                  ``emotion`` is stored as its name string (e.g. ``"JOY"``).
                  ``timestamp`` is stored as an ISO-8601 string.
        """
        return {
            "emotion": self.emotion.name,
            "title": self.title,
            "body": self.body,
            "intensity": self.intensity,
            "tags": self.tags,
            "timestamp": self.timestamp.isoformat(),
            "show_buttons": self.show_buttons,
            "border_radius": self.border_radius,
        }
