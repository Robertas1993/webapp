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
    st.markdown(f"**Balansas**: :green[{balansas:.2f}]")

elif balansas < 0:
    st.markdown(f"**Balansas**: :red[{balansas:.2f}]")

else:
    st.markdown(f"**Balansas**: {balansas:.2f}")
    


import datetime as dt
import os
import pickle
from dataclasses import dataclasses
import streamlit as st
from typing import Literal
st.write("Roberto 's Streamlit BIBLIOTEKA")

@dataclasses
class Knyga:
    def __init__(self, pavadinimas, autorius, leidybos_metai, zanras):
        self.pavadinimas = pavadinimas
        self.autorius = autorius
        self.leidybos_metai = leidybos_metai
        self.zanras = zanras
        self.pasiskolinta = False
        self.grazinimo_data = None
        self.skaitytojas = None 

    def yra_veluojanti(self):
        if self.grazinimo_data and self.grazinimo_data < dt.date.today():
            return True
        else:
            return False

    def __str__(self):
        return f"Pavadinimas: {self.pavadinimas}, Autorius: {self.autorius}, Leidimo metai: {self.leidybos_metai}, Žanras: {self.zanras}"



@dataclasses
class Biblioteka:
    def __init__(self):
        self.knygos = self.load_knygos()
        self.skaitytojai = self.load_skaitytojai()
        if self.skaitytojai is None:
            self.skaitytojai = []



    def paskolinti_knyga(self, pavadinimas, vardas, pavarde):
        skaitytojas = self.rasti_skaitytoja(vardas, pavarde)
        if skaitytojas is None:
            skaitytojas = Skaitytojas(vardas, pavarde)
            self.skaitytojai.append(skaitytojas)
            self.save_skaitytojai()
            st.write(f"Skaitytojas '{vardas} {pavarde}' pridėtas sėkmingai!")

        knyga = self.rasti_knyga(pavadinimas)
        if knyga:
            skaitytojas.paskolinti_knyga(knyga)
        else:
            st.write("Knyga nerasta.")
                
    def prideti_skaitytoja(self, vardas, pavarde):
        skaitytojas = Skaitytojas(vardas, pavarde)
        self.skaitytojai.append(skaitytojas)
        self.save_skaitytojai()
    
        st.write(f"Skaitytojas '{vardas} {pavarde}' pridėtas sėkmingai!")
        
        
    def load_knygos(self):
        if os.path.exists("knygos.pkl"):
            with open("knygos.pkl", "rb") as f:
                knygos = pickle.load(f)
                for knyga in knygos:
                    if not hasattr(knyga, 'pasiskolinta'):
                        knyga.pasiskolinta = False
                    if not hasattr(knyga, 'grazinimo_data'):
                        knyga.grazinimo_data = None
                return knygos
        else:
                        return []

    def load_skaitytojai(self):

        if os.path.exists("skaitytojai.pkl"):

            with open("skaitytojai.pkl", "rb") as f:

                return pickle.load(f)

        else:

            return None

    def save_knygos(self):
        with open("knygos.pkl", "wb") as f:
            pickle.dump(self.knygos, f)

    def save_skaitytojai(self):
        with open("skaitytojai.pkl", "wb") as f:
            pickle.dump(self.skaitytojai, f)

    def prideti_knyga(self, knyga):
        self.knygos.append(knyga)
        self.save_knygos()
    def prideti_knyga(self, knyga):
        self.knygos.append(knyga)
        self.save_knygos()

    def ieskoti_knygos(self, pavadinimas_arba_autorius):
        rezultatai = []
        for knyga in self.knygos:
            if pavadinimas_arba_autorius in knyga.pavadinimas or pavadinimas_arba_autorius in knyga.autorius:
                rezultatai.append(knyga)
        return rezultatai

    def istrinti_knyga(self, knyga):
        if knyga in self.knygos:
            self.knygos.remove(knyga)
            self.save_knygos()
            st.write(f"Knyga '{knyga.pavadinimas}' pašalinta sėkmingai!")
        else:
            st.write(f"Knyga '{knyga.pavadinimas}' nerasta!")





    def rasti_knyga(self, pavadinimas):
        for knyga in self.knygos:
            if knyga.pavadinimas == pavadinimas:
                return knyga
        return None
    
    def grazinti_knyga(self, pavadinimas, vardas, pavarde):
            for knyga in self.knygos:
                if knyga.pavadinimas == pavadinimas:
                    if knyga.pasiskolinta:
                        knyga.pasiskolinta = False
                        knyga.grazinimo_data = None
                        skaitytojas = self.rasti_skaitytoja(vardas, pavarde)
                        if skaitytojas:
                            skaitytojas.pasiskolintos_knygos.remove(knyga)
                            self.save_skaitytojai()
                            st.write(f"Knyga '{knyga.pavadinimas}' grąžinta sėkmingai!")
                        else:
                            st.write(f"Skaitytojas '{vardas} {pavarde}' nerastas!")
                    else:
                        st.write("Knyga nėra paskolinta.")
                    return

            st.write(f"Knyga '{pavadinimas}' nerasta!")

    def rasti_skaitytoja(self, vardas, pavarde):
            for skaitytojas in self.skaitytojai:
                if skaitytojas.vardas == vardas and skaitytojas.pavarde == pavarde:
                    return skaitytojas
            return None
                    
    def perziureti_pasiskolintas_knygas(self, vardas, pavarde):
        skaitytojas = self.rasti_skaitytoja(vardas, pavarde)
        if skaitytojas:
            st.write("Pasiskolintos knygos:")
            for knyga in skaitytojas.pasiskolintos_knygos:
                st.write(knyga)
        else:
            st.write("Skaitytojas nerastas!")   
            
    def rasti_skaitytojus_su_skolomis(self):
        skaitytojai_su_skolomis = [skaitytojas for skaitytojas in self.skaitytojai if skaitytojas.pasiskolintos_knygos]
        if skaitytojai_su_skolomis:
            st.write("Skaitytojai su skolomis:")
            for skaitytojas in skaitytojai_su_skolomis:
                veluojancios_knygos = [knyga for knyga in skaitytojas.pasiskolintos_knygos if knyga.grazinimo_data < dt.date.today()]
                if veluojancios_knygos:
                    knygu_info = ", ".join(f"{knyga.pavadinimas} (grąžinti iki {knyga.grazinimo_data})" for knyga in veluojancios_knygos)
                    st.write(f"{skaitytojas.vardas} {skaitytojas.pavarde}: {knygu_info}")
        else:
            st.write("Nėra skaitytojų su skolomis.")
            
