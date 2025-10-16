import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import io

st.set_page_config(page_title="CSET – Családi Erőforrás Térkép", layout="centered")
st.title("CSET – Családi Erőforrás Térkép (25 kérdéses Likert-skálás MVP)")

# --- 5 dimenzió, mindegyikhez 5 kérdés ---
question_blocks = {
    "Bizalom": [
        "Bízom a családom tagjaiban.",
        "Nyíltan megosztjuk egymással az érzéseinket.",
        "Szükség esetén számíthatunk egymásra.",
        "A döntéseket átláthatóan hozzuk meg.",
        "Hosszú távú terveimet biztonsággal alapozhatom a többiekre."
    ],
    "Csapatmunka": [
        "A családtagok együttműködnek a mindennapi feladatokban.",
        "Közös célokat tűzünk ki.",
        "Mindenkinek van beleszólása a közös ügyekbe.",
        "A feladatok igazságosan oszlanak meg.",
        "A konfliktusokat békésen rendezzük."
    ],
    "Hagyományőrzés": [
        "Fontosnak tartjuk a hagyományok megőrzését.",
        "Értékeljük a család történetét és múltját.",
        "A hagyományok ünneplése összeköt minket.",
        "Büszkék vagyunk a családi múltunkra.",
        "Fontos számunkra a család jó hírneve."
    ],
    "Rugalmasság": [
        "Rugalmasan kezeljük a változásokat.",
        "Nyitottak vagyunk az új ötletekre.",
        "Rugalmasan osztjuk el a feladatokat.",
        "Gyorsan reagálunk a kihívásokra.",
        "Szükség esetén változtatunk a szerepeken."
    ],
    "Lojalitás": [
        "A családban erős a lojalitás.",
        "A család összetart a nehézségekben.",
        "Szívesen teszek extra erőfeszítést a közös célokért.",
        "Szívesen töltünk együtt minőségi időt.",
        "Megbecsüljük egymás munkáját."
    ],
}

st.markdown("_Válaszskála: 1 = egyáltalán nem jellemző … 7 = teljesen jellemző_")

# --- Kérdőív ---
with st.form("cset_form"):
    all_answers = {}
    for dim, qs in question_blocks.items():
        st.subheader(dim)
        st.caption("Mennyire érzi jellemzőnek? (1–7 Likert-skála)")
        dim_vals = []
        for i, q in enumerate(qs, start=1):
            val = st.radio(
                f"{q}",
                options=[1, 2, 3, 4, 5, 6, 7],
                horizontal=True,
                key=f"{dim}_{i}"
            )
            dim_vals.append(val)
            st.divider()
        all_answers[dim] = dim_vals
        st.markdown("")

    submitted = st.form_submit_button("Eredmény megjelenítése")

# --- Eredmények ---
if submitted:
    dimensions = list(question_blocks.keys())
    grouped_scores = [float(np.mean(all_answers[d])) for d in dimensions]

    # Radar chart
    angles = np.linspace(0, 2 * np.pi, len(dimensions), endpoint=False).tolist()
    plot_scores = grouped_scores + grouped_scores[:1]
    plot_angles = angles + angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(plot_angles, plot_scores, linewidth=2)
    ax.fill(plot_angles, plot_scores, alpha=0.35)
    ax.set_xticks(angles)
    ax.set_xticklabels(dimensions, fontsize=12)
    ax.set_yticks(range(1, 8))
    ax.set_yticklabels([str(i) for i in range(1, 8)])
    ax.set_title("Családi Erőforrás Térkép – Összesített radar", pad=20)
    st.pyplot(fig)

    # Szöveges értékelés
    st.subheader("Szöveges értékelés")
    for dim, val in zip(dimensions, grouped_scores):
        if val >= 5:
            if dim == "Bizalom":
                st.write("A bizalom magas szinten van, ami stabil alapot teremt a család működéséhez és hosszú távú biztonságot ad.")
            elif dim == "Csapatmunka":
                st.write("A csapatmunka kiemelkedő, ami támogatja a közös célok elérését és erősíti a mindennapi együttműködést.")
            elif dim == "Hagyományőrzés":
                st.write("A hagyományok tisztelete erős, ami összeköti a családtagokat és identitást ad a közösségnek.")
            elif dim == "Rugalmasság":
                st.write("A rugalmasság magas szintje gyors alkalmazkodást tesz lehetővé a változásokhoz, ami erőforrás a jövő kihívásaira.")
            elif dim == "Lojalitás":
                st.write("A lojalitás erősen jelen van, ami biztosítja az elköteleződést és a hosszú távú összetartozást.")
        elif val <= 3:
            if dim == "Bizalom":
                st.write("A bizalom alacsonyabb szinten jelenik meg, érdemes tudatosan építeni az átláthatóságot és a nyílt kommunikációt.")
            elif dim == "Csapatmunka":
                st.write("A csapatmunka erősítése szükséges, különösen az együttműködés és a feladatmegosztás terén.")
            elif dim == "Hagyományőrzés":
                st.write("A hagyományőrzés kevésbé hangsúlyos, érdemes tudatosan beépíteni a mindennapokba és a közös ünnepekbe.")
            elif dim == "Rugalmasság":
                st.write("A rugalmasság fejlesztése fontos, hogy a család hatékonyabban reagáljon a változásokra.")
            elif dim == "Lojalitás":
                st.write("A lojalitás erősítése szükséges, hogy stabilabb legyen a kötődés és az elköteleződés.")
        else:
            st.write(f"A(z) {dim} közepes szinten van, ami stabil alap, de még tudatos erősítést igényelhet.")

    # Excel DataFrame letöltés
    row = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    for dim, val in zip(dimensions, grouped_scores):
        row[dim] = round(val, 2)

    df_row = pd.DataFrame([row])
    excel_buffer = io.BytesIO()
    df_row.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)

    st.download_button(
        label="📥 Eredmények letöltése Excelben",
        data=excel_buffer,
        file_name="cset_eredmeny.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
