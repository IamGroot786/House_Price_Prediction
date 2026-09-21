"""Reference-inspired landing page; prediction and shared sections stay in app.py."""
import streamlit as st

_STYLE = """
<style>
.hpp-landing {color:#111b2b;font-family:Arial,sans-serif;background:#fff;}
.hpp-landing * {box-sizing:border-box;}
.hpp-landing h1,.hpp-landing h2,.hpp-landing h3 {font-family:inherit;letter-spacing:-.045em;color:inherit;line-height:1.08;}
.hpp-landing p {font-size:15px;line-height:1.75;color:#697383;}
.hpp-eyebrow {font-size:11px!important;font-weight:700;letter-spacing:.2em;text-transform:uppercase;}
.hpp-hero {position:relative;min-height:540px;padding:70px 7%;background:linear-gradient(115deg,#6d85ac,#a4b4ce);overflow:hidden;}
.hpp-hero-copy {position:relative;z-index:2;width:44%;max-width:430px;}
.hpp-hero h1 {font-size:clamp(40px,4.6vw,70px);font-weight:700;color:white;margin:24px 0;}
.hpp-hero p {color:#f4f6fb;}
.hpp-hero img {position:absolute;right:0;bottom:0;width:53%;height:84%;object-fit:cover;object-position:center;border:12px solid rgba(255,255,255,.12);border-right:0;border-bottom:0;}
.hpp-link {display:inline-block;padding:13px 22px;color:white!important;border:1px solid #e2e8f2;text-decoration:none!important;font-size:13px;font-weight:600;margin-top:20px;}
.hpp-link:hover {background:#ffffff20;}
.hpp-offerings {display:grid;grid-template-columns:1.2fr 1fr 1fr;gap:0;padding:85px 7% 60px;}
.hpp-intro {padding:10px 28px 24px 0;}
.hpp-landing h2 {font-size:clamp(28px,3vw,42px);margin:10px 0 18px;}
.hpp-tile {min-height:180px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:25px;background:#f0f2fa;}
.hpp-tile:nth-child(3n) {background:#fafbfe;}
.hpp-tile:nth-child(5) {background:#fff;}
.hpp-tile svg {width:42px;height:42px;fill:none;stroke:#172335;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round;margin-bottom:18px;}
.hpp-tile strong {font-size:14px;}
.hpp-features {border-top:1px solid #e8ebf2;display:flex;justify-content:space-between;gap:20px;margin:0 7%;padding:26px 0 55px;flex-wrap:wrap;}
.hpp-features span {font-size:13px;color:#56677e;}
.hpp-features b {color:#14223a;margin-right:12px;}
.hpp-plans {padding:60px 12% 20px;text-align:center;background:linear-gradient(#fff,#f8f9fc);}
.hpp-plans p {max-width:480px;margin:0 auto 30px;}
.hpp-main-room {width:100%;height:440px;object-fit:cover;display:block;}
.hpp-rooms {display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:18px;text-align:left;}
.hpp-rooms img {width:100%;height:150px;object-fit:cover;display:block;}
.hpp-rooms figcaption {font-size:12px;padding:10px 0;color:#526078;}
.hpp-rooms figure {margin:0;}
.hpp-cta {padding:60px 7% 12px;text-align:center;}
.hpp-cta p {max-width:540px;margin:0 auto 15px;}
.st-key-hpp_landing_action {text-align:center;padding:0 0 36px;}
.st-key-hpp_landing_action .stButton>button {background:#101b2e;color:white;border:1px solid #101b2e;border-radius:0;box-shadow:none;padding:12px 28px;}
.st-key-hpp_landing_action .stButton>button:hover {background:#263c5f;border-color:#263c5f;color:white;}
.st-key-hpp_landing_action .stButton>button:focus-visible {outline:3px solid #8aa4cf;outline-offset:3px;}
@media(max-width:700px) {
.hpp-hero {padding:35px 7% 0;min-height:0;}
.hpp-hero-copy {width:100%;max-width:none;}
.hpp-hero img {position:relative;width:100%;height:260px;margin-top:28px;border:0;}
.hpp-offerings {grid-template-columns:1fr 1fr;padding:40px 7%;}
.hpp-intro {grid-column:1/-1;}
.hpp-tile {min-height:145px;}
.hpp-plans {padding:35px 7% 15px;}
.hpp-main-room {height:260px;}
.hpp-rooms {gap:8px;}
.hpp-rooms img {height:95px;}
}
</style>
"""

