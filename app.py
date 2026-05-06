import streamlit as st
import streamlit.components.v1 as components
from model import new_df, recommend

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    background-color: #0A0A0C;
    color: #F0EDE6;
    font-family: 'DM Sans', sans-serif;
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #111114; }
::-webkit-scrollbar-thumb { background: #C9A84C; border-radius: 3px; }

.hero {
    text-align: center;
    padding: 56px 20px 36px;
}

.hero-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: #C9A84C;
    margin-bottom: 18px;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(48px, 7vw, 88px);
    font-weight: 900;
    line-height: 1.0;
    color: #F0EDE6;
    margin-bottom: 20px;
    letter-spacing: -0.02em;
}

.hero-title span { color: #C9A84C; }

.hero-sub {
    font-size: 16px;
    color: #8A8479;
    font-weight: 300;
    max-width: 480px;
    margin: 0 auto 48px;
    line-height: 1.7;
}

.gold-rule {
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg, transparent, #C9A84C, transparent);
    margin: 0 auto 40px;
}

.controls-wrapper {
    background: #111114;
    border: 1px solid #1E1E24;
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 40px;
    box-shadow: 0 8px 40px rgba(0,0,0,0.6);
}

.control-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #C9A84C;
    margin-bottom: 8px;
}

[data-testid="stSelectbox"] > div > div {
    background-color: #18181C !important;
    border: 1px solid #2A2A32 !important;
    border-radius: 10px !important;
    color: #F0EDE6 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSelectbox"] > div > div:hover {
    border-color: #C9A84C !important;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #C9A84C 0%, #A8883A 100%);
    color: #0A0A0C;
    border: none;
    border-radius: 10px;
    height: 52px;
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 8px;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(201,168,76,0.35);
}

.section-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 24px;
}

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 26px;
    font-weight: 700;
    color: #F0EDE6;
    white-space: nowrap;
}

.section-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #2A2A32, transparent);
}

.section-count {
    font-size: 12px;
    color: #5A5852;
    white-space: nowrap;
}

.empty-state {
    text-align: center;
    padding: 80px 20px;
}

.empty-state-icon {
    font-size: 64px;
    margin-bottom: 20px;
    opacity: 0.25;
}

.empty-state-text {
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    color: #2E2C28;
}

.footer {
    text-align: center;
    padding: 48px 0 32px;
    font-size: 12px;
    color: #2E2C28;
    letter-spacing: 0.1em;
}

.footer span { color: #C9A84C; }

</style>
""", unsafe_allow_html=True)


# ---------------- HERO ---------------- #

st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">✦ Powered by TF-IDF & Cosine Similarity ✦</div>
    <div class="hero-title">Cine<span>Match</span></div>
    <div class="hero-sub">
        Discover films tailored to your taste. Select a movie, set your filters,
        and let the algorithm find your next obsession.
    </div>
    <div class="gold-rule"></div>
</div>
""", unsafe_allow_html=True)


# ---------------- CONTROLS ---------------- #

