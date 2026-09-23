# 🇪🇺 Dashboard FEDER Europe — DROM & COM

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75.svg)](https://plotly.com/)
[![Data Source](https://img.shields.io/badge/Data-Cohesion%20Open%20Data-003399.svg)](https://cohesiondata.ec.europa.eu/)
[![Made with ❤️](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F-red.svg)](#)

> **Analyse complète des programmes FEDER / FSE / FEADER dans les Départements et Régions d'Outre-Mer (DROM) et Collectivités d'Outre-Mer (COM) — Période 2014-2027**

---

## 📋 Table des matières

- [À propos](#-à-propos)
- [Fonctionnalités](#-fonctionnalités)
- [Sources de données](#-sources-de-données)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Structure du projet](#-structure-du-projet)
- [Programmes analysés](#-programmes-analysés)
- [Méthodologies](#-méthodologies)
- [Contribuer](#-contribuer)
- [Licence](#-licence)
- [Auteur](#-auteur)

---

## 🎯 À propos

Ce projet fournit **trois dashboards Streamlit** et un **dashboard HTML autonome** pour analyser les fonds européens structurels et d'investissement (ESI Funds) dans les territoires ultramarins français.

### Ce que vous pouvez faire

- 📊 **Visualiser** les budgets, dépenses et taux d'absorption des programmes FEDER / FSE / FEADER
- 🔍 **Comparer** les 5 DROM (Guadeloupe, Martinique, Guyane, La Réunion, Mayotte) et les COM
- 📈 **Analyser** l'évolution annuelle des financements 2014-2023
- 🔮 **Prédire** les tendances budgétaires avec régression linéaire
- ⚠️ **Évaluer** les risques par programme avec scoring multi-critères
- 💰 **Calculer** le ROI multi-dimensionnel (emploi, PME, social)
- 🎯 **Segmenter** les territoires par clustering K-means

---

## ✨ Fonctionnalités

| Fonctionnalité | Description |
|----------------|-------------|
| 🗺️ **Tableau de bord territorial** | Métriques par territoire (population, PIB, chômage, IDH) |
| 📊 **Analyse comparative** | Comparaison inter-programmes et inter-fonds |
| ⚡ **Efficacité** | Coût par emploi, efficacité projet, taux d'absorption |
| 🏆 **Performance** | Radar multi-critères (innovation, inclusion, durabilité) |
| ⚠️ **Risques** | 6 facteurs de risque + mesures d'atténuation |
| 💰 **ROI** | Retour sur investissement pondéré (emploi 40%, PME 30%, social 30%) |
| 🔮 **Prédictions** | Régression linéaire avec intervalles de confiance 95% |
| 🎯 **Clustering** | Segmentation des territoires par K-means |
| 🔗 **Corrélations** | Matrice de corrélation des indicateurs |
| 🌐 **API européenne** | Données réelles de Cohesion Open Data |

---

## 📡 Sources de données

Ce projet utilise l'**API officielle** de la Commission européenne :

| Source | URL | Usage |
|--------|-----|-------|
| **Cohesion Open Data** | [cohesiondata.ec.europa.eu](https://cohesiondata.ec.europa.eu/) | Données financières des programmes ESI |
| **Dataset ESIF 2014-2020** | [99js-gm52](https://cohesiondata.ec.europa.eu/datasets/99js-gm52) | Implémentation financière détaillée |
| **Kohesio** | [kohesio.ec.europa.eu](https://kohesio.ec.europa.eu/) | Données projet par projet |
| **Portail FEDER** | [ec.europa.eu/regional_policy](https://ec.europa.eu/regional_policy/) | Informations programmes 2021-2027 |

### API Socrata (SODA 2.1)

```bash
# Exemple : tous les programmes français
curl "https://cohesiondata.ec.europa.eu/resource/99js-gm52.json?\$where=ms='FR'&\$limit=50000"
```

---

## 🚀 Installation

### Prérequis

- **Python** 3.8 ou supérieur
- **pip** et **venv** (recommandé)
- **Git** pour cloner le dépôt

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/gunout/Dashboard-FEDER_Europe-DROM-COM.git
cd Dashboard-FEDER_Europe-DROM-COM

# 2. Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Télécharger les données
python3 scrap.py
```

### Dépendances principales

```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
requests>=2.31.0
scikit-learn>=1.3.0
scipy>=1.11.0
matplotlib>=3.7.0
seaborn>=0.12.0
```

---

## 💻 Utilisation

### Dashboard Streamlit (3 versions)

```bash
# 1. Dashboard de base — Données réelles
streamlit run Dashboard.py

# 2. Dashboard avancé — Analyses prédictives
streamlit run Dash.py

# 3. Dashboard complet — Analyses de base + avancées
streamlit run Final.py
```

Chaque dashboard s'ouvre automatiquement sur `http://localhost:8501`.

### Dashboard HTML autonome

```bash
# Ouvrir directement dans le navigateur
open dashboard.html   # macOS
# xdg-open dashboard.html   # Linux
# start dashboard.html      # Windows
```

### Scraper les données

```bash
# Télécharger les données FEDER pour la France
python3 scrap.py

# Filtrer uniquement les DROM/COM
python3 filter_ultramarin.py

# Calculer les budgets réels
python3 budgets.py
```

---

## 📁 Structure du projet

```
Dashboard-FEDER_Europe-DROM-COM/
│
├── 📄 Dashboard.py              # Dashboard de base
├── 📄 Dash.py                   # Dashboard avancé
├── 📄 Final.py                  # Dashboard complet
├── 📄 scrap.py                  # Scraper API Cohesion Open Data
├── 📄 filter_ultramarin.py      # Filtrage DROM/COM
├── 📄 budgets.py                # Calcul budgets réels
│
├── 📄 dashboard.html            # Dashboard HTML autonome
├── 📄 index.html                # Page de présentation
│
├── 📄 feder_data.json           # Données brutes (France entière)
├── 📄 feder_ultramarin.json     # Données filtrées DROM/COM
├── 📄 budget_ultramarin.json    # Budgets consolidés
│
├── 📄 requirements.txt          # Dépendances Python
├── 📄 LICENSE                   # Licence MIT
├── 📄 README.md                 # Ce fichier
└── 📄 .gitignore                # Fichiers ignorés
```

---

## 🗺️ Programmes analysés

### Programmes 2014-2020 (données réelles)

| Code CCI | Territoire | Fonds | Contribution UE |
|----------|-----------|-------|----------------|
| `2014FR05M2OP001` | Guadeloupe + St-Martin | ERDF, ESF | 60,15 M€ |
| `2014FR05SFOP003` | Guyane | ESF | 34,53 M€ |
| `2014FR05SFOP004` | Martinique | ESF | 59,86 M€ |
| `2014FR05SFOP005` | La Réunion | ESF | 237,64 M€ |
| `2014FR06RDRP001` | Guadeloupe | EAFRD | 51,97 M€ |
| `2014FR06RDRP002` | Martinique | EAFRD | 62,13 M€ |
| `2014FR06RDRP003` | Guyane | EAFRD | 35,77 M€ |
| `2014FR06RDRP004` | La Réunion | EAFRD | 108,66 M€ |
| `2014FR06RDRP006` | Mayotte | EAFRD | 21,23 M€ |
| **TOTAL** | **5 territoires** | **3 fonds** | **671,91 M€** |

### Programmes 2021-2027

| Programme | Territoire | Budget | Contribution UE |
|-----------|-----------|--------|----------------|
| **FEDER - DROM** | 5 DROM | 1 250 M€ | 937,5 M€ |
| **FEDER - COM** | 5 COM | 350 M€ | 262,5 M€ |

---

## 🧪 Méthodologies

### Analyse prédictive

- **Régression linéaire** simple (`sklearn.linear_model.LinearRegression`)
- **Intervalles de confiance** à 95% (± 1,96 σ)
- **R²** pour évaluer la qualité du modèle

### Clustering

- **Standardisation** des données (`StandardScaler`)
- **K-means** avec k=3 (`sklearn.cluster.KMeans`)
- Segmentation : développé / en transition / en développement

### Analyse de risques

- **6 facteurs** : budgétaire, opérationnel, environnemental, social, politique, exécution
- **Score global** = moyenne pondérée
- **Catégorisation** : faible (<0,2) / moyen (0,2-0,3) / élevé (>0,3)

### Calcul du ROI

```
ROI_Emploi  = (Emplois × 35 000 €) / Budget
ROI_PME     = (PME × 50 000 €) / Budget
ROI_Social  = (Bénéficiaires × 5 000 €) / Budget
ROI_Total   = 0,4 × ROI_Emploi + 0,3 × ROI_PME + 0,3 × ROI_Social
```

---

## 🤝 Contribuer

Les contributions sont **les bienvenues** ! Voici comment procéder :

```bash
# 1. Fork le projet
# 2. Créer une branche
git checkout -b feature/ma-nouvelle-fonctionnalite

# 3. Commit les changements
git commit -m "feat: ajout d'une nouvelle analyse"

# 4. Push
git push origin feature/ma-nouvelle-fonctionnalite

# 5. Ouvrir une Pull Request
```

### Standards de code

- **PEP 8** pour Python
- **Docstrings** pour toutes les fonctions
- **Type hints** quand c'est pertinent
- **Tests** pour les nouvelles fonctionnalités

---

## 📄 Licence

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 👤 Auteur

**Gleaphe** — 2025

[![GitHub](https://img.shields.io/badge/GitHub-gunout-181717?logo=github)](https://github.com/gunout)

---

## 🙏 Remerciements

- 🇪🇺 **Commission européenne** pour les données ouvertes
- 📊 **Streamlit** pour le framework de dashboard
- 📈 **Plotly** pour les visualisations interactives
- 🐍 **Python** et sa communauté

---

## 📚 Ressources

- [Documentation FEDER 2021-2027](https://ec.europa.eu/regional_policy/fr/2021_2027/)
- [Cohesion Open Data](https://cohesiondata.ec.europa.eu/)
- [Kohesio — Projets financés](https://kohesio.ec.europa.eu/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python](https://plotly.com/python/)

---

<div align="center">

**⭐ Si ce projet vous est utile, n'oubliez pas de lui donner une étoile ! ⭐**

🇪🇺 Fait avec ❤️ pour les territoires ultramarins

</div>

---




# Dashboard-FEDER_Europe-DROM-COM // STREAMLIT .
3 🇪🇺 DASHBOARD FEDER EUROPE Fonds Européen de Développement Régional - Analyse des Programmes 2014-2027

<img width="662" height="465" alt="Screenshot_2025-10-16_18-21-05" src="https://github.com/user-attachments/assets/765758bb-66df-4239-99f9-ac5e411733ea" />

# EXAMPLE
<img width="1280" height="1024" alt="Screenshot_2025-10-16_12-40-51" src="https://github.com/user-attachments/assets/13af0913-d26b-4aab-9e6b-e348bff5c430" />
<img width="1280" height="1024" alt="Screenshot_2025-10-16_12-43-26" src="https://github.com/user-attachments/assets/62ef5895-9ef7-4274-8c33-8a1c36362281" />
<img width="1280" height="1024" alt="Screenshot_2025-10-16_12-43-57" src="https://github.com/user-attachments/assets/ff858fdc-387b-44c0-a911-1681220246f9" />
<img width="1280" height="1024" alt="Screenshot_2025-10-16_12-44-12" src="https://github.com/user-attachments/assets/f3654209-967d-4253-ad48-0efbfd1254da" />

# INSTALL DEPENDENCIES 

    pip install streamlit pandas numpy plotly requests scikit-learn seaborn matplotlib scipy

1 . # RUN PROGRAM 🇪🇺 DASHBOARD FEDER EUROPE
Fonds Européen de Développement Régional - Analyse des Programmes 2014-2027

    streamlit run Dashboard.py

<img width="662" height="465" alt="Screenshot_2025-10-16_18-21-38" src="https://github.com/user-attachments/assets/4a2de291-7422-4e98-b3eb-e67ca1382a80" />

# EXAMPLE
<img width="1280" height="1024" alt="Screenshot_2025-10-16_18-17-17" src="https://github.com/user-attachments/assets/9f47fa54-f6f7-4c57-b2f3-d80cdf1c3ddb" />
<img width="1280" height="1024" alt="Screenshot_2025-10-16_18-17-34" src="https://github.com/user-attachments/assets/330ba508-5d6f-4a31-a854-679ca5efe2dc" />
<img width="1280" height="1024" alt="Screenshot_2025-10-16_18-18-17" src="https://github.com/user-attachments/assets/97709635-6476-4ff2-a3e5-d822e139a0e7" />
<img width="1280" height="1024" alt="Screenshot_2025-10-16_18-18-36" src="https://github.com/user-attachments/assets/6a011a79-77af-496a-a31e-80d8d784c4d3" />
<img width="1280" height="1024" alt="Screenshot_2025-10-16_18-18-53" src="https://github.com/user-attachments/assets/dbf6a089-93b1-4eb9-989d-f3165444d775" />

2 . # RUN PROGRAM 🇪🇺 DASHBOARD FEDER EUROPE - ANALYSES AVANCÉES
Fonds Européen de Développement Régional - Analyses Avancées et Prédictives

    streamlit run Dash.py

<img width="662" height="465" alt="Screenshot_2025-10-16_18-22-08" src="https://github.com/user-attachments/assets/a3d89250-52ec-4708-8b47-ecee44a6290f" />

# EXAMPLE 
<img width="1280" height="1024" alt="Screenshot_2025-10-16_18-19-43" src="https://github.com/user-attachments/assets/43d44ec8-3ee2-43cb-bffb-bd0194c26480" />
<img width="1280" height="1024" alt="Screenshot_2025-10-16_18-19-52" src="https://github.com/user-attachments/assets/5ad7bc93-4627-4e5c-a43c-e2f6dbcb21c2" />
<img width="1280" height="1024" alt="Screenshot_2025-10-16_18-20-08" src="https://github.com/user-attachments/assets/66df721c-bc9a-4af4-8957-966fff935b31" />
<img width="1280" height="1024" alt="Screenshot_2025-10-16_18-20-14" src="https://github.com/user-attachments/assets/b7715aa1-0b96-4afd-97e5-1725a8d12ffd" />

3 . # RUN PROGRAM 🇪🇺 DASHBOARD FEDER EUROPE - ANALYSES COMPLÈTES
Fonds Européen de Développement Régional - Analyses de Base et Avancées

    streamlit run Final.py 

---

<div align="center">

### 🇫🇷 Gunout · 2026

![Made in France](https://img.shields.io/badge/Made_in-France-002395?style=flat-square&labelColor=FFFFFF&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA5MDAgNjAwIj48cmVjdCB3aWR0aD0iOTAwIiBoZWlnaHQ9IjYwMCIgZmlsbD0iIzAwMjM5NSIvPjxyZWN0IHdpZHRoPSI5MDAiIGhlaWdodD0iNDAwIiB5PSIxMDAiIGZpbGw9IiNmZmYiLz48cmVjdCB3aWR0aD0iOTAwIiBoZWlnaHQ9IjIwMCIgeT0iNDAwIiBmaWxsPSIjZWQyOTM5Ii8+PC9zdmc+)
![GitHub](https://img.shields.io/badge/GitHub-gunout-181717?style=flat-square&logo=github&logoColor=white)
![Year](https://img.shields.io/badge/2026-ED2939?style=flat-square&labelColor=FFFFFF)

<sub>© 2026 <strong>Gunout</strong> — Tous droits réservés.</sub>

</div>

