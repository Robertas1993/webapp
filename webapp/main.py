import streamlit as st
import datetime as dt
import os
import pickle
from dataclasses import dataclass

@dataclass
class Knyga:
    pavadinimas: str
    autorius: str
    leidybos_metai: int
    zanras: str
    pasiskolinta: bool = False
    grazinimo_data: dt.date = None
    skaitytojas: 'Skaitytojas' = None

    def yra_veluojanti(self):
        if self.grazinimo_data and self.grazinimo_data < dt.date.today():
            return True
        else:
            return False

    def __str__(self):
        return f"Pavadinimas: {self.pavadinimas}, Autorius: {self.autorius}, Leidimo metai: {self.leidybos_metai}, Žanras: {self.zanras}"

@dataclass
class Skaitytojas:
    vardas: str
    pavarde: str
    pasiskolintos_knygos: list[Knyga] = dataclass.field(default_factory=list)
    max_knygu_kiekis: int = 3

    def paskolinti_knyga(self, knyga: Knyga):
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

class Biblioteka:
    def __init__(self):
        self.knygos = self.load_knygos()
        self.skaitytojai = self.load_skaitytojai()

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

    def prideti_knyga(self, knyga: Knyga):
        self.knygos.append(knyga)
        self.save_knygos()

    def ieskoti_knygos(self, pavadinimas_arba_autorius: str):
        rezultatai = []
        for knyga in self.knygos:
            if pavadinimas_arba_autorius in knyga.pavadinimas or pavadinimas_arba_autorius in knyga.autorius:
                rezultatai.append(knyga)
        return rezultatai

    def istrinti_knyga(self, knyga: Knyga):
        if knyga in self.knygos:
            self.knygos.remove(knyga)
            self.save_knygos()
            st.write(f"Knyga '{knyga.pavadinimas}' pašalinta sėkmingai!")
        else:
            st.write(f"Knyga '{knyga.pavadinimas}' nerasta!")

    def rasti_kny ga(self, pavadinimas: str):
        for knyga in self.knygos:
            if knyga.pavadinimas == pavadinimas:
                return knyga
        return None

    def grazinti_knyga(self, pavadinimas: str, vardas: str, pavarde: str):
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

    def rasti_skaitytoja(self, vardas: str, pavarde: str):
        for skaitytojas in self.skaitytojai:
            if skaitytojas.vardas == vardas and skaitytojas.pavarde == pavarde:
                return skaitytojas
        return None

    def perziureti_pasiskolintas_knygas(self, vardas: str, pavarde: str):
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

def main():
    biblioteka = Biblioteka()
    st.write("Bibliotekos valdymo sistema")
    pasirinkimas = st.selectbox("Pasirinkite veiksmą", ["Įtraukti knygą", "Pašalinti seną knygą", "Pasiimti knygą išsinešimui", "Ieškoti knygos", "Rodyti visas knygas", "Peržiūrėti visas vėluojančias knygas", "Peržiūrėti pasiskolintas knygas", "Baigti darbą"])

    if pasirinkimas == "Įtraukti knygą":
        pavadinimas = st.text_input("Įveskite knygos pavadinimą")
        autorius = st.text_input("Įveskite knygos autorių")
        leidybos_metai = st.number_input("Įveskite leidybos metus")
        zanras = st.text_input("Įveskite žanrą")
        knyga = Knyga(pavadinimas, autorius, leidybos_metai, zanras)
        biblioteka.prideti_knyga(k nyga)
        st.write(f"Knyga '{pavadinimas}' įtraukta sėkmingai!")

    elif pasirinkimas == "Pašalinti seną knygą":
        knyga_pavadinimas = st.text_input("Įveskite knygos pavadinimą kuria norite Ištrinti")
        for knyga in biblioteka.knygos:
            if knyga.pavadinimas == knyga_pavadinimas:
                biblioteka.istrinti_knyga(knyga)
                break
        else:
            st.write(f"Knyga '{knyga_pavadinimas}' nerasta!")

    elif pasirinkimas == "Pasiimti knygą išsinešimui":
        pavadinimas = st.text_input("Įveskite knygos pavadinimą")
        vardas = st.text_input("Įveskite skaitytojo vardą")
        pavarde = st.text_input("Įveskite skaitytojo pavardę")
        biblioteka.paskolinti_knyga(pavadinimas, vardas, pavarde)

    elif pasirinkimas == "Ieškoti knygos":
        pavadinimas_arba_autorius = st.text_input("Įveskite knygos pavadinimą arba autorių")
        rezultatai = biblioteka.ieskoti_knygos(pavadinimas_arba_autorius)
        if rezultatai:
            for knyga in rezultatai:
                st.write(knyga)
        else:
            st.write(f"Knyga '{pavadinimas_arba_autorius}' nerasta!")

    elif pasirinkimas == "Rodyti visas knygas":
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

    elif pasirinkimas == "Peržiūrėti visas vėluojančias knygas":
        biblioteka.rasti_skaitytojus_su_skolomis()

    elif pasirinkimas == "Peržiūrėti pasiskolintas knygas":
        vardas = st.text_input("Įveskite savo vardą")
        pavarde = st.text_input("Įveskite savo pavardę")
        biblioteka.perziureti_pasiskolintas_knygas(vardas, pavarde)

    elif pasirinkimas == "Baigti darbą":
        biblioteka.save_knygos()
        biblioteka.save_skaitytojai()
        st.write("Duomenys išsaugoti. Baigiama darbo sesija.")

if __name__ == "__main__":
    main()