st.markdown('<div class="controls-wrapper">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([3, 1.5, 1.2])

with col1:
    st.markdown('<div class="control-label">Select a Movie</div>', unsafe_allow_html=True)
    selected_movie = st.selectbox("Movie", new_df['title'].values, label_visibility="collapsed")

with col2:
    genres = sorted(set(g for gl in new_df['genres'] for g in gl))
    st.markdown('<div class="control-label">Genre Filter</div>', unsafe_allow_html=True)
    selected_genre = st.selectbox("Genre", ["All Genres"] + genres, label_visibility="collapsed")

with col3:
    st.markdown('<div class="control-label">&nbsp;</div>', unsafe_allow_html=True)
    recommend_clicked = st.button("Find Films →")

st.markdown('</div>', unsafe_allow_html=True)


# ---------------- CAROUSEL BUILDER ---------------- #

def build_carousel(recommendations, movie_title):
    """Renders a fully self-contained HTML carousel injected into Streamlit."""

    cards_html = ""

    for movie in recommendations:
        poster = movie["poster"] or ""
        title  = movie["title"].replace("'", "&#39;")
        match  = movie["similarity"]
        overview = movie["overview"][:200].replace("'", "&#39;") + "…"

        try:
            rating = round(float(movie["rating"]), 1)
            rating_str = f"⭐ {rating}"
        except:
            rating_str = "N/A"

        year = str(movie["release_date"])[:4] if movie["release_date"] != "N/A" else "N/A"

        poster_block = (
            f'<img class="card-poster" src="{poster}" alt="{title}">'
            if poster else
            '<div class="card-no-poster">🎬</div>'
        )

        cards_html += f"""
        <div class="card">
            <div class="poster-wrap">
                {poster_block}
                <div class="badge-match">🔥 {match}%</div>
                <div class="badge-rating">{rating_str}</div>
                <div class="poster-fade"></div>
            </div>
            <div class="card-body">
                <div class="card-title">{title}</div>
                <div class="card-year">{year}</div>
                <div class="card-overview">{overview}</div>
            </div>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>

    * {{ margin: 0; padding: 0; box-sizing: border-box; }}

    body {{
        background: transparent;
        font-family: 'DM Sans', sans-serif;
        color: #F0EDE6;
        overflow-x: hidden;
    }}

    /* ── Section header ── */
    .header {{
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 28px;
        padding: 0 4px;
    }}

    .header-title {{
        font-family: 'Playfair Display', serif;
        font-size: 22px;
        font-weight: 700;
        color: #F0EDE6;
        white-space: nowrap;
    }}

    .header-title em {{ color: #C9A84C; font-style: italic; }}

    .header-line {{
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, #2A2A32, transparent);
    }}

    .header-count {{
        font-size: 11px;
        color: #5A5852;
        white-space: nowrap;
        letter-spacing: 0.08em;
    }}

    /* ── Arrow buttons ── */
    .nav-btn {{
        background: #18181C;
        border: 1px solid #2A2A32;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        cursor: pointer;
        color: #C9A84C;
        font-size: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;
        flex-shrink: 0;
        user-select: none;
    }}

    .nav-btn:hover {{
        background: #C9A84C;
        color: #0A0A0C;
        border-color: #C9A84C;
        box-shadow: 0 4px 16px rgba(201,168,76,0.4);
    }}

    .nav-btn:disabled {{
        opacity: 0.25;
        cursor: default;
    }}

    .nav-btn:disabled:hover {{
        background: #18181C;
        color: #C9A84C;
        border-color: #2A2A32;
        box-shadow: none;
    }}

    /* ── Carousel track ── */
    .carousel-wrapper {{
        display: flex;
        align-items: center;
        gap: 14px;
    }}

    .carousel-viewport {{
        flex: 1;
        overflow: hidden;
        border-radius: 14px;
    }}

    .carousel-track {{
        display: flex;
        gap: 16px;
        transition: transform 0.45s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        will-change: transform;
    }}

    /* ── Card ── */
    .card {{
        flex: 0 0 220px;
        background: #111114;
        border: 1px solid #1E1E24;
        border-radius: 14px;
        overflow: hidden;
        transition: border-color 0.3s ease, transform 0.35s cubic-bezier(0.25,0.46,0.45,0.94), box-shadow 0.35s ease;
        cursor: default;
    }}

    .card:hover {{
        border-color: #C9A84C;
        transform: translateY(-6px);
        box-shadow: 0 20px 48px rgba(0,0,0,0.7), 0 0 0 1px rgba(201,168,76,0.25);
    }}

    /* ── Poster ── */
    .poster-wrap {{
        position: relative;
        width: 100%;
        aspect-ratio: 2/3;
        background: #1A1A1E;
        overflow: hidden;
    }}

    .card-poster {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
        transition: transform 0.5s ease;
    }}

    .card:hover .card-poster {{ transform: scale(1.04); }}

    .card-no-poster {{
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 52px;
        background: linear-gradient(135deg, #111114, #1A1A1E);
    }}

    .poster-fade {{
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 60px;
        background: linear-gradient(transparent, #111114);
        pointer-events: none;
    }}

    /* ── Badges ── */
    .badge-match, .badge-rating {{
        position: absolute;
        top: 10px;
        border-radius: 20px;
        padding: 4px 10px;
        font-size: 11px;
        font-weight: 600;
        backdrop-filter: blur(8px);
    }}

    .badge-match {{
        right: 10px;
        background: rgba(10,10,12,0.85);
        border: 1px solid rgba(201,168,76,0.6);
        color: #C9A84C;
    }}

    .badge-rating {{
        left: 10px;
        background: rgba(10,10,12,0.85);
        border: 1px solid rgba(255,255,255,0.1);
        color: #FFD86B;
    }}

    /* ── Card body ── */
    .card-body {{ padding: 14px 16px 16px; }}

    .card-title {{
        font-family: 'Playfair Display', serif;
        font-size: 14px;
        font-weight: 700;
        color: #F0EDE6;
        line-height: 1.3;
        margin-bottom: 5px;
    }}

    .card-year {{
        font-size: 11px;
        color: #5A5852;
        font-weight: 500;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }}

    .card-overview {{
        font-size: 11.5px;
        color: #7A7570;
        line-height: 1.65;
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }}

    /* ── Dots ── */
    .dots {{
        display: flex;
        justify-content: center;
        gap: 8px;
        margin-top: 24px;
    }}

    .dot {{
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #2A2A32;
        cursor: pointer;
        transition: all 0.3s ease;
    }}

    .dot.active {{
        width: 24px;
        border-radius: 3px;
        background: #C9A84C;
    }}

    </style>
    </head>
    <body>

    <div class="header">
        <div class="header-title">Because you liked <em>{movie_title}</em></div>
        <div class="header-line"></div>
        <div class="header-count">{len(recommendations)} titles</div>
    </div>

    <div class="carousel-wrapper">
        <button class="nav-btn" id="prevBtn" onclick="slide(-1)" disabled>&#8592;</button>
        <div class="carousel-viewport" id="viewport">
            <div class="carousel-track" id="track">
                {cards_html}
            </div>
        </div>
        <button class="nav-btn" id="nextBtn" onclick="slide(1)">&#8594;</button>
    </div>

    <div class="dots" id="dots"></div>

    <script>
        const track    = document.getElementById('track');
        const prevBtn  = document.getElementById('prevBtn');
        const nextBtn  = document.getElementById('nextBtn');
        const dotsEl   = document.getElementById('dots');
        const viewport = document.getElementById('viewport');

        const CARD_W   = 220;
        const GAP      = 16;
        const STEP     = CARD_W + GAP;
        const total    = {len(recommendations)};

        let current = 0;

        function visibleCount() {{
            return Math.floor((viewport.offsetWidth + GAP) / STEP);
        }}

        function maxIndex() {{
            return Math.max(0, total - visibleCount());
        }}

        function buildDots() {{
            dotsEl.innerHTML = '';
            const pages = maxIndex() + 1;
            for (let i = 0; i < pages; i++) {{
                const d = document.createElement('div');
                d.className = 'dot' + (i === 0 ? ' active' : '');
                d.onclick = () => goTo(i);
                dotsEl.appendChild(d);
            }}
        }}

        function updateDots() {{
            document.querySelectorAll('.dot').forEach((d, i) => {{
                d.className = 'dot' + (i === current ? ' active' : '');
            }});
        }}

        function goTo(idx) {{
            current = Math.max(0, Math.min(idx, maxIndex()));
            track.style.transform = `translateX(-${{current * STEP}}px)`;
            prevBtn.disabled = current === 0;
            nextBtn.disabled = current >= maxIndex();
            updateDots();
        }}

        function slide(dir) {{
            goTo(current + dir);
        }}

        // keyboard nav
        document.addEventListener('keydown', e => {{
            if (e.key === 'ArrowRight') slide(1);
            if (e.key === 'ArrowLeft')  slide(-1);
        }});

        // touch swipe
        let touchStartX = 0;
        viewport.addEventListener('touchstart', e => {{ touchStartX = e.touches[0].clientX; }});
        viewport.addEventListener('touchend',   e => {{
            const diff = touchStartX - e.changedTouches[0].clientX;
            if (Math.abs(diff) > 40) slide(diff > 0 ? 1 : -1);
        }});

        // init
        buildDots();
        goTo(0);
        window.addEventListener('resize', () => {{ buildDots(); goTo(0); }});
    </script>

    </body>
    </html>
    """

    return html


# ---------------- RECOMMENDATIONS ---------------- #

if recommend_clicked:

    genre_filter = None if selected_genre == "All Genres" else selected_genre

    with st.spinner("Finding your films…"):
        recommendations = recommend(selected_movie, genre_filter)

    if recommendations:
        carousel_html = build_carousel(recommendations, selected_movie)
        # Height: poster(330) + card body(140) + header(60) + dots(50) + nav padding
        components.html(carousel_html, height=660, scrolling=False)

    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">🎭</div>
            <div class="empty-state-text">No matches found for this genre filter.</div>
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">🎬</div>
        <div class="empty-state-text">Your recommendations will appear here</div>
    </div>
    """, unsafe_allow_html=True)


# ---------------- FOOTER ---------------- #

st.markdown("""
<div class="footer">
    CINEMATCH &nbsp;·&nbsp; Built with <span>♦</span> using TMDB &nbsp;·&nbsp; TF-IDF Cosine Similarity Engine
</div>
""", unsafe_allow_html=True)