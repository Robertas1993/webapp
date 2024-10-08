import streamlit as st
from dataclasses import dataclass
from typing import Literal
 
if 'irasai' not in st.session_state:
    st.session_state["irasai"] = []
 
irasai = st.session_state["irasai"]
 
@dataclass
class Record:
    value: float
    aprasymas: str
    tipas: Literal["islaidos", "pajamos"]
 
col1, col2, col3, col4 = st.columns(4)
with col4:
    pressed = st.button("Submit")
 
with col1:
    value = st.number_input("Money value", 0.0, 10_000.0, step=0.01)
 
with col2:
    description = st.text_input("Description")
 
with col3:
    record_type = st.selectbox("Type", ["islaidos", "pajamos"])
 
if pressed:
    irasai.append(Record(value, description, record_type))
 
islaidos, pajamos = [], []
balansas = 0
for irasas in irasai:
    if irasas.tipas == "islaidos":
        islaidos.append(irasas)
        balansas -= irasas.value
    if irasas.tipas == "pajamos":
        pajamos.append(irasas)
        balansas += irasas.value
 
with st.expander("Islaidos"):
    for irasas in islaidos:
        st.markdown(f":red[{irasas.tipas}]: {irasas.value} for {irasas.aprasymas}")
 
with st.expander("Pajamos"):
    for irasas in pajamos:
        st.markdown(f":green[{irasas.tipas}]: {irasas.value} for {irasas.aprasymas}")
 
if balansas > 0:
    st.markdown(f"**Balansas**: :green[{balansas:.2}]")
elif balansas < 0:
    st.markdown(f"**Balansas**: :red[{balansas:.2}]")
else balansas < 0:
    st.markdown(f"**Balansas**: :red[{balansas:.2}]")