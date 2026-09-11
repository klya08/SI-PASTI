def inject_tailwind_and_fonts():
    return """<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

.stApp { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8fafc; color: #1f2937; }

/* KUNCI PERBAIKAN 1: Pangkas jarak atas bawaan Streamlit untuk Desktop */
.block-container { padding-top: 2rem !important; }

[data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e5e7eb; }
.sidebar-brand { display: flex; align-items: center; gap: 12px; padding: 10px 0 20px 0; margin-bottom: 20px; }
.sidebar-brand svg { width: 32px; height: 32px; color: #059669; flex-shrink: 0; }
.sidebar-brand-text { font-weight: 800; font-size: 16px; color: #064e3b; letter-spacing: 0.5px; line-height: 1.2; }
.sidebar-brand-sub { font-size: 12px; font-weight: 500; color: #6b7280; }

.sidebar-profile { background: #ffffff; border: 1px solid #e5e7eb; box-shadow: 0 2px 4px rgba(0,0,0,0.02); border-radius: 12px; padding: 16px; display: flex; align-items: center; gap: 12px; margin-bottom: 32px; transition: border-color 0.2s; }
.sidebar-profile:hover { border-color: #059669; }
.profile-avatar { width: 42px; height: 42px; border-radius: 50%; background: #ecfdf5; color: #059669; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 16px; flex-shrink: 0; }
.profile-info { display: flex; flex-direction: column; }
.profile-name { font-weight: 700; font-size: 14px; color: #111827; }
.profile-role { font-size: 12px; color: #6b7280; display: flex; align-items: center; gap: 6px; margin-top: 2px; }
.online-dot { width: 6px; height: 6px; background-color: #10b981; border-radius: 50%; }

.kua-sidebar-label { font-size: 11px; font-weight: 700; color: #9ca3af; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
.kua-side-note { font-size: 13px; color: #6b7280; line-height: 1.5; background: #f3f4f6; padding: 12px; border-radius: 8px; }

.hero-card { background: #ffffff; border-radius: 16px; padding: 24px 32px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03); border: 1px solid #e5e7eb; display: flex; align-items: center; justify-content: space-between; margin-bottom: 32px; }
.hero-content-left { display: flex; align-items: center; gap: 24px; }
.hero-icon-box { background: #ecfdf5; color: #059669; min-width: 64px; height: 64px; border-radius: 14px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.hero-title { font-size: 26px; font-weight: 800; color: #064e3b; margin: 0; line-height: 1.2; }
.hero-subtitle { font-size: 15px; color: #6b7280; margin: 6px 0 0 0; }
.status-badge { display: inline-flex; align-items: center; gap: 6px; background: #ecfdf5; color: #059669; font-size: 12px; font-weight: 600; padding: 6px 12px; border-radius: 999px; margin-top: 12px; border: 1px solid #a7f3d0; }
.status-dot { width: 8px; height: 8px; background-color: #10b981; border-radius: 50%; box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2); animation: pulse-dot 2s infinite; }
@keyframes pulse-dot { 0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); } 70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); } 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); } }

.stepper-container { display: flex; align-items: center; justify-content: space-between; margin-bottom: 40px; position: relative; padding: 0 10px; }
.stepper-line { position: absolute; top: 14px; left: 20px; right: 20px; height: 2px; background: #e5e7eb; z-index: 1; }
.step-item { position: relative; z-index: 2; display: flex; flex-direction: row; align-items: center; gap: 10px; background: #f8fafc; padding: 0 10px; }
.step-circle { width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 700; border: 2px solid #e5e7eb; background: #ffffff; color: #9ca3af; transition: all 0.3s ease; flex-shrink: 0; }
.step-label { font-size: 14px; font-weight: 600; color: #9ca3af; }
.step-item.active .step-circle { border-color: #059669; background: #059669; color: #ffffff; box-shadow: 0 0 0 4px #ecfdf5; }
.step-item.active .step-label { color: #064e3b; }
.step-item.completed .step-circle { border-color: #059669; background: #ffffff; color: #059669; }
.step-item.completed .step-label { color: #059669; }

.section-wrapper { background: #ffffff; border-radius: 16px; padding: 32px; border: 1px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-bottom: 24px; }
.section-header { margin-bottom: 24px; }
.section-title { font-size: 18px; font-weight: 700; color: #064e3b; margin: 0 0 6px 0; display: flex; align-items: center; gap: 8px; }
.section-caption { font-size: 14px; color: #6b7280; margin: 0; }

[data-testid="stFileUploadDropzone"] { background-color: #f9fafb !important; border: 2px dashed #cbd5e1 !important; border-radius: 12px !important; padding: 40px 20px !important; transition: all 0.2s ease; }
[data-testid="stFileUploadDropzone"]:hover { border-color: #059669 !important; background-color: #ecfdf5 !important; }
.stTextInput input { border-radius: 8px !important; border: 1px solid #d1d5db !important; padding: 12px 16px !important; font-size: 14px !important; box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important; transition: border-color 0.2s ease, box-shadow 0.2s ease; }
.stTextInput input:focus { border-color: #059669 !important; box-shadow: 0 0 0 3px #d1fae5 !important; }
.stButton button[kind="primary"] { background-color: #059669 !important; color: white !important; border-radius: 8px !important; font-weight: 600 !important; padding: 10px 24px !important; border: none !important; transition: transform 0.1s ease, background-color 0.2s ease !important; }
.stButton button[kind="primary"]:hover { background-color: #047857 !important; transform: translateY(-1px); box-shadow: 0 4px 6px -1px rgba(5, 150, 105, 0.2); }
[data-testid="stMetricValue"] { font-weight: 800 !important; color: #064e3b !important; }

/* ========================================= */
/* KUNCI PERBAIKAN 2: Pangkas lebih sadis di Layar HP */
/* ========================================= */
@media (max-width: 768px) {
    .block-container { padding-top: 1rem !important; }
    .hero-card { flex-direction: column; text-align: center; gap: 20px; padding: 24px 16px; margin-bottom: 24px; }
    .hero-content-left { flex-direction: column; text-align: center; gap: 16px; }
    .hero-icon-box { margin: 0 auto; }
    .hero-title { font-size: 22px; }
    .status-badge { justify-content: center; }
    
    .stepper-container { flex-wrap: wrap; justify-content: center; gap: 12px; margin-bottom: 24px; }
    .stepper-line { display: none; }
    .step-item { background: transparent; padding: 0; }
    
    .section-wrapper { padding: 20px 16px; }
}
</style>"""

