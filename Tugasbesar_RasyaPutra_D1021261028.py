import streamlit as st

st.set_page_config(page_title="Laundry Kiloan", page_icon="🧺", layout="centered")

# ===== TAMPILAN (CSS) - bagian ini cuma untuk desain =====
st.markdown("""
<style>
.header {
    background: linear-gradient(135deg, #0f4c81, #2a9d8f);
    padding: 28px 24px; border-radius: 18px; color: white; margin-bottom: 24px;
}
.header h1 { margin: 0; font-size: 1.7rem; font-weight: 700; color: white; }
.header p { margin: 6px 0 0 0; opacity: 0.85; font-size: 0.95rem; }

.card {
    background: rgba(128,128,128,0.10); border: 1px solid rgba(128,128,128,0.25);
    border-radius: 14px; padding: 14px 16px; margin-bottom: 10px;
}
.card .label { font-size: 0.8rem; opacity: 0.7; }
.card .value { font-size: 1.15rem; font-weight: 600; }

.total {
    background: linear-gradient(135deg, #2a9d8f, #43c59e);
    border-radius: 14px; padding: 18px 20px; color: white; margin-top: 6px;
}
.total .label { font-size: 0.85rem; opacity: 0.9; }
.total .value { font-size: 1.8rem; font-weight: 700; }


.scale-wrap { text-align: center; }
.gauge {
    position: relative; width: 200px; height: 100px; margin: 10px auto 6px auto;
    border-radius: 100px 100px 0 0; overflow: hidden;
    background: linear-gradient(90deg, #2a9d8f, #f4c95d, #e76f51);
}
.needle {
    position: absolute; bottom: 0; left: 50%; width: 4px; height: 88px;
    background: #1b1b1b; border-radius: 4px; transform-origin: bottom center;
}
.pivot {
    position: absolute; bottom: -8px; left: 50%; width: 18px; height: 18px;
    margin-left: -9px; background: #1b1b1b; border-radius: 50%;
}
.scale-label { font-size: 1.3rem; font-weight: 700; }
.basket { text-align: center; line-height: 1.5; }
.basket .icon { font-size: 3rem; }
.basket .items { font-size: 1.3rem; }

div.stButton > button {
    width: 100%; border-radius: 10px; padding: 10px 0; font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ===== HEADER =====
st.markdown("""
<div class="header">
    <h1>🧺 Laundry Kiloan</h1>
    <p>Hitung cepat biaya laundry kiloan</p>
</div>
""", unsafe_allow_html=True)

# ===== INPUT =====
nim = st.text_input("NIM (10 digit)", key="nim", placeholder="contoh: 2411001347")
berat = st.number_input("Berat Cucian (kg)", key="berat", value=None, step=1,
                        placeholder="contoh: 10")


def reset():
    st.session_state.nim = ""
    st.session_state.berat = None


col1, col2 = st.columns(2)
hitung = col1.button("Hitung", type="primary")
col2.button("Reset", on_click=reset)

# ===== PROSES (logika tidak berubah) =====
if hitung:
    if len(nim) != 10 or not nim.isdigit():
        st.error("NIM tidak valid! Harus 10 digit angka.")
    elif berat is None or berat <= 0:
        st.error("Berat tidak valid! Harus bilangan bulat lebih dari 0.")
    else:
        tarif = 5000 + int(nim[-1]) * 500
        genap = 0
        for d in nim:
            if int(d) % 2 == 0:
                genap = genap + 1
        diskon = genap  # persen
        normal = berat * tarif
        potongan = diskon / 100 * normal
        total = normal - potongan

        # ===== KERANJANG & TIMBANGAN (sesuai berat) =====
        sudut = -90 + min(berat, 50) / 50 * 180   # 0 kg = kiri, 50 kg = kanan
        jumlah = min(berat, 20)                    # maksimal 20 baju ditampilkan
        sisa = berat - jumlah
        baju = "👕" * jumlah + (f" +{sisa}" if sisa > 0 else "")
        v1, v2 = st.columns(2)
        v1.markdown(f"""<div class="basket"><div class="icon">🧺</div>
            <div class="items">{baju}</div>
            <div class="label">Keranjang cucian</div></div>""", unsafe_allow_html=True)
        v2.markdown(f"""<div class="scale-wrap"><div class="gauge">
            <div class="needle" style="transform: translateX(-50%) rotate({sudut}deg);"></div>
            <div class="pivot"></div></div>
            <div class="scale-label">⚖️ {berat} kg</div></div>""", unsafe_allow_html=True)

        # ===== HASIL =====
        st.markdown("### Rincian Perhitungan")
        a, b = st.columns(2)
        a.markdown(f"""<div class="card"><div class="label">Tarif per kg</div>
            <div class="value">Rp {tarif:,.0f}</div></div>""", unsafe_allow_html=True)
        b.markdown(f"""<div class="card"><div class="label">Persen diskon</div>
            <div class="value">{diskon} %</div></div>""", unsafe_allow_html=True)
        c, d_ = st.columns(2)
        c.markdown(f"""<div class="card"><div class="label">Biaya normal</div>
            <div class="value">Rp {normal:,.0f}</div></div>""", unsafe_allow_html=True)
        d_.markdown(f"""<div class="card"><div class="label">Potongan</div>
            <div class="value">Rp {potongan:,.0f}</div></div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class="total"><div class="label">Total bayar</div>
            <div class="value">Rp {total:,.0f}</div></div>""", unsafe_allow_html=True)
