# SubjectClustering MFF UK

Tento projekt slouží k automatické clusterizaci předmětů vyučovaných na Matematicko-fyzikální fakultě Univerzity Karlovy. Na základě textových dat (název, anotace, sylabus) seskupuje podobné předměty do logických celků a vizualizuje je v interaktivní mapě.

Projekt vznikl jako součást vývoje doporučovacího systému **RecSIS**.

## Instalace a spuštění

1. **Instalace závislostí:**
Využijte připravený seznam knihoven:
```bash
pip install -r requirements_research.txt
```

2. **Příprava dat:**
V `config.py` nastavte připojení k databázi (`DB_CONNECTION`). Pokud nemáte přístup k DB, skript se pokusí načíst lokální CSV soubory definované tamtéž.
3. **Spuštění analýzy:**
```bash
python main.py
```


4. **Ladění parametrů (volitelné):**
Pokud chcete spustit Grid Search pro nalezení lepšího Silhouette Score:
```bash
python tune_params.py
```

5. **Spuštění dashboardu:**
```bash
python dashboard.py
```

Aplikace poběží na `http://127.0.0.1:8050`.

---

## Metodika a výsledky

Projekt používá dvoufázovou redukci dimenzionality pro vizualizaci:

1. **PCA** (Principal Component Analysis) zredukuje TF-IDF matici na 50 komponent pro zachování globální struktury a odstranění šumu.
2. **t-SNE** následně data převede do 2D prostoru pro lidsky čitelnou mapu.

Aktuální nejlepší konfigurace (zapsaná v `config.py`) využívá 95 clusterů, což poskytuje nejlepší rovnováhu mezi granularitou témat a stabilitou shluků.