@dataclasses
class Skaitytojas:
    def __init__(self, vardas, pavarde):
        self.vardas = vardas
        self.pavarde = pavarde
        self.pasiskolintos_knygos = []
        self.max_knygu_kiekis = 3

    def paskolinti_knyga(self, knyga):
        if len(self.pasiskolintos_knygos) < self.max_knygu_kiekis:
            knyga.grazinimo_data = dt.date.today() + dt.timedelta(days=21)  
            st.write(f"Knygos '{knyga.pavadinimas}' grąžinimo data: {knyga.grazinimo_data}")
            knyga.pasiskolinta = True  
            knyga.skaitytojas = self  
            self.pasiskolintos_knygos.append(knyga)   
        else:
            st.write(f"{self.vardas} {self.pavarde} jau turi {self.max_knygu_kiekis} knygų, negali pasiimti daugiau")
            
    def turi_velavimu(self):
        for knyga in self.pasiskolintos_knygos:
            if knyga.yra_veluojanti():
                return True
        return False

    
    def pasiimti_knyga(self, knyga):
        if len(self.pasiskolintos_knygos) < self.max_knygu_kiekis:
            self.pasiskolintos_knygos.append(knyga)
            st.write(f"{self.vardas} {self.pavarde} pasiėmė knygą '{knyga.pavadinimas}'")
        else:
            st.write(f"{self.vardas} {self.pavarde} jau turi {self.max_knygu_kiekis} knygų, negali pasiimti daugiau")
            


