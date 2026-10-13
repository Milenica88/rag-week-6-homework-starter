# Nedeljni izveštaj — NACRT

## 1. Osnovne informacije

| Polje                          | Odgovor                                                                                                                                                              |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ime i prezime                  | Milena Paripovic                                                                                                                                                     |
| Adresa e-pošte                 | paripovicmilena@gmail.com                                                                                                                                            |
| Discord korisničko ime         | Milena Paripovic                                                                                                                                                     |
| Nedelja                        | 6 — RAG homework                                                                                                                                                     |
| Par / tim                      | Tim 9 — Milena Paripovic i Dušan Nikolić                                                                                                                             |
| Moj konkretan doprinos / uloga | Pokretala sam testove i CLI komande, proveravala rezultate i prezentujem demo.                                                                                       |
| Datum predaje                  | 2026-10-13                                                                                                                                                           |
| Reference na rad i dokaze      | `evidence.md`; komanda `python -m pytest` sa rezultatom `9 passed in 0.32s`; sačuvani CLI outputi za podržano i nepodržano pitanje, chunking i `top_k` eksperimente. |

## 2. Moj status

**Status:** Završeno

Osnovni Week 6 zadatak je završen za Team 9. Testovi su prošli, demonstrirani su podržan i nepodržan upit, a rezultati su dokumentovani. Opcionalni prošireni corpus nije deo ovog izveštaja.

## 3. Rad ove nedelje

Radila sam na proveri RAG pipeline-a kroz chunking, retrieval, citiranje izvora i refusal ponašanje. Na početku `python -m pytest` nije radio zato što Python nije bio dostupan kroz komandu `python`. U dostavljenom outputu je zatim dokumentovano uspešno kreiranje virtualnog okruženja pomoću `py -m venv .venv`, aktiviranje okruženja i instaliranje zahteva iz `requirements.txt`; lično autorstvo svakog setup koraka nije posebno razdvojeno.

Zatim sam pokrenula celu test-suite komandom `python -m pytest`. Rezultat je bio `9 passed in 0.32s`, što je proverilo učitavanje corpusa, validaciju chunkovanja, redosled retrieval rezultata, citiranje podržanog odgovora i refusal ponašanje.

Za podržano pitanje „What is retrieval augmented generation?“ pokrenula sam CLI i dobila `Refused: False`, sa citatima `doc-1-chunk-0` i `doc-2-chunk-0`. To pokazuje da odgovor koristi retrieved context i da su ID-jevi chunkova eksplicitno navedeni. Za pitanje „Who was emperor of Mars?“ dobila sam `Refused: True` i `Citations: None`, što pokazuje da sistem ne izmišlja odgovor kada corpus nema dovoljno dokaza.

Uporedila sam dve konfiguracije chunkovanja: `chunk_size=140, overlap=30` i `chunk_size=80, overlap=10`. Veći chunkovi su sačuvali više konteksta i vratili `doc-1-chunk-0` i `doc-2-chunk-0`, dok su manji chunkovi vratili `doc-1-chunk-0` i `doc-2-chunk-1` i pokazali fragmentaciju teksta na granicama. Takođe sam pokrenula `top_k=2` i `top_k=3`. Izabrano pitanje o citatima nije imalo dovoljno dokaza u default corpus-u, pa su oba pokušaja pravilno završila refusal-om. Ograničenje je dokumentovano u `evidence.md`; redosled relevantnih rezultata dodatno potvrđuje prolazni retrieval test.

Moj konkretan doprinos bio je izvršavanje komandi i pregled rezultata. Dušan Nikolić je pratio testiranje, pomagao u radu i proveravao rezultate zajedno sa mnom. Ja prezentujem demo. `evidence.md` sadrži zajednički dokumentovane dokaze; dostavljeni materijal ne dokazuje posebno ko ga je tehnički sastavljao.

Za sastavljanje ovog nacrta korišćena je AI pomoć za organizovanje dostavljenih beleški i `evidence.md`; komande i rezultate proveravam prema sačuvanom outputu. AI korišćenje u samoj implementaciji projekta nije navedeno u dostavljenom materijalu.

## 4. Sledeći korak

Predlog za potvrdu: pre druge sesije pokrenuti podržano pitanje sa `top_k=2` i `top_k=3`, tako da se u `evidence.md` prikaže i konkretno poređenje rangiranih chunkova, a ne samo refusal rezultat.

## 5. Poverljiva napomena za tutora

Nema dodatne napomene.
