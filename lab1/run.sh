#!/bin/bash

# omogući pokretanje aplikacije
chmod u+x password_manager.py

# upute za korištenje
./password_manager.py help

# inicijalizacija
./password_manager.py init glavna_lozinka

# dodavanje nekoliko zapisa
./password_manager.py put glavna_lozinka fer.unizg.hr ferlozinka
./password_manager.py put glavna_lozinka moodle.fer.hr moodlelozinka
./password_manager.py put glavna_lozinka ferko.fer.hr ferkolozinka
./password_manager.py put glavna_lozinka sczg.unizg.hr sczglozinka
./password_manager.py put glavna_lozinka srce.unizg.hr srcelozinka

# dohvaćanje broja zapisa
./password_manager.py count glavna_lozinka

# ispis svih zapisa
./password_manager.py list glavna_lozinka

# dohvaćanje zapisa koji postoji
./password_manager.py get glavna_lozinka fer.unizg.hr

# dohvaćanje drugog zapisa koji postoji
./password_manager.py get glavna_lozinka moodle.fer.hr 

# dohvaćanje zapisa koji ne postoji
./password_manager.py get glavna_lozinka ffzg.unizg.hr

# dohvaćanje zapisa za ferko.fer.hr
./password_manager.py get glavna_lozinka ferko.fer.hr

# promjena zapisa za ferko.fer.hr
./password_manager.py put glavna_lozinka ferko.fer.hr ferkonovalozinka

# ponovno dohvaćanje zapisa za ferko.fer.hr
./password_manager.py get glavna_lozinka ferko.fer.hr

# dohvaćanje zapisa korištenjem krive glavne lozinke
./password_manager.py get kriva_lozinka1 fer.unizg.hr

# dodavanje zapisa korištenjem krive glavne lozinke
./password_manager.py put kriva_lozinka2 ffzg.unizg.hr ffzglozinka

# dohvaćanje broja zapisa korištenjem krive glavne lozinke
./password_manager.py count kriva_lozinka3

# ispis svih zapisa korištenjem krive glavne lozinke
./password_manager.py list kriva_lozinka4

# promjena datoteke, tj. narušavanje integriteta
echo "narusi_integritet" >> vault

# pokušaj dohvaćanja zapisa nakon što je narušen integritet
./password_manager.py get glavna_lozinka srce.unizg.hr

# pokušaj dodavanja zapisa nakon što je narušen integritet
./password_manager.py put glavna_lozinka ffzg.unizg.hr ffzglozinka

# obriši datoteku s lozinkama
rm vault

# pokušaj dohvatiti neku lozinku nakon brisanja datoteke s lozinkama
./password_manager.py get glavna_lozinka fer.unizg.hr