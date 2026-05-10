"""
components/card.py
==================

Base Card component for the EmotionalCards application.

This module defines the :class:`Card` — a simple, reusable UI card element
that can display a title, body text, and an optional footer.

Example usage::

    card = Card(title="Hello", body="World", color="#ffffff")
    card.render()
"""

from dataclasses import dataclass, field
from typing import Optional
import streamlit as st


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_BG_COLOR: str = "#ffffff"
DEFAULT_TEXT_COLOR: str = "#333333"
DEFAULT_BORDER_RADIUS: str = "12px"


# ---------------------------------------------------------------------------
# Card dataclass
# ---------------------------------------------------------------------------

@dataclass
class Card:
    """A simple, reusable card component.

    Attributes:
        title (str): The card's heading text.
        body (str): The main content / description text.
        color (str): Background colour in any valid CSS format (hex, rgb, named).
            Defaults to ``"#ffffff"``.
        text_color (str): Foreground text colour.
            Defaults to ``"#333333"``.
        footer (Optional[str]): Optional footer text shown at the bottom of the card.
            Defaults to ``None`` (no footer rendered).
        border_radius (str): CSS border-radius value.
            Defaults to ``"12px"``.
        elevation (int): Shadow intensity level (0–5).
            Defaults to ``2``.
    """

    title: str
    body: str
    color: str = DEFAULT_BG_COLOR
    text_color: str = DEFAULT_TEXT_COLOR
    footer: Optional[str] = None
    border_radius: str = DEFAULT_BORDER_RADIUS
    elevation: int = 2

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _shadow_css(self) -> str:
        """Return a CSS box-shadow string based on the elevation level.

        Returns:
            str: A CSS ``box-shadow`` value, e.g. ``"0 4px 8px rgba(0,0,0,0.12)"``.
        """
        spread = self.elevation * 4
        opacity = 0.06 + self.elevation * 0.03
        return f"0 {spread // 2}px {spread}px rgba(0,0,0,{opacity:.2f})"

    def _build_html(self) -> str:
        """Assemble the full HTML string for the card.

        Returns:
            str: An HTML snippet ready to be passed to ``st.markdown()``.
        """
        footer_html = (
            f'<div style="margin-top:12px; font-size:0.8em; color:{self.text_color}88;">'
            f"{self.footer}</div>"
            if self.footer
            else ""
        )

        return f"""
        <div style="
            background-color: {self.color};
            color: {self.text_color};
            border-radius: {self.border_radius};
            box-shadow: {self._shadow_css()};
            padding: 20px 24px;
            margin: 8px 0;
            font-family: 'Segoe UI', sans-serif;
        ">
            <h3 style="margin:0 0 8px 0; color:{self.text_color};">{self.title}</h3>
            <p  style="margin:0; line-height:1.6;">{self.body}</p>
            {footer_html}
        </div>
        """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def render(self) -> None:
        """Render the card inside the current Streamlit context.

        Calls ``st.markdown(..., unsafe_allow_html=True)`` with the card's HTML.

        Example::

            card = Card(title="Joy", body="Feeling great today!", color="#fffde7")
            card.render()
        """
        st.markdown(self._build_html(), unsafe_allow_html=True)

    def to_dict(self) -> dict:
        """Serialise the card's properties to a plain dictionary.

        Returns:
            dict: All card fields as key-value pairs.

        Example::

            card = Card(title="Test", body="Body text")
            data = card.to_dict()
            # {"title": "Test", "body": "Body text", "color": "#ffffff", ...}
        """
        return {
            "title": self.title,
            "body": self.body,
            "color": self.color,
            "text_color": self.text_color,
            "footer": self.footer,
            "border_radius": self.border_radius,
            "elevation": self.elevation,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Card":
        """Create a :class:`Card` instance from a dictionary.

        Args:
            data (dict): Dictionary with card properties. Unknown keys are ignored.

        Returns:
            Card: A new Card instance.

        Example::

            card = Card.from_dict({"title": "Hi", "body": "There"})
        """
        valid_keys = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
        filtered = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered)
