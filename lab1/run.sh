#!/bin/bash

# omogući pokretanje aplikacije
chmod +x password_manager.py

# inicijalizacija
./password_manager.py init glavna_lozinka

# dodavanje zapisa
./password_manager.py put glavna_lozinka www.fer.hr ferlozinka

# dodavanje još jednog zapisa
./password_manager.py put glavna_lozinka www.stranica.hr lozinka2

# dohvaćanje zapisa koji postoji
./password_manager.py get glavna_lozinka www.fer.hr

# dohvaćanje zapisa koji ne postoji
./password_manager.py get glavna_lozinka www.ferrrr.hr

# dohvaćanje zapisa za stranicu www.stranica.hr
./password_manager.py get glavna_lozinka www.stranica.hr

# promjena zapisa za www.stranica.hr
./password_manager.py put glavna_lozinka www.stranica.hr lozinka7

# ponovno dohvaćanje zapisa za www.stranica.hr
./password_manager.py get glavna_lozinka www.stranica.hr

# dohvaćanje zapisa korištenjem krive glavne lozinke
./password_manager.py get main_pasword www.fer.hr

# dodavanje zapisa korištenjem krive glavne lozinke
./password_manager.py put main_pasword www.stranica.hr ffzglozinka

# promjena datoteke, tj. narušavanje integriteta
echo "narusi integritet" >> vault

# pokušaj dodavanja zapisa nakon što je narušen integritet
./password_manager.py put glavna_lozinka ffzg.unizg.hr tvzlozinka

# pokušaj dohvaćanja zapisa nakon što je narušen integritet
./password_manager.py get glavna_lozinka www.fer.hr
