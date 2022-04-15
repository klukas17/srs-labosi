#!/bin/bash

# omogući pokretanje usermgmt i login skripti
chmod u+x usermgmt.py
chmod u+x login.py

# brisanje stare datoteke vault.txt
rm vault.txt

# dodavanje nekoliko korisnika
./usermgmt.py add korisnik1 # input: lozinka1, lozinka1
./usermgmt.py add korisnik2 # input: lozinka2, lozinka2
./usermgmt.py add korisnik3 # input: lozinka3, lozinka3
./usermgmt.py add korisnik4 # input: lozinka4, lozinka4
./usermgmt.py add korisnik5 # input: lozinka5, lozinka5
echo ""

# pokušaj dodavanja korisnika koji već postoji
./usermgmt.py add korisnik1
echo ""

# pokušaj dodavanja korisnika s mismatching lozinkama
./usermgmt.py add korisnik6 # input: lozinka6, 6, lozinka6, lozinka6
echo ""

# brisanje korisnika
./usermgmt.py del korisnik4
echo ""

# promjena lozinke korisnika
./usermgmt.py passwd korisnik2 # input: lozinka22, lozinka22
echo ""

# forsiranje promjene lozinke
./usermgmt.py forcepass korisnik1
echo ""

# ispravan login
./login.py korisnik5 # input: lozinka5
echo ""

# neispravna lozinka
./login.py korisnik5 # input: lozinka6
echo ""

# login kada je potrebno promijeniti lozinku
./login.py korisnik1 # input: lozinka1, lozinka11, lozinka11
echo ""

# ponovan login za prethodnog korisnika
./login.py korisnik1 # input: lozinka11
echo ""