def naudotojo_funkcija():
    biblioteka = Biblioteka()
    biblioteka.perziureti_pasiskolintas_knygas("Vardas", "Pavarde")
    while True:
        st.write("Bibliotekos valdymo sistema")
        st.write("1. Įtraukti knygą")
        st.write("2. Pašalinti seną knygą")
        st.write("3. Pasiimti knygą išsinešimui ")
        st.write("4. Ieškoti knygos")
        st.write("5. Rodyti visas knygas")
        st.write("6. Peržiūrėti visas vėluojančias knygas")
        st.write("7. Peržiūrėti pasiskolintas knygas")
        st.write("8 Baigti darbą")

        pasirinkimas = input("Įveskite savo pasirinkimą: ")

        if pasirinkimas == "1":
            pavadinimas = input("Įveskite knygos pavadinimą: ")
            autorius = input("Įveskite knygos autorių: ")
            leidybos_metai = int(input("Įveskite leidybos metus: "))
            zanras = input("Įveskite žanrą: ")
            knyga = Knyga(pavadinimas, autorius, leidybos_metai, zanras)
            biblioteka.prideti_knyga(knyga)
            st.write(f"Knyga '{pavadinimas}' įtraukta sėkmingai!")

        elif pasirinkimas == "2":
            knyga_pavadinimas = str(input("Įveskite knygos pavadinimą kuria norite Ištrinti "))
            for knyga in biblioteka.knygos:
                if knyga.pavadinimas == knyga_pavadinimas:
                    biblioteka.istrinti_knyga(knyga)
                    break
            else:
                st.write(f"Knyga '{knyga_pavadinimas}' nerasta!")
                
        elif pasirinkimas == "3":
            pavadinimas = input("Įveskite knygos pavadinimą: ")
            vardas = input("Įveskite skaitytojo vardą: ")
            pavarde = input("Įveskite skaitytojo pavardę: ")
            biblioteka.paskolinti_knyga(pavadinimas, vardas, pavarde)

        elif pasirinkimas == "4":
            pavadinimas_arba_autorius = input("Įveskite knygos pavadinimą arba autorių: ")
            rezultatai = biblioteka.ieskoti_knygos(pavadinimas_arba_autorius)
            if rezultatai:
                for knyga in rezultatai:
                    st.write(knyga)
            else:
                st.write(f"Knyga '{pavadinimas_arba_autorius}' nerasta!")

        

        elif pasirinkimas == "5":
            knygu_kiekiai = {}
            for knyga in biblioteka.knygos:
                raktas = (knyga.pavadinimas, knyga.autorius, knyga.leidybos_metai, knyga.zanras)
                if raktas in knygu_kiekiai:
                    knygu_kiekiai[raktas] += 1
                else:
                    knygu_kiekiai[raktas] = 1

            for raktas, kiekis in knygu_kiekiai.items():
                pavadinimas, autorius, leidybos_metai, zanras = raktas
                if kiekis > 1:
                    st.write(f"Pavadinimas: {pavadinimas}, Autorius: {autorius}, Leidimo metai: {leidybos_metai}, Žanras: {zanras} ({kiekis} egz.)")
                else:
                    st.write(f"Pavadinimas: {pavadinimas}, Autorius: {autorius}, Leidimo metai: {leidybos_metai}, Žanras: {zanras}")

        elif pasirinkimas=="6":
            biblioteka.rasti_skaitytojus_su_skolomis()
            break

        elif pasirinkimas == "7":

            vardas = input("Įveskite savo vardą: ")

            pavarde = input("Įveskite savo pavardę: ")

            biblioteka.perziureti_pasiskolintas_knygas(vardas, pavarde)
            
        elif pasirinkimas == "8":
            biblioteka.save_knygos()
            biblioteka.save_skaitytojai()
            st.write("Duomenys išsaugoti. Baigiama darbo sesija.")
            break

        else:
            st.write("Neteisingas pasirinkimas. Bandykite dar kartą.")

if __name__ == "__main__":            
    naudotojo_funkcija()


