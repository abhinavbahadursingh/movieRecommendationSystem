import streamlit as st
import pickle
import pandas as pd
import requests
import time

# ------------------- PAGE CONFIG -------------------
st.set_page_config(
    page_title="CineMatch // Neural Recommender",
    page_icon="⬡",
    layout="wide"
)

# ------------------- FUTURISTIC CSS -------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@300;400;500;600;700&family=Orbitron:wght@400;700;900&display=swap');

:root {
    --neon-cyan: #00f5ff;
    --neon-magenta: #ff006e;
    --neon-green: #39ff14;
    --dark-bg: #020408;
    --panel-bg: rgba(0, 245, 255, 0.03);
    --border-glow: rgba(0, 245, 255, 0.2);
    --text-primary: #e0f7fa;
    --text-muted: rgba(0, 245, 255, 0.5);
}

/* ---- GLOBAL RESET ---- */
html, body, .stApp {
    background-color: var(--dark-bg) !important;
    font-family: 'Rajdhani', sans-serif;
    color: var(--text-primary);
}

/* Animated hex grid background */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(circle at 20% 20%, rgba(0, 245, 255, 0.04) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(255, 0, 110, 0.04) 0%, transparent 50%),
        repeating-linear-gradient(
            0deg,
            transparent,
            transparent 60px,
            rgba(0, 245, 255, 0.02) 60px,
            rgba(0, 245, 255, 0.02) 61px
        ),
        repeating-linear-gradient(
            90deg,
            transparent,
            transparent 60px,
            rgba(0, 245, 255, 0.02) 60px,
            rgba(0, 245, 255, 0.02) 61px
        );
    pointer-events: none;
    z-index: 0;
}

/* ---- HEADER ---- */
.cyber-header {
    text-align: center;
    padding: 2.5rem 0 0.5rem;
    position: relative;
}

.cyber-logo {
    font-family: 'Orbitron', monospace;
    font-weight: 900;
    font-size: clamp(2.5rem, 6vw, 5rem);
    letter-spacing: 0.15em;
    color: transparent;
    background: linear-gradient(135deg, var(--neon-cyan) 0%, #7df9ff 40%, var(--neon-magenta) 100%);
    -webkit-background-clip: text;
    background-clip: text;
    text-shadow: none;
    filter: drop-shadow(0 0 30px rgba(0, 245, 255, 0.5));
    animation: logoFlicker 4s ease-in-out infinite;
    display: inline-block;
}

@keyframes logoFlicker {
    0%, 94%, 100% { opacity: 1; filter: drop-shadow(0 0 30px rgba(0, 245, 255, 0.5)); }
    95% { opacity: 0.85; filter: drop-shadow(0 0 50px rgba(0, 245, 255, 0.9)); }
    96% { opacity: 1; filter: drop-shadow(0 0 30px rgba(0, 245, 255, 0.5)); }
    97% { opacity: 0.9; filter: drop-shadow(0 0 45px rgba(0, 245, 255, 0.8)); }
}

.cyber-tagline {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.4em;
    color: var(--text-muted);
    margin-top: 0.25rem;
    text-transform: uppercase;
}

.cyber-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
    margin: 1.5rem auto;
    max-width: 600px;
    opacity: 0.4;
}

/* ---- SCANLINE BADGE ---- */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: var(--neon-green);
    border: 1px solid rgba(57, 255, 20, 0.3);
    padding: 0.25rem 0.75rem;
    background: rgba(57, 255, 20, 0.05);
    border-radius: 2px;
    margin-bottom: 2rem;
}

.status-dot {
    width: 6px;
    height: 6px;
    background: var(--neon-green);
    border-radius: 50%;
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 6px var(--neon-green); }
    50% { opacity: 0.4; box-shadow: none; }
}

/* ---- SELECTBOX / INPUT OVERRIDE ---- */
div[data-testid="stSelectbox"] > div {
    background: rgba(0, 245, 255, 0.04) !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 4px !important;
    transition: border-color 0.3s, box-shadow 0.3s;
}

div[data-testid="stSelectbox"] > div:focus-within {
    border-color: var(--neon-cyan) !important;
    box-shadow: 0 0 0 1px var(--neon-cyan), 0 0 20px rgba(0, 245, 255, 0.15) !important;
}

div[data-testid="stSelectbox"] label {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.3em !important;
    color: var(--text-muted) !important;
    text-transform: uppercase !important;
}

div[data-testid="stSelectbox"] svg {
    color: var(--neon-cyan) !important;
}

/* ---- BUTTON ---- */
div[data-testid="stButton"] > button {
    width: 100%;
    background: transparent !important;
    border: 1px solid var(--neon-cyan) !important;
    color: var(--neon-cyan) !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.3em !important;
    padding: 0.75rem 2rem !important;
    border-radius: 2px !important;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    text-transform: uppercase;
}

div[data-testid="stButton"] > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0, 245, 255, 0.1), transparent);
    transition: left 0.4s ease;
}

