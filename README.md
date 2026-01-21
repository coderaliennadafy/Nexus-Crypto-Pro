# 📊 Nexus Cryptocurrency Finance Pro

**Plateforme d'analyse financière avancée avec backtesting intégré**

---

## 📋 Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Fonctionnalités](#fonctionnalités)
3. [Installation](#installation)
4. [Utilisation](#utilisation)
5. [Architecture du Projet](#architecture-du-projet)
6. [Justifications Mathématiques](#justifications-mathématiques)
7. [Références et Inspirations](#références-et-inspirations)
8. [Difficultés Rencontrées](#difficultés-rencontrées)
9. [Améliorations Futures](#améliorations-futures)

---

## 🎯 Vue d'ensemble

Cette application est une plateforme complète d'analyse quantitative et technique des cryptomonnaies, développée dans le cadre du module **Mathématiques Appliquées au Traitement des Données**.

### Objectifs pédagogiques atteints :
✅ Manipulation de données financières sous forme matricielle  
✅ Calcul d'indicateurs financiers avec formules mathématiques explicites  
✅ Application des probabilités et statistiques aux rendements  
✅ Interprétation via graphiques professionnels  
✅ Développement d'une application interactive Python  
✅ Implémentation et test de stratégies de trading  

---

## 🚀 Fonctionnalités

### 1. **Acquisition des Données**
- ✅ Importation via **Yahoo Finance API** (yfinance)
- ✅ Support de multiples cryptos (BTC, ETH, SOL, XRP, BNB, etc.)
- ✅ Sélection de période personnalisée
- ✅ Données OHLC (Open, High, Low, Close)

### 2. **Traitement Mathématique**
- ✅ **Rendements arithmétiques** : `R_t = (P_t - P_{t-1}) / P_{t-1}`
- ✅ **Rendements logarithmiques** : `r_t = ln(P_t / P_{t-1})`
- ✅ **Rendements cumulés** : Évolution de la performance
- ✅ **Volatilité annualisée** : `σ_annuel = σ_quotidien × √252`

### 3. **Statistiques & Probabilités**
#### Statistiques descriptives :
- Moyenne, Médiane, Écart-type
- Maximum, Minimum
- **Skewness** (asymétrie) : `E[(R - μ)³] / σ³`
- **Kurtosis** (aplatissement) : `E[(R - μ)⁴] / σ⁴`
- **Percentiles** (5%, 25%, 75%, 95%)

#### Tests statistiques :
- **Test de Shapiro-Wilk** (normalité)
- Interprétation de la p-value

#### Visualisations :
- ✅ **Histogramme des rendements** avec courbe de densité normale
- ✅ **QQ-Plot** (Quantile-Quantile) pour évaluation visuelle de la normalité
- ✅ **Graphique des rendements cumulés**

### 4. **Indicateurs Techniques**

#### Moyennes Mobiles :
- **SMA** (Simple Moving Average) : `SMA_n(t) = (1/n) × Σ P_{t-i}`
- **EMA** (Exponential Moving Average) : `EMA_n(t) = α·P_t + (1-α)·EMA_{t-1}`

#### Indicateurs de Momentum :
- **RSI** (Relative Strength Index) : `RSI = 100 - 100/(1 + RS)`
  - RS = Moyenne des gains / Moyenne des pertes sur 14 périodes
  - Suracheté : RSI > 70
  - Survendu : RSI < 30

#### Indicateurs de Tendance :
- **MACD** (Moving Average Convergence Divergence) :
  - MACD = EMA(12) - EMA(26)
  - Signal = EMA(9) du MACD
  - Histogramme = MACD - Signal

#### Indicateurs de Volatilité :
- **Bandes de Bollinger** :
  - Bande supérieure = SMA(20) + 2×σ(20)
  - Bande inférieure = SMA(20) - 2×σ(20)

### 5. **Backtesting Professionnel**

#### Stratégies implémentées :
1. **SMA Crossover** (Trend Following)
   - Achat : SMA(20) > SMA(50)
   - Vente : SMA(20) < SMA(50)

2. **RSI Mean Reversion**
   - Achat : RSI < 30
   - Vente : RSI > 70

3. **Buy & Hold**
   - Achat au début, vente à la fin

#### Métriques de performance :
- ✅ **Rendement Total** : `(Capital_final - Capital_initial) / Capital_initial`
- ✅ **Max Drawdown** : Perte maximale depuis le pic
- ✅ **Profit Factor** : `Gains totaux / Pertes totales`
- ✅ **Ratio de Sharpe** : `(Rendement moyen / Écart-type) × √252`
- ✅ **Taux de Réussite** : `Nombre de trades gagnants / Total trades`
- ✅ **Frais de Transaction** : 0.1% par trade (configurable)

#### Visualisations :
- Courbe d'équité (évolution du capital)
- Graphique du Drawdown
- Journal détaillé des transactions

---

## 💻 Installation

### Prérequis :
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes :

```bash
# 1. Cloner ou télécharger le projet
git clone <url_du_projet>
cd nexus-crypto-finance

# 2. Créer un environnement virtuel (recommandé)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'application
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse : `http://localhost:8501`

---

## 📖 Utilisation

### Interface principale :

1. **Sidebar (Barre latérale)** :
   - Sélectionner une stratégie de trading
   - Configurer le capital initial (défaut: 1000$)
   - Ajuster les frais de transaction (défaut: 0.1%)
   - Saisir le symbole crypto (ex: BTC, ETH, SOL)
   - Choisir la période d'analyse

2. **Onglet "Graphiques Techniques"** :
   - Prix avec SMA(20), SMA(50) et Bandes de Bollinger
   - RSI (14 périodes)
   - MACD avec signal et histogramme

3. **Onglet "Analyses Statistiques"** :
   - Statistiques descriptives complètes
   - Test de normalité
   - Histogramme des rendements
   - QQ-Plot
   - Rendements cumulés

4. **Onglet "Backtesting"** :
   - Courbe d'équité
   - Métriques de performance
   - Interprétation automatique
   - Journal des transactions

5. **Onglet "Données"** :
   - Tableau des données historiques
   - Export CSV

---

## 📁 Architecture du Projet

```
nexus-crypto-finance/
│
├── app.py                   # Application principale Streamlit
├── data_loader.py           # Chargement des données (yfinance)
├── analytics.py             # Calculs mathématiques et backtesting
├── visualizations.py        # Graphiques Plotly
├── requirements.txt         # Dépendances Python
├── README.md               # Documentation (ce fichier)
└── .streamlit              # pour force mode dark 
```

### Description des modules :

#### `app.py`
- Interface utilisateur Streamlit
- Organisation en onglets (Tabs)
- Live market feed
- Orchestration des analyses

#### `data_loader.py`
- Récupération des données via yfinance
- Nettoyage et formatage
- Gestion des erreurs

#### `analytics.py`
- **Fonctions principales** :
  - `calculate_returns()` : Calcul des rendements
  - `add_technical_indicators()` : Ajout des indicateurs
  - `get_statistics()` : Statistiques descriptives
  - `run_backtesting()` : Simulation de trading
  - `calculate_sharpe_ratio()` : Ratio risque/rendement
  - `calculate_win_rate()` : Taux de réussite

#### `visualizations.py`
- **Graphiques Plotly** :
  - `plot_price_with_indicators()` : Prix + indicateurs
  - `plot_returns_histogram()` : Distribution
  - `plot_qq_plot()` : Test normalité
  - `plot_cumulative_returns()` : Performance
  - `plot_equity_curve_with_drawdown()` : Backtesting

---

## 🧮 Justifications Mathématiques

### 1. Rendements Logarithmiques vs Arithmétiques

**Pourquoi les rendements logarithmiques ?**

Les rendements logarithmiques sont **additifs dans le temps** :

```
r_total = r_1 + r_2 + ... + r_n

```

Contrairement aux rendements arithmétiques qui sont multiplicatifs.

De plus, ils sont **symétriques** :
- Une hausse de 50% suivie d'une baisse de 50% ne donne PAS 0%
- En log : ln(1.5) + ln(0.5) ≈ 0

### 2. Volatilité Annualisée

**Formule** : `σ_annuel = σ_quotidien × √252`

**Justification** : Basée sur la racine carrée du temps (hypothèse de marche aléatoire).
252 = nombre de jours de trading par an.

### 3. Ratio de Sharpe

**Formule** : `Sharpe = (Rendement moyen - Taux sans risque) / Écart-type × √252`

**Interprétation** :
- Sharpe > 1 : Bon ratio risque/rendement
- Sharpe > 2 : Excellent
- Sharpe < 1 : Médiocre

### 4. Bandes de Bollinger (±2σ)

**Justification statistique** : Si les rendements suivent une loi normale, environ **95%** des valeurs se trouvent dans l'intervalle [μ - 2σ, μ + 2σ].

### 5. Test de Shapiro-Wilk

**Hypothèse H0** : Les données suivent une distribution normale.
- Si p-value < 0.05 : On rejette H0 (distribution non-normale)
- Si p-value ≥ 0.05 : On ne peut pas rejeter H0

---

## 🌐 Références et Inspirations

### Plateformes professionnelles :

1. **TradingView** (https://tradingview.com)
   - Interface graphique interactive
   - Bibliothèque complète d'indicateurs
   - Backtesting intégré
   - **Inspirations adoptées** :
     - Layout multi-panneaux
     - Indicateurs superposables
     - Zoom et navigation

2. **Bloomberg Terminal**
   - Structure modulaire
   - Visualisations multi-fenêtres
   - Données en temps réel
   - **Inspirations adoptées** :
     - Organisation professionnelle
     - Métriques de performance

3. **Binance** (https://binance.com)
   - Dashboard crypto
   - API publique gratuite
   - **Inspirations adoptées** :
     - Live market feed
     - Interface minimaliste

### API et librairies utilisées :

- **Yahoo Finance API** (yfinance) : Données historiques
- **Plotly** : Graphiques interactifs
- **SciPy** : Tests statistiques
- **Streamlit** : Framework web Python

---

## 🚧 Difficultés Rencontrées

### 1. **Gestion du MultiIndex avec yfinance**
**Problème** : Lorsque plusieurs symboles sont téléchargés, yfinance retourne un DataFrame avec MultiIndex.

**Solution** : Détection et conversion automatique en colonnes simples :
```python
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)
```

### 2. **Calcul du Drawdown**
**Problème** : Le drawdown doit être calculé par rapport au **pic historique**, pas au jour précédent.

**Solution** : Utilisation de `cummax()` :
```python
roll_max = equity_curve.cummax()
drawdown = (equity_curve - roll_max) / roll_max
```

### 3. **Frais de Transaction Réalistes**
**Problème** : Les backtests sans frais donnent des résultats trop optimistes.

**Solution** : Déduction de 0.1% à chaque changement de position :
```python
df['Transaction_Cost'] = 0.0
df.loc[df['Trade_Action'] != 0, 'Transaction_Cost'] = 0.001
```

### 4. **Test de Normalité sur Petits Échantillons**
**Problème** : Shapiro-Wilk peut échouer avec moins de 20 observations.

**Solution** : Vérification de la taille avant le test :
```python
if len(returns) < 20:
    st.warning("Échantillon trop petit pour le test de normalité")
```

### 5. **Performance de l'Application**
**Problème** : Rechargement complet à chaque interaction.

**Solution** : Utilisation de `@st.cache_data` pour les fonctions coûteuses :
```python
@st.cache_data
def load_historical_data(symbol, start_date, end_date):
    ...
```

---

##  Améliorations Futures

### Court terme :
1.  Support de multiples actifs simultanés
2.  Matrice de corrélation entre cryptos
3.  Export des résultats en PDF
4.  Backtesting avec position sizing dynamique

### Moyen terme :
5.  Optimisation automatique des paramètres (grid search)
6.  Stratégies basées sur Machine Learning
7.  Connexion API Binance en temps réel
8.  Alertes par email/SMS

### Long terme :
9. Portfolio multi-actifs avec gestion du risque
10.  Analyse de sentiment (Twitter, Reddit)
11.  Support d'autres marchés (actions, forex, commodities)
12.  Version mobile responsive
13. ect...

---

##  Exemple d'Utilisation

### Cas pratique : Analyse BTC sur 1 an

```python
# Paramètres :
- Symbole : BTC-USD
- Période : 2023-01-01 → 2024-01-01
- Capital : 10,000 $
- Stratégie : SMA Crossover
- Frais : 0.1%

# Résultats attendus :
- Rendement Total : Variable selon marché
- Sharpe Ratio : ~1.2 (si marché haussier)
- Max Drawdown : ~15-20%
- Nombre de Trades : 10-15
- Taux de Réussite : ~55-60%
```

---

##  Auteur

**Projet réalisé dans le cadre du module :**  
*Mathématiques Appliquées au Traitement des Données*

**Encadrant :** M. Hamza Saber

---

##  Licence

Ce projet est à usage pédagogique uniquement.

---

##  Support

Pour toute question ou suggestion :
- Utiliser le bouton "Feedback" dans l'application
- Ouvrir une issue sur GitHub
- Contacter l'encadrant du projet

---

**Dernière mise à jour :** Janvier 2026