def render_sidebar_brand():
    return """<div class="sidebar-brand">
<svg fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
<path d="M4 4h16v16H4V4zm2 4v2h12V8H6zm0 4v2h12v-2H6zm0 4v2h8v-2H6z"/>
</svg>
<div>
<div class="sidebar-brand-text">KUA DIGITAL ARCHIVE</div>
<div class="sidebar-brand-sub">Sistem Digitalisasi Nikah</div>
</div>
</div>"""

def render_user_profile(name):
    initial = name[0].upper() if name else "A"
    return f"""<div class="sidebar-profile">
<div class="profile-avatar">{initial}</div>
<div class="profile-info">
<span class="profile-name">{name}</span>
<span class="profile-role">
<div class="online-dot"></div> Petugas KUA
</span>
</div>
</div>"""

def render_header(img_base64=""):
    logo_html = f'<img src="data:image/png;base64,{img_base64}" width="100" style="opacity: 0.9;">' if img_base64 else ""
    return f"""<div class="hero-card">
<div class="hero-content-left">
<div class="hero-icon-box">
<svg width="32" height="32" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
<path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
</svg>
</div>
<div>
<h1 class="hero-title">Digitalisasi Arsip Akta Nikah KUA</h1>
<p class="hero-subtitle">Sistem digital untuk pencocokan arsip nikah dengan data Excel dan Google Drive.</p>
<div class="status-badge">
<div class="status-dot"></div> Sistem aktif dan siap digunakan
</div>
</div>
</div>
{logo_html}
</div>"""

def render_stepper(current_step):
    steps = [
        {"num": "01", "label": "Upload Data"},
        {"num": "02", "label": "Pencocokan"},
        {"num": "03", "label": "Review"},
        {"num": "04", "label": "Selesai"}
    ]
    
    html = '<div class="stepper-container"><div class="stepper-line"></div>'
    for i, step in enumerate(steps):
        step_val = i + 1
        status_class = "active" if step_val == current_step else "completed" if step_val < current_step else ""
        html += f'<div class="step-item {status_class}"><div class="step-circle">{step["num"]}</div><div class="step-label">{step["label"]}</div></div>'
    html += '</div>'
    return html

def render_divider():
    return '<hr style="border: 0; border-top: 1px solid #e5e7eb; margin: 32px 0;">'

def render_metrics(tot, match, notfound, ambigu):
    return ""