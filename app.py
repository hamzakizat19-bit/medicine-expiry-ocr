"""Advanced: Streamlit веб-интерфейсі.
Іске қосу:  streamlit run app.py
"""
from datetime import date

import easyocr
import numpy as np
import streamlit as st
from PIL import Image

from medicine_ocr import extract_expiry, check_status

st.set_page_config(page_title="Medicine Expiry Checker", page_icon="💊")
st.title("💊 Дәрінің жарамдылық мерзімін анықтау")


@st.cache_resource
def get_reader():
    return easyocr.Reader(['en'], gpu=False)


uploaded = st.file_uploader("Дәрі қаптамасының суретін жүктеңіз", type=["jpg", "jpeg", "png"])

if uploaded:
    image = Image.open(uploaded).convert("RGB")
    st.image(image, use_container_width=True)

    with st.spinner("EasyOCR мәтінді оқып жатыр..."):
        texts = get_reader().readtext(np.array(image), detail=0)

    st.subheader("Танылған мәтін")
    st.code("\n".join(texts) or "(мәтін жоқ)")

    expiry = extract_expiry(texts)
    if expiry is None:
        st.error("Жарамдылық мерзімі табылмады! (Expiration date not found)")
    else:
        today = date.today()
        status, status_kz, days_left = check_status(expiry, today)
        c1, c2, c3 = st.columns(3)
        c1.metric("Бүгін", str(today))
        c2.metric("Жарамдылық мерзімі", str(expiry))
        c3.metric("Қалған күн", days_left)
        msg = f"{status} — {status_kz}"
        if status == "EXPIRED":
            st.error(msg)
        elif status == "EXPIRING SOON":
            st.warning(msg)
        else:
            st.success(msg)
