import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy import stats

def plot_price_with_indicators(df, ticker):
    
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.5, 0.25, 0.25],
        subplot_titles=(f'{ticker} - Prix & Indicateurs', 'RSI', 'MACD')
    )
    
    fig.add_trace(
        go.Scatter(x=df.index, y=df['Portfolio_Close'], name='Prix', line=dict(color='#f0b90b', width=2)),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=df.index, y=df['SMA_20'], name='SMA 20', line=dict(color='#00ff00', width=1)),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=df.index, y=df['SMA_50'], name='SMA 50', line=dict(color='#ff4b4b', width=1)),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=df.index, y=df['BB_Upper'], name='BB Supérieure', 
                   line=dict(color='rgba(128,128,128,0.3)', dash='dash')),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=df.index, y=df['BB_Lower'], name='BB Inférieure', 
                   line=dict(color='rgba(128,128,128,0.3)', dash='dash'),
                   fill='tonexty', fillcolor='rgba(128,128,128,0.1)'),
        row=1, col=1
    )
    
    # === الرسم الثاني: RSI ===
    fig.add_trace(
        go.Scatter(x=df.index, y=df['RSI'], name='RSI', line=dict(color='#9467bd', width=2)),
        row=2, col=1
    )
    
    # خطوط RSI (30 و 70)
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
    
    # === الرسم الثالث: MACD ===
    fig.add_trace(
        go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color='#00bfff', width=2)),
        row=3, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=df.index, y=df['MACD_Signal'], name='Signal', line=dict(color='#ff6347', width=1)),
        row=3, col=1
    )
    
    fig.add_trace(
        go.Bar(x=df.index, y=df['MACD_Histogram'], name='Histogram', marker_color='#848e9c'),
        row=3, col=1
    )
    
    # تنسيق عام
    fig.update_layout(
        height=800,
        template='plotly_dark',
        showlegend=True,
        hovermode='x unified'
    )
    
    fig.update_xaxes(rangeslider_visible=False)
    
    return fig

def plot_returns_histogram(df):
   
    returns = df['Returns_Log'].dropna()
    
    fig = go.Figure()
    
    # Histogramme
    fig.add_trace(go.Histogram(
        x=returns,
        nbinsx=50,
        name='Rendements',
        marker_color='#f0b90b',
        opacity=0.7,
        histnorm='probability density'
    ))
    
    # Courbe de densité normale théorique
    mu = returns.mean()
    sigma = returns.std()
    x = np.linspace(returns.min(), returns.max(), 100)
    y = stats.norm.pdf(x, mu, sigma)
    
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines',
        name='Distribution Normale',
        line=dict(color='red', width=2)
    ))
    
    fig.update_layout(
        title='Distribution des Rendements Logarithmiques',
        xaxis_title='Rendements',
        yaxis_title='Densité',
        template='plotly_dark',
        showlegend=True,
        height=400
    )
    
    return fig

def plot_qq_plot(df):
    
    returns = df['Returns_Log'].dropna()
    
    # Calcul des quantiles
    theoretical_quantiles = stats.probplot(returns, dist="norm")[0][0]
    sample_quantiles = stats.probplot(returns, dist="norm")[0][1]
    
    fig = go.Figure()
    
    # Points QQ
    fig.add_trace(go.Scatter(
        x=theoretical_quantiles,
        y=sample_quantiles,
        mode='markers',
        name='Données',
        marker=dict(color='#f0b90b', size=5)
    ))
    
    # Ligne de référence (y=x)
    fig.add_trace(go.Scatter(
        x=theoretical_quantiles,
        y=theoretical_quantiles,
        mode='lines',
        name='Distribution Normale',
        line=dict(color='red', dash='dash')
    ))
    
    fig.update_layout(
        title='QQ-Plot (Test de Normalité)',
        xaxis_title='Quantiles Théoriques',
        yaxis_title='Quantiles Observés',
        template='plotly_dark',
        height=400
    )
    
    return fig

def plot_cumulative_returns(df):
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Cumulative_Returns'] * 100,
        mode='lines',
        name='Rendements Cumulés',
        line=dict(color='#00ff00', width=2),
        fill='tozeroy',
        fillcolor='rgba(0,255,0,0.1)'
    ))
    
    fig.update_layout(
        title='Évolution des Rendements Cumulés',
        xaxis_title='Date',
        yaxis_title='Rendement Cumulé (%)',
        template='plotly_dark',
        height=400,
        hovermode='x unified'
    )
    
    return fig

def plot_equity_curve_with_drawdown(df, initial_capital):
  
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.7, 0.3],
        subplot_titles=('Évolution du Capital', 'Drawdown')
    )
    
    # Courbe d'équité
    fig.add_trace(
        go.Scatter(x=df.index, y=df['Equity_Curve'], 
                   name='Capital', line=dict(color='#f0b90b', width=2)),
        row=1, col=1
    )
    
    # Ligne du capital initial
    fig.add_hline(y=initial_capital, line_dash="dash", 
                  line_color="gray", row=1, col=1,
                  annotation_text=f"Capital Initial: ${initial_capital:,.0f}")
    
    # Drawdown
    roll_max = df['Equity_Curve'].cummax()
    drawdown = ((df['Equity_Curve'] - roll_max) / roll_max) * 100
    
    fig.add_trace(
        go.Scatter(x=df.index, y=drawdown,
                   name='Drawdown', line=dict(color='#ff4b4b', width=1),
                   fill='tozeroy', fillcolor='rgba(255,75,75,0.3)'),
        row=2, col=1
    )
    
    fig.update_layout(
        height=600,
        template='plotly_dark',
        showlegend=True,
        hovermode='x unified'
    )
    
    fig.update_yaxes(title_text="Capital ($)", row=1, col=1)
    fig.update_yaxes(title_text="Drawdown (%)", row=2, col=1)
    
    return fig

def plot_correlation_heatmap(corr_matrix):
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale='RdYlGn',
        zmid=0,
        text=corr_matrix.values,
        texttemplate='%{text:.2f}',
        textfont={"size": 10},
        colorbar=dict(title="Corrélation")
    ))
    
    fig.update_layout(
        title='Matrice de Corrélation des Rendements',
        template='plotly_dark',
        height=500,
        width=500
    )
    
    return fig