div[data-testid="stButton"] > button:hover::before {
    left: 100%;
}

div[data-testid="stButton"] > button:hover {
    background: rgba(0, 245, 255, 0.08) !important;
    box-shadow: 0 0 25px rgba(0, 245, 255, 0.3), inset 0 0 25px rgba(0, 245, 255, 0.05) !important;
    text-shadow: 0 0 10px var(--neon-cyan) !important;
}

div[data-testid="stButton"] > button:active {
    transform: scale(0.98);
}

/* ---- MOVIE CARDS ---- */
.movie-card {
    position: relative;
    background: var(--panel-bg);
    border: 1px solid var(--border-glow);
    border-radius: 4px;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
    margin-bottom: 0.5rem;
    animation: cardReveal 0.5s ease-out both;
}

@keyframes cardReveal {
    from { opacity: 0; transform: translateY(20px) scale(0.95); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}

.movie-card:nth-child(1) { animation-delay: 0.1s; }
.movie-card:nth-child(2) { animation-delay: 0.2s; }
.movie-card:nth-child(3) { animation-delay: 0.3s; }
.movie-card:nth-child(4) { animation-delay: 0.4s; }
.movie-card:nth-child(5) { animation-delay: 0.5s; }

.movie-card:hover {
    border-color: var(--neon-cyan);
    box-shadow:
        0 0 30px rgba(0, 245, 255, 0.15),
        inset 0 0 30px rgba(0, 245, 255, 0.03);
    transform: translateY(-6px) scale(1.02);
}

.movie-card:hover .scan-line {
    animation: scan 1.5s linear infinite;
}

.scan-line {
    position: absolute;
    top: -100%;
    left: 0;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
    opacity: 0;
    z-index: 10;
}

.movie-card:hover .scan-line {
    opacity: 1;
}

@keyframes scan {
    0% { top: -5%; }
    100% { top: 105%; }
}

.movie-poster {
    width: 100%;
    aspect-ratio: 2/3;
    object-fit: cover;
    display: block;
    filter: brightness(0.85) saturate(0.9);
    transition: filter 0.4s ease;
}

.movie-card:hover .movie-poster {
    filter: brightness(1) saturate(1.1);
}

.poster-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(2,4,8,0.95) 0%, transparent 55%);
    pointer-events: none;
}

.movie-title {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 1rem 0.75rem 0.75rem;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 600;
    font-size: 0.85rem;
    letter-spacing: 0.05em;
    color: #fff;
    line-height: 1.3;
    text-shadow: 0 0 10px rgba(0, 245, 255, 0.4);
}

.movie-id-tag {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.55rem;
    color: var(--neon-cyan);
    background: rgba(2, 4, 8, 0.7);
    border: 1px solid rgba(0, 245, 255, 0.3);
    padding: 0.15rem 0.35rem;
    border-radius: 2px;
    letter-spacing: 0.1em;
    backdrop-filter: blur(4px);
}

/* ---- RESULTS HEADER ---- */
.results-header {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.35em;
    color: var(--text-muted);
    text-transform: uppercase;
    padding: 1.5rem 0 1rem;
    border-top: 1px solid var(--border-glow);
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 1rem;
}

.results-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border-glow), transparent);
}

/* ---- SPINNER / STATUS ---- */
div[data-testid="stStatus"] {
    background: rgba(0, 245, 255, 0.03) !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 4px !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.75rem !important;
    color: var(--neon-cyan) !important;
}

/* ---- SCROLLBAR ---- */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--dark-bg); }
::-webkit-scrollbar-thumb { background: var(--border-glow); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--neon-cyan); }

/* ---- HIDE STREAMLIT CHROME ---- */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 1200px; }

/* ---- CORNER DECORATIONS ---- */
.corner-decor {
    position: fixed;
    width: 80px;
    height: 80px;
    pointer-events: none;
    opacity: 0.2;
    z-index: 999;
}
.corner-decor.tl { top: 1rem; left: 1rem; border-top: 1px solid var(--neon-cyan); border-left: 1px solid var(--neon-cyan); }
.corner-decor.tr { top: 1rem; right: 1rem; border-top: 1px solid var(--neon-cyan); border-right: 1px solid var(--neon-cyan); }
.corner-decor.bl { bottom: 1rem; left: 1rem; border-bottom: 1px solid var(--neon-cyan); border-left: 1px solid var(--neon-cyan); }
.corner-decor.br { bottom: 1rem; right: 1rem; border-bottom: 1px solid var(--neon-cyan); border-right: 1px solid var(--neon-cyan); }
</style>

