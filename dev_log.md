# Vývoj projektu

- Cílem projektu bylo vytvořit clusterizaci předmětů na MFF UK na základě jejich názvu, anotací a sylabu.
- Vstupní data: Export ze SIS v rámci vývoje projektu RecSIS

## 1. verze - Základní (15 clusterů)
- Na začátku projektu jsem si navrhla základní schéma: 
    1. Export dat z databáze - kód předmětu, název, anotace a sylabus v češtině
    2. Odstranění předmětů, která nemají ani anotaci, ani sylabus delší než 3 slova.
    3. Čištění textu pomocí vyfiltrování pomocí manuálně vytvořeného seznamu českých stop-slov
    4. Reprezentace předmětu pomocí TF-IDF
    5. Clusterizace pomocí K-Means
    6. Vizualizace: PCA + t-SNE

Výsledek:
![1.0 verze clusterizace](cluster_map_archive/cluster_map_1.0.jpg)

[1.0 interaktivní verze clusterizace](cluster_map_archive/cluster_map_1.0.html)


### Problémy
I přesto, že jsme z dat brali jen sloupce s daty v češtině, tak vidíme, že velké clustery tvoří anglická stop slova a také římské číslovky jako např. "ii". Zařadíme tedy také odstranění anglických stop slov a číslovek. 

Dalším problémem jsou v akademické sféře běžně používaná data jako "seminář", "předměty", "povinné", "kapitoly", atd. Tak přidáme manuální vyfiltrování těchto slov. Dále ještě přidáme slovník pro manuální překlad některých akademických slov z angličtiny, které nám nevyfiltrovaly anglická stop-slova, ale žádný význam pro nás nemají, jako např. "course".

Výsledek:
![1.1 verze clusterizace](cluster_map_archive/cluster_map_1.4.jpg)

[1.1 interaktivní verze clusterizace](cluster_map_archive/cluster_map_1.4.html)


## 2. verze - Mazání anglický stop-slov a akademického balastu (20 clusterů)
- Po lepším čištění dat se nyní zaměříme na lepší rozdělelní do clusterů a začneme s tím, že zvýšíme počet clusterů na 20.

Výsledek:
![2.0 verze clusterizace](cluster_map_archive/cluster_map_2.0.jpg)

[2.0 interaktivní verze clusterizace](cluster_map_archive/cluster_map_2.0.html)


### Problémy
20 clusterů nám stále přijde málo, tak ještě zvýšíme počet clusterů a to na 24. A zároveň přidáme nová slova na odstranění do akademického slovníku.

Výsledek:
![2.1 verze clusterizace](cluster_map_archive/cluster_map_2.2.jpg)

[2.1 interaktivní verze clusterizace](cluster_map_archive/cluster_map_2.2.html)


Dále v datech vidíme problém se skloňováním v češtině - "algoritmů" a "algoritmy" jsou brané jako jiné slovo, stejně tak "strojové" a "strojový". Přidáme tedy lemmatizaci - určení základního slova ohýbaného tvaru. A přidáme ještě dva clustery - nyní 26 clusterů. Využijeme také jinou paletu barev, aby jsme lépe rozlišili jednotlivé clustery. K názvu clusteru ještě do závorky přidáme předmět, který je nejblíže centroidu.

Výsledek:
![2.2 verze clusterizace](cluster_map_archive/cluster_map_2.3.jpg)

[2.2 interaktivní verze clusterizace](cluster_map_archive/cluster_map_2.3.html)

Bohužel lemmatizace (pomocí knihovny) v tomto případě moc nezabrala - některá slova knihovna pravděpodobně vůbec neznala jako např. "kvantová". A např. pro "strojové učení" jsme dostaly "strojové učený". 

## 3. verze - Stemming + Překlady + Bi-gramy (26 clusterů)
- V této verzi jsme zařadili bi-gramy, aby náš algoritmus bral v úvahu i často používaná sousloví, např. "strojové učení" nebo "umělá inteligence".
- Dále jsme se snažili vyřešit problém s lemmatizací, a přistoupili jsme tak k radikálnějšímu kroku a to ke stemming - úplně uřezat koncovky slov.
- Dále jsme se snažili vařešit to, že některé texty, i přestože by měli být podle databáze v češtině jsou v angličtině. To nám dělá problém při identifikaci podobných předmětů, např. "development" vs. "vývoj".
- Zařadili jsme tedy knihovnu deep-translator a v případě, že jsme text identifikovali jako anglický (obsahoval nějaké procenta anglických stop-slov, tak jsme text přeložili.)

