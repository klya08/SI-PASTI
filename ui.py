# ==========================================
# KUA DIGITAL UI (PRESENTATION ONLY)
# ==========================================

def inject_tailwind_and_fonts():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        :root { --kua-green: #166534; --kua-dark: #14532d; --kua-emerald: #059669; --kua-soft: #dcfce7; --kua-bg: #f8fafc; --kua-text: #1e293b; --kua-muted: #64748b; --kua-border: #e2e8f0; }
        html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; color: var(--kua-text); }
        .stApp { background: #f0fdf4 !important; }
        /* Override form login streamlit-authenticator */
        [data-testid="stForm"] { background: #ffffff !important; border: 1px solid #bbf7d0 !important; border-radius: 18px !important; box-shadow: 0 12px 30px rgba(22, 101, 52, .08) !important; padding: 1.5rem !important; }
        [data-testid="stTextInput"] input, .stTextInput input { background: #ffffff !important; border: 1px solid #86efac !important; border-radius: 10px !important; color: #14532d !important; }
        [data-testid="stTextInput"] input:focus, .stTextInput input:focus { border-color: #059669 !important; box-shadow: 0 0 0 2px rgba(5, 150, 105, .18) !important; outline: none !important; }
        [data-testid="stForm"] .stButton > button, [data-testid="stForm"] button[kind="primary"], .stButton > button[kind="primary"] { background: #059669 !important; border: 1px solid #059669 !important; border-radius: 10px !important; color: #ffffff !important; font-weight: 700 !important; }
        [data-testid="stForm"] .stButton > button:hover, [data-testid="stForm"] button[kind="primary"]:hover, .stButton > button[kind="primary"]:hover { background: #047857 !important; border-color: #047857 !important; color: #ffffff !important; }
        [data-testid="stAlert"]:has(svg[data-testid="stAlertIconInfo"]), [data-baseweb="notification"] { background: #ecfdf5 !important; border: 1px solid #86efac !important; border-radius: 10px !important; color: #14532d !important; }
        [data-testid="stAlert"]:has(svg[data-testid="stAlertIconInfo"]) p, [data-baseweb="notification"] p { color: #14532d !important; }
        [data-testid="stSidebar"] { background: #fff; border-right: 1px solid var(--kua-border); }
        [data-testid="stSidebar"] > div:first-child { padding: 1.25rem 1rem; }
        [data-testid="stSidebar"] .stButton > button { width: 100%; justify-content: flex-start; }
        .block-container { max-width: 1440px; padding: 2.25rem 3rem 3rem; }
        .kua-brand { padding: .2rem .25rem 1.5rem; border-bottom: 1px solid var(--kua-border); margin-bottom: 1.35rem; }
        .kua-brand-mark, .kua-hero-mark { display: inline-flex; align-items: center; justify-content: center; background: var(--kua-green); color: white; border-radius: 12px; font-size: 1.45rem; font-weight: 700; }
        .kua-brand-mark { width: 42px; height: 42px; margin-bottom: .8rem; }
        .kua-brand-title { color: var(--kua-dark); font-size: 1rem; font-weight: 700; letter-spacing: .04em; margin: 0; }
        .kua-brand-subtitle, .kua-profile-status { color: var(--kua-muted); font-size: .72rem; margin: .25rem 0 0; }
        .kua-profile { display: flex; gap: .75rem; align-items: center; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 14px; padding: .8rem; margin: 0 0 1.35rem; }
        .kua-avatar { width: 35px; height: 35px; display: grid; place-items: center; border-radius: 50%; background: var(--kua-soft); color: var(--kua-green); font-weight: 700; }
        .kua-profile-name { color: var(--kua-dark); font-size: .82rem; font-weight: 600; margin: 0; }
        .kua-online { color: var(--kua-emerald); font-size: .7rem; font-weight: 600; margin-left: .2rem; }
        .kua-sidebar-label { color: var(--kua-muted); font-size: .68rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; margin: 1.25rem .25rem .55rem; }
        .kua-side-note { color: var(--kua-muted); background: var(--kua-bg); border: 1px solid var(--kua-border); border-radius: 12px; padding: .8rem; font-size: .74rem; line-height: 1.5; }
        .kua-banner { display: flex; align-items: center; gap: 1.1rem; background: #fff; border: 1px solid #bbf7d0; border-left: 5px solid var(--kua-green); border-radius: 18px; padding: 1.5rem 1.7rem; margin-bottom: 1.5rem; box-shadow: 0 8px 24px rgba(15, 23, 42, .05); }
        .kua-hero-mark { width: 58px; height: 58px; font-size: 1.8rem; flex: 0 0 auto; }
        .kua-eyebrow { color: var(--kua-emerald); font-size: .7rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; margin: 0 0 .35rem; }
        .kua-title { color: var(--kua-dark); font-size: clamp(1.45rem, 2.5vw, 2rem); font-weight: 700; line-height: 1.2; margin: 0; }
        .kua-subtitle { color: var(--kua-muted); font-size: .9rem; margin: .45rem 0 0; }
        .kua-status { color: var(--kua-emerald); font-size: .72rem; font-weight: 600; margin-top: .75rem; }
        .kua-status::before { content: '●'; margin-right: .35rem; }
        .kua-section-title { color: var(--kua-dark); font-size: 1.15rem; font-weight: 700; margin: 1.4rem 0 .25rem; }
        .kua-section-caption { color: var(--kua-muted); font-size: .82rem; margin: 0 0 1rem; }
        .kua-stepper { display: flex; gap: .45rem; align-items: center; margin: .3rem 0 1.5rem; color: #94a3b8; font-size: .74rem; font-weight: 600; }
        .kua-step { display: flex; align-items: center; gap: .35rem; white-space: nowrap; }
        .kua-step.active { color: var(--kua-green); }
        .kua-step-number { display: grid; place-items: center; width: 25px; height: 25px; border: 1px solid #cbd5e1; border-radius: 50%; }
        .kua-step.active .kua-step-number { background: var(--kua-green); border-color: var(--kua-green); color: white; }
        .kua-step-line { height: 1px; flex: 1; min-width: 18px; background: #cbd5e1; }
        .kua-panel { background: #fff; border: 1px solid var(--kua-border); border-radius: 16px; padding: 1.35rem; box-shadow: 0 5px 20px rgba(15, 23, 42, .035); }
        .kua-panel-head { display: flex; gap: .75rem; align-items: flex-start; margin-bottom: 1rem; }
        .kua-step-badge { display: grid; place-items: center; width: 34px; height: 34px; border-radius: 10px; background: var(--kua-soft); color: var(--kua-green); font-weight: 700; font-size: .78rem; }
        .kua-panel-title { color: var(--kua-dark); font-weight: 700; margin: 0; font-size: 1rem; }
        .kua-panel-copy { color: var(--kua-muted); margin: .25rem 0 0; font-size: .78rem; }
        .kua-help { color: var(--kua-muted); font-size: .72rem; margin: -.55rem 0 1rem; }
        .kua-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 1rem; margin: .75rem 0 1.5rem; }
        .kua-card { background: #fff; border: 1px solid var(--kua-border); border-radius: 14px; padding: 1.15rem 1.25rem; box-shadow: 0 5px 18px rgba(15, 23, 42, .035); position: relative; overflow: hidden; transition: transform .2s, box-shadow .2s; }
        .kua-card:hover { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(15, 23, 42, .07); }
        .kua-accent-green, .kua-accent-red, .kua-accent-yellow, .kua-accent-slate { position: absolute; left: 0; top: 0; bottom: 0; width: 4px; }
        .kua-accent-green { background: var(--kua-emerald); } .kua-accent-red { background: #e11d48; } .kua-accent-yellow { background: #d97706; } .kua-accent-slate { background: #94a3b8; }
        .kua-metric-title { font-size: .7rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; margin: 0 0 .45rem; }
        .text-slate { color: var(--kua-muted); } .text-green { color: var(--kua-emerald); } .text-red { color: #be123c; } .text-yellow { color: #b45309; }
        .kua-metric-val { color: var(--kua-dark); font-size: 1.75rem; font-weight: 700; margin: 0; }
        .kua-divider { width: 100%; height: 1px; background: var(--kua-border); margin: 1.6rem 0; }
        .stButton > button, .stDownloadButton > button { border-radius: 10px; min-height: 2.55rem; font-weight: 600; transition: transform .2s, box-shadow .2s, border-color .2s; }
        .stButton > button:hover, .stDownloadButton > button:hover { transform: translateY(-1px); box-shadow: 0 5px 14px rgba(22, 101, 52, .15); }
        [data-testid="stFileUploaderDropzone"] { border: 1px dashed #86efac; border-radius: 12px; background: #f0fdf4; }
        [data-testid="stFileUploaderDropzone"]:hover { border-color: var(--kua-emerald); background: #ecfdf5; }
        [data-testid="stTextInput"] input { border-radius: 10px; }
        @media (max-width: 700px) { .block-container { padding: 1.25rem 1rem 2rem; } .kua-banner { padding: 1.1rem; } .kua-hero-mark { width: 46px; height: 46px; font-size: 1.4rem; } .kua-stepper { overflow-x: auto; padding-bottom: .35rem; } .kua-step-line { min-width: 10px; } }
    </style>
    """

def render_sidebar_brand():
    return """
    <div class="kua-brand">
        <div class="kua-brand-mark">▤</div>
        <p class="kua-brand-title">KUA DIGITAL ARCHIVE</p>
        <p class="kua-brand-subtitle">Sistem Digitalisasi Arsip Nikah</p>
    </div>
    """

def render_user_profile(name):
    return f"""
    <div class="kua-profile">
        <div class="kua-avatar">{str(name)[:1].upper()}</div>
        <div><p class="kua-profile-name">{name}</p><p class="kua-profile-status">Petugas KUA <span class="kua-online">● Online</span></p></div>
    </div>
    """

def render_stepper(current_step=1):
    # Fungsi kecil untuk menentukan apakah kelas 'active' perlu ditambahkan
    def active_cls(step):
        return " active" if current_step >= step else ""

    # Menggunakan CSS Stepper dari desainmu secara dinamis
    return f"""
    <div class="kua-stepper">
        <div class="kua-step{active_cls(1)}"><span class="kua-step-number">01</span><span>Upload Data</span></div>
        <span class="kua-step-line"></span>
        <div class="kua-step{active_cls(2)}"><span class="kua-step-number">02</span><span>Pencocokan</span></div>
        <span class="kua-step-line"></span>
        <div class="kua-step{active_cls(3)}"><span class="kua-step-number">03</span><span>Review</span></div>
        <span class="kua-step-line"></span>
        <div class="kua-step{active_cls(4)}"><span class="kua-step-number">04</span><span>Selesai</span></div>
    </div>
    """

def render_header():
    return """
    <div class="kua-banner"><div class="kua-hero-mark">▤</div><div><p class="kua-eyebrow">KUA Digital Service</p><h1 class="kua-title">Digitalisasi Arsip Akta Nikah KUA</h1><p class="kua-subtitle">Sistem digital untuk pencocokan arsip nikah dengan data Excel dan Google Drive.</p><p class="kua-status">Sistem aktif dan siap digunakan</p></div></div>
    """

def render_divider():
    return '<div class="kua-divider"></div>'

def render_metrics(tot_data, tot_match, tot_notfound, tot_ambigu):
    return f"""
    <div class="kua-grid"><div class="kua-card"><div class="kua-accent-slate"></div><p class="kua-metric-title text-slate">Total Data</p><p class="kua-metric-val">{tot_data}</p></div><div class="kua-card"><div class="kua-accent-green"></div><p class="kua-metric-title text-green">Matched</p><p class="kua-metric-val">{tot_match}</p></div><div class="kua-card"><div class="kua-accent-red"></div><p class="kua-metric-title text-red">Not Found</p><p class="kua-metric-val">{tot_notfound}</p></div><div class="kua-card"><div class="kua-accent-yellow"></div><p class="kua-metric-title text-yellow">Ambiguous</p><p class="kua-metric-val">{tot_ambigu}</p></div></div>
    """