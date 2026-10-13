# Nedeljni izveštaj — NACRT

## 1. Osnovne informacije

| Polje                          | Odgovor                                                                                                                                                                                     |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ime i prezime                  | Dušan Nikolić                                                                                                                                                                               |
| Adresa e-pošte                 | d-nikolic98@outlook.com                                                                                                                                                                     |
| Discord korisničko ime         | Dušan Nikolić                                                                                                                                                                               |
| Nedelja                        | 6 — RAG homework                                                                                                                                                                            |
| Par / tim                      | Tim 9 — Milena Paripovic i Dušan Nikolić                                                                                                                                                    |
| Moj konkretan doprinos / uloga | Pratio sam testiranje, pomagao u radu i proveravao rezultate zajedno sa Milenom.                                                                                                            |
| Datum predaje                  | 2026-10-13                                                                                                                                                                                  |
| Reference na rad i dokaze      | `evidence.md`; zajednički dokumentovani output komande `python -m pytest` sa rezultatom `9 passed in 0.32s`; CLI outputi za podržano i nepodržano pitanje, chunking i `top_k` eksperimente. |

## 2. Moj status

**Status:** Završeno

Osnovni Week 6 zadatak je završen u radu Team 9. Dostavljeni dokazi pokazuju da su testovi prošli i da su provereni podržan odgovor, citati, refusal ponašanje i uticaj chunkovanja. Opcionalni prošireni corpus nije deo ovog izveštaja.

## 3. Rad ove nedelje

Učestvovao sam u radu na jednostavnom RAG pipeline-u i pratio testiranje i rezultate CLI komandi. Cilj je bio da proverimo da sistem vraća relevantan kontekst, navodi ID-jeve izvora, poredi chunking konfiguracije i odbija pitanja za koja nema dovoljno dokaza.

Pratio sam proveru testova. U dostavljenom outputu vidi se da je posle podešavanja okruženja i instaliranja zahteva komanda `python -m pytest` pronašla 9 testova i da je svih 9 prošlo. Rezultat pokriva corpus loading, chunking validaciju, retrieval ordering, citation ponašanje i refusal ponašanje.

Zajedno sa Milenom proveravao sam rezultate podržanog pitanja „What is retrieval augmented generation?“ Za taj slučaj sistem je vratio `Refused: False` i citate `doc-1-chunk-0` i `doc-2-chunk-0`. Proverili smo i nepodržano pitanje „Who was emperor of Mars?“, za koje je sistem vratio jasnu refusal poruku, `Refused: True` i `Citations: None`. To je važno jer sistem ne treba da izmišlja odgovor kada retrieved evidence nije dovoljna.

Pratio sam i poređenje konfiguracija `chunk_size=140, overlap=30` i `chunk_size=80, overlap=10`. U dokazima se vidi da su različite konfiguracije vratile različite chunk ID-jeve i da su manji chunkovi bili fragmentiraniji, uključujući presecanje teksta na granicama. Pregledali smo i `top_k=2` i `top_k=3`. Pošto pitanje o važnosti citata nije imalo dovoljno dokaza u default corpus-u, oba pokretanja su završila refusal-om. To ograničenje je korektno zapisano u `evidence.md`, umesto da se tvrdi da je ranking prikazan kada nije.

Moj doprinos prema dostavljenom opisu bio je praćenje testiranja, pomoć u radu i provera rezultata zajedno sa Milenom. Milena je pokretala testove i CLI komande, pripremila `evidence.md` i prezentuje demo. Dostavljeni materijal ne razdvaja pojedinačne komande koje sam lično pokrenuo, pa ne tvrdim da sam sam izvršio komande koje nisu posebno pripisane meni.

Za sastavljanje ovog nacrta korišćena je AI pomoć za organizovanje dostavljenih beleški i `evidence.md`; rezultate treba proveriti prema sačuvanom outputu pre slanja. AI korišćenje u samoj implementaciji projekta nije navedeno u dostavljenom materijalu.

## 4. Sledeći korak

Predlog za potvrdu: zajedno sa Milenom ponoviti jedan podržani upit sa `top_k=2` i `top_k=3` i dopuniti `evidence.md` konkretnim rangiranim chunkovima, ako je to potrebno za potpuniji Outcome 2.

## 5. Poverljiva napomena za tutora

Nema dodatne napomene.