Výsledek:
![3. verze clusterizace](cluster_map_archive/cluster_map_3.0.jpg)

[3. interaktivní verze clusterizace](cluster_map_archive/cluster_map_3.0.html)

### Problémy 
Stemming jsme v první várce nastavili jen na koncovky "-a", "-e", "-i", "-o", ... Proto jsme nově zařadili i koncovky jako "-ický", "-ích", "-ami" atd. Opět pokračujeme ve vyřazování dalších slov z akademického prostředí. 

## 4. verze - Synonyma
Nyní už máme textové popisy poměrně čisté a můžeme se tak zaměřit na větší detaily. V některých případech se nám neidentifikují synonyma jako stejná slova a občas se nám pak rozdělují do jiných clusterů, např. "učitel" a "pedagog" nebo i "angličtina" a anglický jazyk". Přidáme tedy manuální identifikaci některých klíčových slov. 

Výsledek:
![4. verze clusterizace](cluster_map_archive/cluster_map_5.0.jpg)

[4. interaktivní verze clusterizace](cluster_map_archive/cluster_map_5.0.html)

### Problémy 
Dalším nepříjemným aspektem jsou cizí jazyky. Za ideální stav jsme považovali, že se všechny jazyky sloučí do jednoho clusteru. Nyní máme společně jazyky jako francouština, ruština, španělština, němčina a čeština. Ale angličtina se nám v některých případech odděluje, protože jsou tu různá specifika jako "Angličtina pro fyziky", "Obchodní angličtina" atd. Další problém dělá i výskyt slova "anglický jazyk" nebo "angličtina" v lingvistických předmětech nebo v případech kdy je zmíněno např. "Předmět je vyučován v anglickém jazyce.". 

V průběhu celého vývoje jsme s tímto clustrem dělali pokusy např. nahrazení "německý", "španělský" atd. za "anglický", aby se tyto clustery sloučili. Nebo např. úplné odstranění těchto slov. Nebo nahrazení i včetně "anglický" za sousloví "cizí jazyk". Bohužel "cizí jazyk" pak dělal problémy ve skupinách, kde byla "angličtina" zmíněna, i když to nebyl předmět s výukou cizího jazyka. 

Ve finále jsme skončili u nahrazení všech jazyků za "anglický". 

Výsledek:
![4.1 verze clusterizace](cluster_map_archive/cluster_map_5.1.jpg)

[4.1 interaktivní verze clusterizace](cluster_map_archive/cluster_map_5.1.html)

Nyní se zkusíme ještě vrátit k nižšímu počtu clusterů - 24.
Výsledek:
![4.2 verze clusterizace](cluster_map_archive/cluster_map_5.2.jpg)

[4.2 interaktivní verze clusterizace](cluster_map_archive/cluster_map_5.2.html)

## 5. verze - přidání dat v angličtině (24 clusterů)
- Když už jsme zavedli překládání anotací a sylabů, které jsou v angličtině. Tak nyní můžeme zařadit i anotace v angličtině a dostaneme tak zpět i předměty, které jsme původně vyřazovali kvůli nedostatku dat. 
- Naše data tedy budou nyní vypadat takto: název, anotace cs, sylabus cs, anotace en, sylabus en. 
- Jednotlivá data projdeme, anglické anotace a sylaby překládáme do češtiny automaticky. A titulek, české sylaby a anotace jen v případě, že detekujeme angličtinu.

Výsledek:
![5. verze clusterizace](cluster_map_archive/cluster_map_6.0.jpg)

[5. interaktivní verze clusterizace](cluster_map_archive/cluster_map_6.0.html)

### Problémy
Nyní nám tu nově vykrystalizoval nový cluster s předměty vyučovanými v rámi Double-degree v Passau. Původně jsem tyto předměty držela u sebe v jednom clusteru, ale postupně jsem doiterovala k tomu, že jsem ve finále vyřadila slova "Pasov" a "Univerzit Pasov".

## 6. verze - experimentace s počtem clusterů a dalšími parametry
- Když už jsme doiterovali k nějakému finálnímu obrazu zpracování dat, začali jsme postupně zkoušet různé počty clusterů, parametry pro max a min DF a max features v rámci TF-IDF.
- Přidali jsme také možnost zamergovat clustery, pokud by byly příliš malé - opět pomocí nastavitelného parametru.
- Tady už se ty výsledky zas tak výrazně nelišili, pouze o drobné detaily.
- Níže se můžete podívat na různé výsledky, ve finále jsme skončili na 27 clusterech. 

Výsledek:
![6.1 verze clusterizace](cluster_map_archive/cluster_map_6.1.jpg)