<!-- Corner decorations -->
<div class="corner-decor tl"></div>
<div class="corner-decor tr"></div>
<div class="corner-decor bl"></div>
<div class="corner-decor br"></div>
""", unsafe_allow_html=True)

# ------------------- LOAD DATA -------------------
@st.cache_data
def load_data():
    movies = pickle.load(open('movie_list.pkl', 'rb'))
    if isinstance(movies, dict):
        movies = pd.DataFrame(movies)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

movies, similarity = load_data()

# ------------------- FETCH POSTER -------------------
OMDB_API_KEY = "edc2c471"

def fetch_poster(title):
    try:
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"
        data = requests.get(url, timeout=5).json()
        if data.get("Poster") and data["Poster"] != "N/A":
            return data["Poster"]
    except:
        pass
    return "https://via.placeholder.com/300x450/020408/00f5ff?text=NO+SIGNAL"

# ------------------- RECOMMEND FUNCTION -------------------
def recommend(movie_name):
    try:
        movie_index = movies[movies['title'] == movie_name].index[0]
        distances = similarity[movie_index]
        movie_indices = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]
        recommended_titles, recommended_posters = [], []
        for i in movie_indices:
            title = movies.iloc[i[0]].title
            recommended_titles.append(title)
            recommended_posters.append(fetch_poster(title))
        return recommended_titles, recommended_posters
    except Exception as e:
        return [], []

# ------------------- HEADER -------------------
st.markdown("""
<div class="cyber-header">
    <div class="cyber-logo">⬡ CINEMATCH</div>
    <div class="cyber-tagline">// Neural Collaborative Filtering Engine v2.4.1</div>
</div>
<div style="text-align:center;">
    <span class="status-badge">
        <span class="status-dot"></span>
        SYSTEM ONLINE · DATABASE SYNCHRONIZED · READY FOR QUERY
    </span>
</div>
""", unsafe_allow_html=True)

# ------------------- SESSION STATE (clear-on-click) -------------------
if "search_key" not in st.session_state:
    st.session_state.search_key = 0
if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None

# ------------------- SEARCH UI -------------------
_, col_mid, _ = st.columns([1, 2, 1])

with col_mid:
    st.markdown('<p style="font-family:\'Share Tech Mono\',monospace;font-size:0.6rem;letter-spacing:0.35em;color:rgba(0,245,255,0.5);text-transform:uppercase;margin-bottom:0.25rem;">⬡ NEURAL SEARCH INTERFACE</p>', unsafe_allow_html=True)

    # The key trick: incrementing the key resets the selectbox to index 0 (cleared)
    selected_movie = st.selectbox(
        "QUERY FILM DATABASE",
        options=[""] + list(movies['title'].values),
        index=0,
        key=f"movie_select_{st.session_state.search_key}",
        placeholder="Begin typing to scan database..."
    )
    st.session_state.selected_movie = selected_movie

    col_btn1, col_btn2 = st.columns([3, 1])
    with col_btn1:
        predict_button = st.button("⬡ INITIATE SEQUENCE", use_container_width=True)
    with col_btn2:
        clear_button = st.button("CLR", use_container_width=True)

# Handle clear
if clear_button:
    st.session_state.search_key += 1
    st.rerun()

# ------------------- RECOMMENDATIONS -------------------
if predict_button:
    if not selected_movie or selected_movie == "":
        st.warning("⚠ No target film specified. Please select a title to proceed.")
    else:
        with st.status("⬡ Engaging neural pathways...", expanded=True) as status:
            st.markdown('<span style="font-family:Share Tech Mono,monospace;font-size:0.7rem;color:#00f5ff;">› Scanning similarity matrix...</span>', unsafe_allow_html=True)
            names, posters = recommend(selected_movie)
            time.sleep(0.3)
            st.markdown('<span style="font-family:Share Tech Mono,monospace;font-size:0.7rem;color:#00f5ff;">› Fetching visual metadata from archive...</span>', unsafe_allow_html=True)
            time.sleep(0.4)
            st.markdown('<span style="font-family:Share Tech Mono,monospace;font-size:0.7rem;color:#39ff14;">› Sequence complete. 5 targets identified.</span>', unsafe_allow_html=True)
            status.update(label="⬡ ANALYSIS COMPLETE", state="complete", expanded=False)

        if not names:
            st.error("⚠ ERROR 404 — Film signature not found in neural matrix.")
        else:
            st.markdown(f"""
            <div class="results-header">
                ⬡ RECOMMENDED SEQUENCES FOR: <span style="color:#fff;letter-spacing:0.05em;">{selected_movie.upper()}</span>
            </div>
            """, unsafe_allow_html=True)

            cols = st.columns(5)
            for idx, (col, name, poster) in enumerate(zip(cols, names, posters)):
                with col:
                    st.markdown(f"""
                    <div class="movie-card" style="animation-delay:{(idx+1)*0.1}s">
                        <div class="scan-line"></div>
                        <img src="{poster}" class="movie-poster" alt="{name}">
                        <div class="poster-overlay"></div>
                        <div class="movie-id-tag">REC-{str(idx+1).zfill(3)}</div>
                        <div class="movie-title">{name}</div>
                    </div>
                    """, unsafe_allow_html=True)