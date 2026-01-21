import streamlit as st
import pandas as pd
import yfinance as yf
from data_loader import get_financial_data
from analytics import (
    calculate_returns, 
    get_statistics,
    run_backtesting, 
    test_normality, 
    add_technical_indicators
)
from visualizations import (
    plot_price_with_indicators,
    plot_returns_histogram,
    plot_qq_plot,
    plot_cumulative_returns,
    plot_equity_curve_with_drawdown
)

st.set_page_config(
    page_title="Nexus Crypto Finance Pro", 
    layout="wide",
    page_icon="💹",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# === Styles CSS ===
st.markdown("""
    <style>
    
    button[aria-label="View app menu"] {
        display: none !important;
    }
    
    .stApp {
        background-color: #0e1117 !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: #0e1117 !important;
    }
        
    h1, h2, h3, .stMarkdown p, .stMarkdown li {
        color: white !important;
    }
    
    [data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.1) !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        padding: 15px !important;
        border-radius: 12px !important;
    }
    
    .stButton > button[kind="primary"] {
        background-color: #f0b90b !important;
        color: black !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #ffd700 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(240, 185, 11, 0.4) !important;
    }
    
    button[data-testid="baseButton-secondary"] {
        background-color: transparent !important;
        color: #f0b90b !important;
        border: 2px solid #f0b90b !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    button[data-testid="baseButton-secondary"]:hover {
        background-color: #f0b90b !important;
        color: black !important;
        transform: scale(1.02) !important;
    }
    
    .stSlider label {
        color: #f0b90b !important;
        font-weight: bold !important;
    }
    
    .stSlider > div > div > div > div {
        background-color: #f0b90b !important;
    }
    
    .stSlider [role="slider"] {
        background-color: #f0b90b !important;
    }
    
    .stSlider [data-baseweb="slider"] > div > div:first-child {
        background-color: #f0b90b !important;
    }
    
    .stSlider [data-testid="stTickBarMin"],
    .stSlider [data-testid="stTickBarMax"],
    .stSlider > div > div:last-child {
        color: #f0b90b !important;
    }
        
    .stSelectbox label {
        color: #f0b90b !important;
        font-weight: bold !important;
    }
    
    .stSelectbox > div > div {
        border-color: rgba(240, 185, 11, 0.3) !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #f0b90b !important;
        box-shadow: 0 0 0 1px #f0b90b !important;
    }
    
    .stSelectbox svg {
        fill: #f0b90b !important;
    }
    
    .stNumberInput label {
        color: #f0b90b !important;
        font-weight: bold !important;
    }
    
    .stNumberInput button:hover {
        background-color: #f0b90b !important;
        color: black !important;
    }
    
    .stNumberInput input:focus {
        border-color: #f0b90b !important;
        box-shadow: 0 0 0 1px #f0b90b !important;
    }
        
    .stTextInput label {
        color: #f0b90b !important;
        font-weight: bold !important;
    }
    
    .stTextInput input:focus {
        border-color: #f0b90b !important;
        box-shadow: 0 0 0 1px #f0b90b !important;
    }
        
    .stDateInput label {
        color: #f0b90b !important;
        font-weight: bold !important;
    }
    
    .stDateInput input:focus {
        border-color: #f0b90b !important;
        box-shadow: 0 0 0 1px #f0b90b !important;
    }
        
    .stTabs [data-baseweb="tab-list"] button {
        color: white !important;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #f0b90b !important;
        border-bottom: 2px solid #f0b90b !important;
    }
    
    .stTabs [data-baseweb="tab-list"] button:hover {
        color: #f0b90b !important;
    }   
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: white !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #1e2329 !important;
    }
    
    input:hover, select:hover {
        border-color: #f0b90b !important;
    }
    </style>
""", unsafe_allow_html=True)

def get_crypto_price(symbol):
    
    try:
        ticker_data = yf.Ticker(symbol)
        df = ticker_data.history(period="2d")
        if len(df) < 2: return 0.0, 0.0
        
        current_price = df['Close'].iloc[-1]
        prev_close = df['Close'].iloc[-2]
        change = ((current_price - prev_close) / prev_close) * 100
        return current_price, change
    except:
        return 0.0, 0.0

with st.sidebar:
    st.markdown("## <span style='color: #f0b90b;'>Nexus Cryptocurrency Finance Pro</span>", unsafe_allow_html=True)
    
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/5968/5968260.png", width=100)
    st.sidebar.markdown("---")
    
    if st.button("Dashboard", use_container_width=True, key="home_btn"):
        st.rerun()
    st.sidebar.markdown("---")
    
    # === Configuration de la Stratégie ===
    st.sidebar.header("⚙️ Stratégie de Trading")
    strategy_choice = st.sidebar.selectbox(
        "Choisir une méthode",
        ["SMA Crossover (Trend)", "RSI Mean Reversion", "Buy & Hold","Elliott & Fibonacci - Analyse Prédictive Pro"]
    )
    
    # === Paramètres Financiers ===
    st.sidebar.header("💰 Paramètres Financiers")
    initial_capital = st.sidebar.number_input("Capital Initial ($)", min_value=100, value=1000, step=100)
    transaction_fee = st.sidebar.slider("Frais de Transaction (%)", min_value=0.0, max_value=1.0, value=0.1, step=0.05) / 100
    
    # === Sélection Crypto ===
    st.header("🔍 Sélection Crypto")
    ticker_input = st.sidebar.text_input("Saisir le Symbole (ex: BTC, ETH, SOL)", value="BTC").upper()
    ticker = f"{ticker_input.upper().strip()}-USD"
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        start_date = st.date_input("Du", value=pd.to_datetime("2023-01-01"))
    with col_d2:
        end_date = st.date_input("Au")
    
    analyze_btn = st.button("Lancer l'Analyse ", use_container_width=True, type="primary")
  
# === PAGE PRINCIPALE ===

if 'analyze_btn' in locals() and analyze_btn:
    if strategy_choice == "Elliott & Fibonacci - Analyse Prédictive Pro":
        st.markdown(f"""
            <div style="background-color: #1e2329; padding: 40px; border-radius: 15px; border: 2px solid #f0b90b; text-align: center; margin-top: 20px;">
                <h1 style="color: #f0b90b;">🚀 Elliott & Fibonacci</h1>
                <h3 style="color: white;">Analyse Prédictive en cours d'intégration</h3>
                <p style="color: #848e9c; font-size: 18px;">
                    Les algorithmes de détection automatique des vagues et des niveaux d'or 
                    seront disponibles dans la prochaine mise à jour (v2.1).
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.stop() 
        
    st.markdown("""
        <div style='padding: 10px 0; margin-bottom: 20px;'>
            <span style='color: #848e9c;'>Dashboard</span>
            <span style='color: #848e9c;'> > </span>
            <span style='color: #f0b90b; font-weight: bold;'>Analyse </span>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div style='padding: 10px 0; margin-bottom: 20px;'>
            <span style='color: #f0b90b; font-weight: bold;'>Dashboard</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #f0b90b;'> Nexus Cryptocurrency Finance Pro</h1>", unsafe_allow_html=True)

if not analyze_btn:
    # === PAGE D'ACCUEIL ===
    col_intro, col_anim = st.columns([2, 1])

    with col_intro:
        st.info("👋 Bienvenue sur **Nexus Crypto Finance Pro**")
        
        st.markdown("### 📈 Indicateurs Techniques Avancés")
        st.write("✅ **SMA & EMA** - Moyennes Mobiles")
        st.write("✅ **RSI** - Relative Strength Index")
        st.write("✅ **MACD** - Moving Average Convergence Divergence")
        st.write("✅ **Bollinger Bands** - Bandes de Volatilité")
        
        st.markdown("### 📊 Analyses Statistiques Avancées")
        st.write("✅ **Distribution des Rendements** - Histogramme & Densité")
        st.write("✅ **QQ-Plot** - Test de Normalité Visuel")
        st.write("✅ **Rendements Cumulés** - Performance dans le Temps")
        st.write("✅ **Percentiles** - Analyse des Risques")
        
        st.markdown("### 💼 Backtesting Professionnel")
        st.write("✅ **Frais de Transaction** - Simulation Réaliste")
        st.write("✅ **Ratio de Sharpe** - Rendement Ajusté au Risque")
        st.write("✅ **Taux de Réussite** - % de Trades Gagnants")
        st.write("✅ **Drawdown** - Perte Maximale")

    with col_anim:
        st.markdown("<p style='color: #848e9c; font-weight: bold;'>📊 Live Crypto Market</p>", unsafe_allow_html=True)
        
        cryptos = {
            "BTC-USD": "Bitcoin", 
            "ETH-USD": "Ethereum", 
            "SOL-USD": "Solana", 
            "XRP-USD": "XRP",
            "BNB-USD": "BNB"
        }

        for sym, name in cryptos.items():
            price, change = get_crypto_price(sym)
            logo_id = sym.split("-")[0].lower()
            
            if logo_id == "xrp":
                logo_url = "https://cryptologos.cc/logos/xrp-xrp-logo.png?v=024"
            elif logo_id == "bnb":
                logo_url = "https://cryptologos.cc/logos/bnb-bnb-logo.png"
            else:
                logo_url = f"https://cryptologos.cc/logos/{name.lower()}-{logo_id}-logo.png"

            status_color = "#00ff00" if change >= 0 else "#ff4b4b"
            arrow = "▲" if change >= 0 else "▼"
            
            st.markdown(f"""
                <div style="background-color: #1e2329; padding: 15px; border-radius: 10px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <img src="{logo_url}" width="35">
                        <div style="color: white; font-weight: bold;">{name}</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: white; font-weight: bold;">${price:,.2f}</div>
                        <div style="color: {status_color}; font-weight: bold;">{arrow} {change:.2f}%</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

else:
    # === ANALYSE COMPLÈTE ===
    with st.spinner('🔄 Chargement et analyse des données...'):
        full_data = get_financial_data(ticker)

        if full_data is None or full_data.empty:
            st.error(f"❌ Impossible de trouver {ticker}. Vérifiez le symbole.")
        else:
            actual_start = max(full_data.index.min().date(), start_date)
            actual_end = min(full_data.index.max().date(), end_date)
            data = full_data.loc[actual_start:actual_end].copy()
            data = data.loc[:, ~data.columns.duplicated()].copy()
    
            if not data.empty:
                # === Calculs ===
                data = calculate_returns(data)
                data = add_technical_indicators(data)
                metrics = get_statistics(data)
                p_val = test_normality(data)
                
                st.success(f"✅ Analyse réussie pour {ticker}")
                
                # === TAB LAYOUT (Organisation Professionnelle) ===
                tab1, tab2, tab3, tab4 = st.tabs([
                    "📈 Graphiques Techniques", 
                    "📊 Analyses Statistiques", 
                    "💼 Backtesting", 
                    "📋 Données"
                ])
                
                # ============================================
                # TAB 1: GRAPHIQUES TECHNIQUES
                # ============================================
                with tab1:
                    st.plotly_chart(
                        plot_price_with_indicators(data, ticker),
                        use_container_width=True
                    )
                
                # ============================================
                # TAB 2: ANALYSES STATISTIQUES (NOUVEAU)
                # ============================================
                with tab2:
                    st.write("### 📊 Statistiques Descriptives Complètes")
                    
                    # Métriques principales
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Moyenne", f"{metrics['Moyenne']:.4f}")
                    col2.metric("Médiane", f"{metrics['Médiane']:.4f}")
                    col3.metric("Écart-type", f"{metrics['Écart-type']:.4f}")
                    col4.metric("Volatilité Annuelle", f"{metrics['Volatilité Annuelle']:.2%}")
                    
                    # Moments statistiques
                    col5, col6, col7, col8 = st.columns(4)
                    col5.metric("Skewness", f"{metrics['Skewness']:.3f}")
                    col6.metric("Kurtosis", f"{metrics['Kurtosis']:.3f}")
                    col7.metric("Min", f"{metrics['Minimum']:.4f}")
                    col8.metric("Max", f"{metrics['Maximum']:.4f}")
                    
                    # Percentiles (NOUVEAU)
                    st.write("#### 📏 Analyse des Percentiles")
                    perc_col1, perc_col2, perc_col3, perc_col4 = st.columns(4)
                    perc_col1.metric("5ème Percentile", f"{metrics['Percentile_5']:.4f}")
                    perc_col2.metric("25ème Percentile", f"{metrics['Percentile_25']:.4f}")
                    perc_col3.metric("75ème Percentile", f"{metrics['Percentile_75']:.4f}")
                    perc_col4.metric("95ème Percentile", f"{metrics['Percentile_95']:.4f}")
                    
                    st.markdown("---")
                    
                    # Test de normalité
                    st.write("### 🧪 Test de Normalité (Shapiro-Wilk)")
                    if p_val < 0.05:
                        st.error(f"❌ Les rendements ne suivent PAS une distribution normale (p-value: {p_val:.4f})")
                    else:
                        st.success(f"✅ Les rendements suivent une distribution normale (p-value: {p_val:.4f})")
                    
                    st.markdown("---")
                    
                    # === GRAPHIQUES STATISTIQUES  ===
                    st.write("### 📉 Visualisations Statistiques")
                    
                    # Histogramme + Densité
                    st.plotly_chart(plot_returns_histogram(data), use_container_width=True)
                    
                    # QQ-Plot
                    st.plotly_chart(plot_qq_plot(data), use_container_width=True)
                    
                    # Rendements Cumulés
                    st.plotly_chart(plot_cumulative_returns(data), use_container_width=True)
                
                # ============================================
                # TAB 3: BACKTESTING (AMÉLIORÉ)
                # ============================================
                with tab3:
                    st.write(f"### 💼 Backtesting: {strategy_choice}")
                    st.info(f"💰 Capital Initial: ${initial_capital:,.0f} | 💸 Frais: {transaction_fee*100:.2f}%")
                    
                    # Backtesting avancé
                    data_backtest, final_perf, max_drawdown, num_trades, profit_factor, sharpe_ratio, win_rate, journal = run_backtesting(
                        data, initial_capital, strategy_choice, transaction_fee
                    )
                    
                    # Graphique Equity + Drawdown
                    st.plotly_chart(
                        plot_equity_curve_with_drawdown(data_backtest, initial_capital),
                        use_container_width=True
                    )
                    
                    # Métriques de Performance 
                    st.write("#### 📊 Métriques de Performance")
                    
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Rendement Total", f"{final_perf:.2%}")
                    m2.metric("Max Drawdown", f"{max_drawdown * 100:.2f}%")
                    m3.metric("Nombre de Trades", int(num_trades))
                    m4.metric("Profit Factor", f"{profit_factor:.2f}")
                    
                    #  Métriques
                    m5, m6, m7, m8 = st.columns(4)
                    m5.metric("Ratio de Sharpe", f"{sharpe_ratio:.2f}")
                    m6.metric("Taux de Réussite", f"{win_rate * 100:.1f}%")
                    
                    final_val = data_backtest['Equity_Curve'].iloc[-1]
                    total_fees = (data_backtest['Transaction_Cost'] * data_backtest['Equity_Curve'].shift(1)).sum()
                    
                    m7.metric("Capital Final", f"${final_val:,.2f}")
                    m8.metric("Frais Totaux", f"${total_fees:,.2f}")
                    
                    # Interprétation automatique
                    st.markdown("---")
                    st.write("#### 🔍 Interprétation des Résultats")
                    
                    interp = []
                    if final_perf > 0:
                        interp.append(f"✅ La stratégie est **profitable** avec un gain de {final_perf:.2%}")
                    else:
                        interp.append(f"❌ La stratégie est **perdante** avec une perte de {final_perf:.2%}")
                    
                    if sharpe_ratio > 1:
                        interp.append(f"✅ Bon ratio risque/rendement (Sharpe = {sharpe_ratio:.2f})")
                    else:
                        interp.append(f"⚠️ Ratio risque/rendement faible (Sharpe = {sharpe_ratio:.2f})")
                    
                    if win_rate > 0.5:
                        interp.append(f"✅ Taux de réussite supérieur à 50% ({win_rate*100:.1f}%)")
                    else:
                        interp.append(f"⚠️ Taux de réussite inférieur à 50% ({win_rate*100:.1f}%)")
                    
                    for item in interp:
                        st.write(item)
                    
                    # Journal des Transactions 
                    st.markdown("---")
                    st.write("#### 📜 Journal des Transactions")
                    
                    if not journal.empty:
                        format_dict = {
                            'Prix_Execution': '{:.2f} $',
                            'Frais': '{:.2f} $',
                            'Cumulative_Returns': '{:.2%}'
                        }
                        journal_unique = journal.loc[:, ~journal.columns.duplicated()].copy()
                        st.dataframe(journal_unique.style.format(format_dict), use_container_width=True)
                    else:
                        st.info("Aucune transaction effectuée.")
                    
                    # Logique de la stratégie
                    with st.expander("📖 Voir la Logique de la Stratégie"):
                        if strategy_choice == "SMA Crossover (Trend)":
                            st.write("- 🟢 **Achat** : SMA(20) > SMA(50)")
                            st.write("- 🔴 **Vente** : SMA(20) < SMA(50)")
                        elif strategy_choice == "RSI Mean Reversion":
                            st.write("- 🟢 **Achat** : RSI < 30 (Survendu)")
                            st.write("- 🔴 **Vente** : RSI > 70 (Suracheté)")
                        else:
                            st.write("- 🟢 **Achat** : Début de période")
                            st.write("- 🔴 **Vente** : Fin de période")
                            
                # ============================================
                # TAB 4: DONNÉES BRUTES
                # ============================================
                with tab4:
                    st.write("### 📋 Données Historiques")
                    st.dataframe(data.tail(100), use_container_width=True)
                    
                    st.download_button(
                        "📥 Télécharger CSV Complet",
                        data.to_csv(),
                        f"{ticker}_{start_date}_{end_date}.csv",
                        mime="text/csv"
                    )