[6.1 interaktivní verze clusterizace](cluster_map_archive/cluster_map_6.1.html)

![6.2 verze clusterizace](cluster_map_archive/cluster_map_6.2.jpg)

[6.2 interaktivní verze clusterizace](cluster_map_archive/cluster_map_6.2.html)

![6.3 verze clusterizace](cluster_map_archive/cluster_map_7.0.jpg)

[6.3 interaktivní verze clusterizace](cluster_map_archive/cluster_map_7.0.html)

![6.4 verze clusterizace](cluster_map_archive/cluster_map_7.1.jpg)

[6.4 interaktivní verze clusterizace](cluster_map_archive/cluster_map_7.1.html)

## Finální verze (27 clusterů)

![Finální verze clusterizace](cluster_map_archive/cluster_map_manual.jpg)

[Finální interaktivní verze clusterizace](cluster_map_archive/cluster_map_manual.html)

## Experiment s tuningem parametrů 
- Nejprve jsme si vyladili clusterizaci manuálně podle kombinace intuice a průzkumu dat. 
- Nyní jsme chtěli vyzkoušet, jaké nejlepší parametry můžeme použít podle etrik pro clusterizaci a primárně jsme se zaměřili na *Silhouette score*.

### Silhouette score

Pro každý bod v datech se počítají dvě základní hodnoty:

1. **$a(i)$ (Soudržnost):** Průměrná vzdálenost bodu ke všem ostatním bodům ve stejném shluku. Chceme, aby byla co nejmenší.
2. **$b(i)$ (Oddělení):** Průměrná vzdálenost bodu k bodům v nejbližším sousedním shluku. Chceme, aby byla co největší.

Samotný koeficient pro jeden bod se pak vypočítá pomocí vzorce: $$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$$

### Interpretace výsledku
Výsledek se vždy pohybuje v rozmezí od -1 do +1:
* **Blízko +1:** Bod je hluboko uvnitř svého shluku a daleko od ostatních. Shluky jsou jasně oddělené a husté.
* **Kolem 0:** Bod leží na hranici mezi dvěma shluky. Data jsou pravděpodobně překrytá a rozdělení není úplně jednoznačné.
* **Záporné hodnoty (k -1):** Špatně. Bod je pravděpodobně v nesprávném shluku a je blíže sousední skupině než té své.

### Výsledek
Nejlepší výsledek jsme dostali podle *silhouette score* pro tyto parametry:
- počet clusterů: 95
- minimální velikost clusteru: 15
- max features pro TF-IDF: 7000
- min_df: 0.3
- max_df: 10

Výsledek byl: 0.036881

![Finální verze clusterizace podle silhouette score](cluster_map_archive/cluster_map_params.jpg)

[Finální interaktivní verze clusterizace podle silhouette score](cluster_map_archive/cluster_map_params.html)

### Top 10 nastavení parametrů podle *silhouette score*
| n_clusters | max_features | min_df | max_df | min_cluster_size | silhouette |
| :--- | :--- | :--- | :--- | :--- |  :--- |
| 95 | 7000 | 10 | 0.3 | 15 | 0.03688 |
| 95 | 10000 | 10 | 0.3 |  15 | 0.03688 |
| 95 | 5000 | 10 | 0.3 |  15 | 0.03688 |
| 90 | 5000 | 5 | 0.11 |  15 | 0.03679 |
| 80 | 5000 | 2 | 0.2 |  15 | 0.03640 |
| 95 | 5000 | 7 | 0.11 |  15 | 0.03624 |
| 100 | 5000 | 2 | 0.15 |  15 | 0.03622 |
| 95 | 5000 | 2 | 0.3 |  15 | 0.03617 |
| 95 | 5000 | 10 | 0.11 |  15 | 0.03617 |
| 95 | 10000 | 10 | 0.11 |  15 | 0.03617 |


## Zhodnocení 
Pro jakékoliv interaktivní využití pro studenty je určitě vhodnější nižší počet clusterů, okolo těch 30. Naším cílem totiž v tomto případě není co nejpřesnější clusterizace, ale také přehlednost, která se s rostoucím počtem clusterů ztrácí. 

Při detailním pohledu ale 95 clusterů působí opravdu velmi přesně, např. jazyky se nám rozdělili na akademickou agličtinu, běžnou angličtinu a ostatní cizí jazyky. Nebo se např. matematická analýza 1 a 2 rozdělila do dvou clusterů. Při bližším zkoumání vidíme, že v jednom clusteru jsou nyní už opravdu jen předměty, které velmi úzce souvisí.







