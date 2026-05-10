"""
cookie_popup/gdpr_cookie.py
============================

GDPR-compliant Cookie Consent module for Streamlit applications.

This module provides :func:`show_cookie_banner` — a ready-to-use banner
that asks users for cookie consent and persists their choice using
Streamlit's session state.

Cookie categories supported:

* **Strictly Necessary** — always enabled (cannot be declined)
* **Analytics** — optional, opt-in only
* **Preferences** — optional, opt-in only

Usage::

    from cookie_popup.gdpr_cookie import show_cookie_banner, get_consent

    show_cookie_banner()

    consent = get_consent()
    if consent["analytics"]:
        # run analytics code
        pass
"""

from __future__ import annotations

import streamlit as st


# ---------------------------------------------------------------------------
# Session-state keys
# ---------------------------------------------------------------------------

_KEY_SHOWN    = "_gdpr_banner_shown"
_KEY_ANALYTICS = "_gdpr_analytics"
_KEY_PREFS    = "_gdpr_preferences"
_KEY_DECIDED  = "_gdpr_decided"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def show_cookie_banner() -> None:
    """Display a GDPR-compliant cookie consent banner.

    The banner is shown **once per session** (until the user makes a choice).
    After the user clicks *Accept All*, *Accept Selected*, or *Reject All*,
    their preferences are stored in ``st.session_state`` and the banner
    is hidden for the remainder of the session.

    The banner renders at the **bottom of the viewport** using
    ``st.markdown`` with injected CSS and a Streamlit ``st.container``.

    Example::

        import streamlit as st
        from cookie_popup.gdpr_cookie import show_cookie_banner

        st.title("My App")
        show_cookie_banner()
    """
    # Initialise state
    if _KEY_DECIDED not in st.session_state:
        st.session_state[_KEY_DECIDED]  = False
    if _KEY_ANALYTICS not in st.session_state:
        st.session_state[_KEY_ANALYTICS] = False
    if _KEY_PREFS not in st.session_state:
        st.session_state[_KEY_PREFS] = False

    # Already decided — nothing to show
    if st.session_state[_KEY_DECIDED]:
        return

    # ------------------------------------------------------------------ #
    #  Banner styling                                                      #
    # ------------------------------------------------------------------ #
    st.markdown(
        """
        <style>
        .gdpr-banner {
            background: #1e1e1e;
            color: #f0f0f0;
            border-radius: 12px 12px 0 0;
            padding: 20px 28px 16px 28px;
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
            line-height: 1.6;
            border-top: 3px solid #4f9cf9;
        }
        .gdpr-banner h4 {
            margin: 0 0 8px 0;
            font-size: 1.05em;
            color: #fff;
        }
        .gdpr-banner a {
            color: #4f9cf9;
        }
        </style>
        <div class="gdpr-banner">
            <h4>🍪 We use cookies</h4>
            <p>
                This website uses cookies to improve your experience and comply with
                <strong>GDPR</strong> (EU) 2016/679.
                Strictly necessary cookies are always active.
                You can choose which optional cookies to accept below.
                For more information, see our
                <a href="PRIVACY_POLICY.md" target="_blank">Privacy Policy</a>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------------ #
    #  Controls                                                           #
    # ------------------------------------------------------------------ #
    with st.container():
        col_check, col_btns = st.columns([2, 3])

        with col_check:
            st.checkbox("✅ Strictly necessary *(always on)*", value=True, disabled=True,
                        key="_gdpr_necessary_display")
            analytics_val = st.checkbox("📊 Analytics cookies", value=False,
                                        key="_gdpr_analytics_check")
            prefs_val     = st.checkbox("⚙️  Preferences cookies", value=False,
                                        key="_gdpr_prefs_check")

        with col_btns:
            st.write("")  # spacing
            b1, b2, b3 = st.columns(3)
            accept_all      = b1.button("✅ Accept All",      use_container_width=True)
            accept_selected = b2.button("💾 Save Selection",  use_container_width=True)
            reject_all      = b3.button("❌ Reject All",      use_container_width=True)

    if accept_all:
        _save_consent(analytics=True, preferences=True)
    elif accept_selected:
        _save_consent(analytics=analytics_val, preferences=prefs_val)
    elif reject_all:
        _save_consent(analytics=False, preferences=False)


def get_consent() -> dict[str, bool]:
    """Return the current cookie consent state.

    Returns:
        dict[str, bool]: A dictionary with three keys:

        * ``"necessary"`` — always ``True``
        * ``"analytics"`` — ``True`` if the user accepted analytics cookies
        * ``"preferences"`` — ``True`` if the user accepted preferences cookies

    Example::

        consent = get_consent()
        if consent["analytics"]:
            run_analytics()
    """
    return {
        "necessary":   True,
        "analytics":   st.session_state.get(_KEY_ANALYTICS, False),
        "preferences": st.session_state.get(_KEY_PREFS, False),
    }


def reset_consent() -> None:
    """Clear all stored consent decisions (for testing or settings UI).

    After calling this function the cookie banner will be shown again
    on the next Streamlit rerun.

    Example::

        if st.button("Reset cookie preferences"):
            reset_consent()
            st.rerun()
    """
    for key in (_KEY_DECIDED, _KEY_ANALYTICS, _KEY_PREFS):
        st.session_state.pop(key, None)


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _save_consent(*, analytics: bool, preferences: bool) -> None:
    """Persist consent decisions to session state and hide the banner.

    Args:
        analytics   (bool): Whether analytics cookies are accepted.
        preferences (bool): Whether preferences cookies are accepted.
    """
    st.session_state[_KEY_ANALYTICS] = analytics
    st.session_state[_KEY_PREFS]     = preferences
    st.session_state[_KEY_DECIDED]   = True
    st.rerun()