def _icon(paths):
    return '<svg viewBox="0 0 32 32" aria-hidden="true">' + paths + '</svg>'

def show_home(navigate):
    st.markdown(_STYLE, unsafe_allow_html=True)
    st.markdown("""
<section class="hpp-landing hpp-hero">
<div class="hpp-hero-copy">
<p class="hpp-eyebrow">House Price Prediction</p>
<h1>Find your<br>dream home.</h1>
<p>AI-powered property price prediction platform. Explore your next move with property estimates and a budget that works for you.</p>
<a class="hpp-link" href="#hpp-plans">Explore the spaces &nbsp; ↗</a>
</div>
<img src="https://images.unsplash.com/photo-1568605114967-8130f3a36994?auto=format&fit=crop&w=1400&q=85" alt="Detached white house with a pitched roof and garden">
</section>
""", unsafe_allow_html=True)
    facilities = [
        ("Gym", '<path d="M3 12v8m4-11v14m18-14v14m4-11v8M7 16h18"/>'),
        ("Parking", '<path d="M5 20v5m22-5v5M3 20v-7l4-6h18l4 6v7H3Zm0-7h26M8 17h3m10 0h3"/>'),
        ("Fireplace", '<path d="M5 28V8h22v20M3 4h26M10 28V15h12v13"/><path d="M16 26c-7-3-3-8 0-11 0 4 7 7 0 11Z"/>'),
        ("Swimming pool", '<path d="M3 23q4-4 8 0t8 0t10 0M3 28q4-4 8 0t8 0t10 0M10 19V7a3 3 0 0 1 6 0m3 12V7a3 3 0 0 1 6 0M10 12h9m-9 5h9"/>'),
        ("Internet", '<rect x="4" y="21" width="24" height="8" rx="2"/><path d="M9 25h1m4 0h1M6 8q10-9 20 0M10 12q6-5 12 0M14 16q2-2 4 0"/>'),
    ]
    tiles = "".join(
        '<div class="hpp-tile">' + _icon(paths) + '<strong>' + name + '</strong></div>'
        for name, paths in facilities
    )
    st.markdown("""
<section class="hpp-landing">
<div class="hpp-offerings">
<div class="hpp-intro"><p class="hpp-eyebrow">A place to call home</p>
<h2>What we are<br>offering</h2><p><strong>Property facilities</strong><br>Discover the details that make a space feel like home.</p></div>
""" + tiles + """
</div>
<div class="hpp-features"><span><b>01</b> Price Prediction</span><span><b>02</b> Budget Analyzer</span><span><b>03</b> Location Pricing</span></div>
</section>
<section class="hpp-landing hpp-plans" id="hpp-plans">
<p class="hpp-eyebrow">Explore your next space</p>
<h2>Plans and dimensions</h2>
<h3>Rooms Gallery</h3>
<p>A closer look at welcoming interiors and thoughtful spaces. Browse our illustrative property gallery.</p>
<img class="hpp-main-room" src="https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1600&q=85" alt="Bright living room with seating and natural light" loading="lazy">
<div class="hpp-rooms">
<figure><img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=600&q=80" alt="Villa exterior" loading="lazy"><figcaption>01 — Villa</figcaption></figure>
<figure><img src="https://images.unsplash.com/photo-1599423300746-b62533397364?auto=format&fit=crop&w=600&q=80" alt="Apartment interior" loading="lazy"><figcaption>02 — Apartment</figcaption></figure>
<figure><img src="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=600&q=80" alt="Studio bedroom" loading="lazy"><figcaption>03 — Studio</figcaption></figure>
</div>
</section>
<section class="hpp-landing hpp-cta"><h2>Interested in buying property?</h2>
<p>Explore an estimated property price and compare it with your budget. Your next chapter starts with a clearer picture.</p></section>
""", unsafe_allow_html=True)
    with st.container(key="hpp_landing_action"):
        if st.button("Predict House Price  →", key="hpp_landing_start"):
            if st.session_state.get("logged_in", False):
                navigate("predict")
            else:
                st.session_state.page = "predict"
                st.switch_page("pages/login.py")


if __name__ == "__main__":
    def navigate(page):
        st.session_state.page = page
        st.switch_page("app.py")

    show_home(navigate)
