import streamlit as st
import yfinance as yf
from datetime import date

st.set_page_config(page_title="Portfolio Tracker", layout="wide", page_icon="📈")

theme_mode = st.sidebar.selectbox("Temă", ["Light", "Dark"], index=0)

if theme_mode == "Dark":
    bg_main = "#071226"
    bg_panel = "#121c34"
    bg_card = "#1a233b"
    bg_subtle = "#101a30"
    border = "rgba(255,255,255,0.08)"
    text_main = "#f8fafc"
    text_soft = "#94a3b8"
    green = "#4ade80"
    green_bg = "rgba(74,222,128,0.16)"
    blue = "#38bdf8"
    orange = "#f59e0b"
    red = "#f87171"
    donut_center = "#0d172d"
    shadow = "0 18px 40px rgba(0,0,0,0.18)"
else:
    bg_main = "#f4f7fb"
    bg_panel = "#ffffff"
    bg_card = "#ffffff"
    bg_subtle = "#eef3f9"
    border = "rgba(15,23,42,0.08)"
    text_main = "#0f172a"
    text_soft = "#64748b"
    green = "#16a34a"
    green_bg = "rgba(22,163,74,0.10)"
    blue = "#2563eb"
    orange = "#d97706"
    red = "#dc2626"
    donut_center = "#ffffff"
    shadow = "0 16px 34px rgba(15,23,42,0.08)"

st.markdown(
    f"""
    <style>
        .stApp {{
            background: {bg_main};
        }}

        .block-container {{
            max-width: 1450px;
            padding-top: 1rem;
            padding-bottom: 2rem;
        }}

        .hero {{
            background: linear-gradient(135deg, {bg_panel} 0%, {bg_subtle} 100%);
            border: 1px solid {border};
            border-radius: 26px;
            padding: 28px;
            margin-bottom: 18px;
            box-shadow: {shadow};
        }}

        .hero-kicker {{
            color: {blue};
            font-size: 0.82rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 8px;
            font-weight: 700;
        }}

        .hero-title {{
            color: {text_main};
            font-size: 2.4rem;
            font-weight: 800;
            line-height: 1.05;
            margin-bottom: 8px;
        }}

        .hero-subtitle {{
            color: {text_soft};
            font-size: 0.98rem;
            max-width: 780px;
        }}

        .summary-card {{
            background: {bg_card};
            border: 1px solid {border};
            border-radius: 22px;
            padding: 18px;
            min-height: 118px;
            box-shadow: {shadow};
        }}

        .summary-label {{
            color: {text_soft};
            font-size: 0.84rem;
            margin-bottom: 10px;
        }}

        .summary-value {{
            color: {text_main};
            font-size: 1.75rem;
            font-weight: 800;
            line-height: 1.05;
        }}

        .summary-positive {{
            color: {green};
            margin-top: 8px;
            font-size: 0.92rem;
            font-weight: 700;
        }}

        .summary-negative {{
            color: {red};
            margin-top: 8px;
            font-size: 0.92rem;
            font-weight: 700;
        }}

        .glass-card {{
            background: {bg_panel};
            border: 1px solid {border};
            border-radius: 22px;
            padding: 18px;
            box-shadow: {shadow};
        }}

        .section-title {{
            color: {text_main};
            font-size: 1.15rem;
            font-weight: 780;
            margin-bottom: 6px;
        }}

        .section-subtitle {{
            color: {text_soft};
            font-size: 0.9rem;
            margin-bottom: 14px;
        }}

        .asset-row {{
            background: {bg_card};
            border: 1px solid {border};
            border-radius: 18px;
            padding: 14px 16px;
            margin-bottom: 10px;
        }}

        .asset-name {{
            color: {text_main};
            font-size: 1rem;
            font-weight: 700;
        }}

        .asset-sub {{
            color: {text_soft};
            font-size: 0.82rem;
            margin-top: 2px;
        }}

        .pill-pos {{
            display: inline-block;
            background: {green_bg};
            color: {green};
            border: 1px solid rgba(34,197,94,0.22);
            border-radius: 999px;
            padding: 4px 10px;
            font-size: 0.78rem;
            font-weight: 700;
        }}

        .pill-neg {{
            display: inline-block;
            background: rgba(239,68,68,0.10);
            color: {red};
            border: 1px solid rgba(239,68,68,0.20);
            border-radius: 999px;
            padding: 4px 10px;
            font-size: 0.78rem;
            font-weight: 700;
        }}

        .sidebar-card {{
            background: {bg_panel};
            border: 1px solid {border};
            border-radius: 22px;
            padding: 16px;
            margin-bottom: 14px;
            box-shadow: {shadow};
        }}

        .sidebar-title {{
            color: {text_main};
            font-size: 1rem;
            font-weight: 760;
            margin-bottom: 10px;
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }}

        .legend-color {{
            width: 12px;
            height: 12px;
            border-radius: 4px;
            margin-right: 8px;
            flex-shrink: 0;
        }}

        .legend-text {{
            color: {text_main};
            font-size: 13px;
            line-height: 1.3;
        }}

        .legend-sub {{
            color: {text_soft};
            font-size: 12px;
        }}

        .notice-box {{
            background: {bg_subtle};
            border: 1px solid {border};
            border-radius: 18px;
            padding: 16px;
            color: {text_main};
            font-size: 0.94rem;
            line-height: 1.7;
        }}

        .ticker-chip {{
            background: {bg_subtle};
            border: 1px solid {border};
            border-radius: 12px;
            padding: 8px 10px;
            text-align: center;
            font-weight: 700;
            color: {text_main};
            margin-bottom: 8px;
        }}

        .crypto-card {{
            background: {bg_card};
            border: 1px solid {border};
            border-radius: 16px;
            padding: 14px;
            margin-bottom: 10px;
        }}

        .crypto-symbol {{
            color: {text_main};
            font-size: 1rem;
            font-weight: 800;
        }}

        .crypto-name {{
            color: {text_soft};
            font-size: 0.82rem;
            margin-top: 2px;
        }}

        .crypto-amount {{
            color: {text_main};
            font-size: 0.95rem;
            font-weight: 700;
            text-align: right;
        }}

        .crypto-value {{
            color: {text_soft};
            font-size: 0.85rem;
            text-align: right;
        }}

        .bvb-badge {{
            display: inline-block;
            border-radius: 999px;
            padding: 4px 10px;
            font-size: 0.76rem;
            font-weight: 700;
            margin-right: 6px;
        }}

        .bvb-ron {{
            background: rgba(37,99,235,0.10);
            color: {blue};
            border: 1px solid rgba(37,99,235,0.18);
        }}

        .bvb-usd {{
            background: {green_bg};
            color: {green};
            border: 1px solid rgba(34,197,94,0.20);
        }}

        .bucket-card {{
            background: {bg_card};
            border: 1px solid {border};
            border-radius: 18px;
            padding: 14px 16px;
            margin-bottom: 10px;
        }}

        .bucket-line {{
            display:flex;
            justify-content:space-between;
            align-items:flex-start;
            gap:12px;
        }}

        .bucket-kicker {{
            color:{text_soft};
            font-size:12px;
            margin-top:4px;
        }}

        .bucket-value {{
            color:{text_main};
            font-size:1.05rem;
            font-weight:800;
            text-align:right;
        }}

        .exchange-box {{
            background: linear-gradient(135deg, {bg_card} 0%, {bg_subtle} 100%);
            border: 1px solid {border};
            border-radius: 18px;
            padding: 18px;
            margin-bottom: 14px;
        }}

        .exchange-value {{
            color:{text_main};
            font-size:2rem;
            font-weight:800;
            line-height:1.05;
        }}

        div[data-testid="stMetric"] {{
            background: {bg_card};
            border: 1px solid {border};
            border-radius: 18px;
            padding: 14px;
            box-shadow: none;
        }}

        div[data-testid="stMetricLabel"] {{
            color: {text_soft};
        }}

        div[data-testid="stMetricValue"] {{
            color: {text_main};
            font-weight: 800;
        }}

        div[data-testid="stMetricDelta"] {{
            font-weight: 700;
        }}

        details {{
            background: {bg_panel};
            border: 1px solid {border};
            border-radius: 16px;
            margin-bottom: 12px;
            box-shadow: {shadow};
        }}

        details summary {{
            color: {text_main};
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

USD_RON_FALLBACK = 4.45

ASSETS = [
    {
        "name": "🪙 Crypto Spot",
        "mode": "crypto_manual",
        "total_now": 111.90,
        "today_pnl": -1.57,
        "today_pnl_pct": -1.38,
        "positions": [
            {"symbol": "BNB", "name": "Build and Build", "amount": "0.0767989", "value": 48.53},
            {"symbol": "BTC", "name": "Bitcoin", "amount": "0.00054", "value": 39.61},
            {"symbol": "XLM", "name": "Stellar Lumens", "amount": "134.00", "value": 23.65},
            {"symbol": "USD", "name": "USD", "amount": "0.085396", "value": 0.09},
            {"symbol": "USDC", "name": "USDC", "amount": "0.01422042", "value": 0.01},
            {"symbol": "EGLD", "name": "MultiversX", "amount": "0.0024066", "value": 0.01},
            {"symbol": "EDG", "name": "Edgeware", "amount": "218.69791733", "value": 0.00},
            {"symbol": "ETHW", "name": "Ethereum PoW", "amount": "0.00008495", "value": 0.00},
        ],
        "note": "Pentru crypto folosim valoarea curentă și Today's PnL din exchange. Cost basis complet nu este disponibil aici, deci totalul este tratat la valoarea actuală.",
    },
    {
        "name": "🇷🇴 BVB Principal",
        "mode": "bvb_manual",
        "cash_ron": 4.63,
        "positions": [
            {
                "ticker": "TLV",
                "name": "Banca Transilvania",
                "quantity": 11,
                "cost_avg_ron": 26.20,
                "market_price_ron": 38.30,
                "market_value_ron": 421.30,
                "return_pct": 46.13,
            },
            {
                "ticker": "TBK",
                "name": "Transilvania Broker",
                "quantity": 1,
                "cost_avg_ron": 18.03,
                "market_price_ron": 18.50,
                "market_value_ron": 18.50,
                "return_pct": 2.60,
            },
        ],
        "note": "BVB folosește valorile manuale din broker. Conversia în USD este estimată pe baza cursului USD/RON.",
    },
    {
        "name": "💰 PIE OT Investimental",
        "mode": "manual_with_positions",
        "tickers": ["LIN", "XOM", "PLD", "NEE", "MSFT", "AMZN", "WMT", "META", "JPM", "LLY"],
        "buy_date": date(2024, 7, 22),
        "amount_per_stock": 37.33,
        "invested_cost_basis": 373.30,
        "invested_now": 480.84,
        "cash_now": 141.98,
        "total_now": 622.82,
        "note": "PIE OT folosește valori manuale reale pentru totaluri. Randamentul pe tickere este calculat pe partea investită inițial, iar cash-ul rămâne separat.",
    },
    {
        "name": "📈 Alex PIE 20",
        "mode": "calculated",
        "tickers": ["COST", "V", "ORCL", "JNJ", "HD", "XOM", "CAT", "MSFT", "WMT", "MA", "AMZN", "GOOG", "BRK-B", "NVDA", "TSLA", "JPM", "LLY", "META", "AVGO", "AAPL"],
        "buy_date": date(2026, 5, 19),
        "amount_per_stock": 54.91,
        "cash_additions": [],
    },
    {
        "name": "🤖 AI TECH",
        "mode": "calculated",
        "tickers": ["AMAT", "MU", "MSTR", "AMD", "MRVL", "ASML", "TSM", "SNPS", "SNDK", "NTNX", "INTC", "AVGO", "CDNS", "ON"],
        "buy_date": date(2026, 5, 26),
        "amount_per_stock": 78.44,
        "cash_additions": [],
    },
]

st.sidebar.markdown('<div class="sidebar-title">Control Panel</div>', unsafe_allow_html=True)
if st.sidebar.button("Refresh Manual", use_container_width=True):
    st.rerun()


def load_history(ticker: str):
    history = yf.Ticker(ticker).history(period="5y", auto_adjust=False)
    if history.empty:
        return history
    return history[["Close"]].dropna()


def get_price_on_or_before(history, target_date: date):
    rows = history[history.index.date <= target_date]
    if rows.empty:
        return None
    return float(rows["Close"].iloc[-1])


def get_ticker_data(ticker: str, buy_date: date):
    try:
        history = load_history(ticker)
        if history.empty:
            return None, "Fără istoric"
        current_price = float(history["Close"].iloc[-1])
        buy_price = get_price_on_or_before(history, buy_date)
        if buy_price is None:
            return None, f"Fără preț la data {buy_date:%d.%m.%Y}"
        return {"price": current_price, "buy_price": buy_price}, None
    except Exception as e:
        return None, str(e)


def get_usdron_rate():
    try:
        direct = yf.Ticker("USDRON=X").history(period="10d", auto_adjust=False)
        if not direct.empty:
            price = float(direct["Close"].dropna().iloc[-1])
            if price > 0:
                return price
    except Exception:
        pass

    try:
        inverse = yf.Ticker("RON=X").history(period="10d", auto_adjust=False)
        if not inverse.empty:
            price = float(inverse["Close"].dropna().iloc[-1])
            if price > 0:
                return 1 / price
    except Exception:
        pass

    return USD_RON_FALLBACK


def update_best_worst(position, best_position, worst_position):
    if best_position is None or position["return_pct"] > best_position["return_pct"]:
        best_position = position
    if worst_position is None or position["return_pct"] < worst_position["return_pct"]:
        worst_position = position
    return best_position, worst_position


usdron_rate = get_usdron_rate()

portfolio_totals = []
portfolio_results = []
global_total_now_usd = 0.0
global_total_in_usd = 0.0
total_cash_usd = 0.0
best_position = None
worst_position = None

for asset in ASSETS:
    if asset["mode"] == "crypto_manual":
        current_usd = asset["total_now"]
        basis_usd = asset["total_now"]

        portfolio_results.append({
            "name": asset["name"],
            "mode": "crypto_manual",
            "current_usd": current_usd,
            "basis_usd": basis_usd,
            "today_pnl": asset["today_pnl"],
            "today_pnl_pct": asset["today_pnl_pct"],
            "positions": asset["positions"],
            "note": asset["note"],
        })

        portfolio_totals.append({"Categorie": asset["name"], "Valoare": current_usd})
        global_total_now_usd += current_usd
        global_total_in_usd += basis_usd
        continue

    if asset["mode"] == "bvb_manual":
        positions = []
        invested_cost_basis_ron = 0.0
        invested_now_ron = 0.0

        for raw in asset["positions"]:
            position_cost_ron = raw["quantity"] * raw["cost_avg_ron"]
            profit_loss_ron = raw["market_value_ron"] - position_cost_ron

            position = {
                "ticker": raw["ticker"],
                "name": raw["name"],
                "quantity": raw["quantity"],
                "cost_avg_ron": raw["cost_avg_ron"],
                "market_price_ron": raw["market_price_ron"],
                "market_value_ron": raw["market_value_ron"],
                "profit_loss_ron": profit_loss_ron,
                "return_pct": raw["return_pct"],
                "portfolio": asset["name"],
            }
            positions.append(position)
            invested_cost_basis_ron += position_cost_ron
            invested_now_ron += raw["market_value_ron"]

            best_position, worst_position = update_best_worst(position, best_position, worst_position)

        cash_ron = asset["cash_ron"]
        total_ron = invested_now_ron + cash_ron
        basis_ron = invested_cost_basis_ron + cash_ron

        invested_change_pct = ((invested_now_ron - invested_cost_basis_ron) / invested_cost_basis_ron * 100) if invested_cost_basis_ron else 0
        total_change_pct = ((total_ron - basis_ron) / basis_ron * 100) if basis_ron else 0

        current_usd = total_ron / usdron_rate
        basis_usd = basis_ron / usdron_rate
        cash_usd = cash_ron / usdron_rate

        portfolio_results.append({
            "name": asset["name"],
            "mode": "bvb_manual",
            "positions": positions,
            "invested_cost_basis_ron": invested_cost_basis_ron,
            "invested_now_ron": invested_now_ron,
            "cash_ron": cash_ron,
            "total_ron": total_ron,
            "invested_change_pct": invested_change_pct,
            "total_change_pct": total_change_pct,
            "usdron_rate": usdron_rate,
            "current_usd": current_usd,
            "basis_usd": basis_usd,
            "cash_usd": cash_usd,
            "note": asset["note"],
        })

        portfolio_totals.append({"Categorie": asset["name"], "Valoare": current_usd})
        global_total_now_usd += current_usd
        global_total_in_usd += basis_usd
        total_cash_usd += cash_usd
        continue

    if asset["mode"] == "manual_with_positions":
        invested_cost_basis = asset["invested_cost_basis"]
        invested_now = asset["invested_now"]
        cash_total = asset["cash_now"]
        total_now = asset["total_now"]
        basis_usd = invested_cost_basis + cash_total

        invested_change_pct = ((invested_now - invested_cost_basis) / invested_cost_basis * 100) if invested_cost_basis else 0
        total_change_pct = ((total_now - basis_usd) / basis_usd * 100) if basis_usd else 0

        positions = []
        failed = []
        total_positions_value = 0.0

        for ticker in asset["tickers"]:
            data, error = get_ticker_data(ticker, asset["buy_date"])
            if error:
                failed.append(f"{ticker}: {error}")
                continue

            current_value = asset["amount_per_stock"] * (data["price"] / data["buy_price"])
            profit_loss = current_value - asset["amount_per_stock"]
            return_pct = (profit_loss / asset["amount_per_stock"] * 100) if asset["amount_per_stock"] else 0

            position = {
                "ticker": ticker,
                "price": data["price"],
                "invested": asset["amount_per_stock"],
                "current_value": current_value,
                "profit_loss": profit_loss,
                "return_pct": return_pct,
                "portfolio": asset["name"],
            }
            positions.append(position)
            total_positions_value += current_value

            best_position, worst_position = update_best_worst(position, best_position, worst_position)

        portfolio_results.append({
            "name": asset["name"],
            "mode": "manual_with_positions",
            "tickers": asset["tickers"],
            "buy_date": asset["buy_date"],
            "amount_per_stock": asset["amount_per_stock"],
            "invested_cost_basis": invested_cost_basis,
            "invested_now": invested_now,
            "cash_total": cash_total,
            "total_now": total_now,
            "invested_change_pct": invested_change_pct,
            "total_change_pct": total_change_pct,
            "note": asset["note"],
            "positions": positions,
            "failed": failed,
            "total_positions_value": total_positions_value,
            "ticker_count": len(asset["tickers"]),
            "current_usd": total_now,
            "basis_usd": basis_usd,
        })

        portfolio_totals.append({"Categorie": asset["name"], "Valoare": total_now})
        global_total_now_usd += total_now
        global_total_in_usd += basis_usd
        total_cash_usd += cash_total
        continue

    positions = []
    failed = []
    total_positions_value = 0.0
    invested_total = asset["amount_per_stock"] * len(asset["tickers"])
    cash_total = sum(x["amount"] for x in asset["cash_additions"])

    for ticker in asset["tickers"]:
        data, error = get_ticker_data(ticker, asset["buy_date"])
        if error:
            failed.append(f"{ticker}: {error}")
            continue

        current_value = asset["amount_per_stock"] * (data["price"] / data["buy_price"])
        profit_loss = current_value - asset["amount_per_stock"]
        return_pct = (profit_loss / asset["amount_per_stock"] * 100) if asset["amount_per_stock"] else 0

        position = {
            "ticker": ticker,
            "price": data["price"],
            "invested": asset["amount_per_stock"],
            "current_value": current_value,
            "profit_loss": profit_loss,
            "return_pct": return_pct,
            "portfolio": asset["name"],
        }
        positions.append(position)
        total_positions_value += current_value

        best_position, worst_position = update_best_worst(position, best_position, worst_position)

    current_usd = total_positions_value + cash_total
    basis_usd = invested_total + cash_total
    change_pct = ((current_usd - basis_usd) / basis_usd * 100) if basis_usd else 0

    portfolio_results.append({
        "name": asset["name"],
        "mode": "calculated",
        "tickers": asset["tickers"],
        "buy_date": asset["buy_date"],
        "positions": positions,
        "failed": failed,
        "cash_total": cash_total,
        "invested_total": invested_total,
        "total_positions_value": total_positions_value,
        "current_usd": current_usd,
        "basis_usd": basis_usd,
        "change_pct": change_pct,
        "ticker_count": len(asset["tickers"]),
    })

    portfolio_totals.append({"Categorie": asset["name"], "Valoare": current_usd})
    global_total_now_usd += current_usd
    global_total_in_usd += basis_usd
    total_cash_usd += cash_total

global_profit_usd = global_total_now_usd - global_total_in_usd
global_profit_pct = (global_profit_usd / global_total_in_usd * 100) if global_total_in_usd else 0

st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">Dashboard</div>
        <div class="hero-title">My Assets</div>
        <div class="hero-subtitle">
            O vedere mai curată asupra portofoliului tău: valoare totală în USD, cash, alocare pe crypto, BVB și PIE-uri, plus performanță pe fiecare poziție.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([3.4, 1.3])

with left:
    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.markdown(
            f"""
            <div class="summary-card">
                <div class="summary-label">Total Assets (USD)</div>
                <div class="summary-value">${global_total_now_usd:,.2f}</div>
                <div class="{'summary-positive' if global_profit_usd >= 0 else 'summary-negative'}">
                    {'+' if global_profit_usd >= 0 else ''}${global_profit_usd:,.2f} ({global_profit_pct:.2f}%)
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with s2:
        st.markdown(
            f"""
            <div class="summary-card">
                <div class="summary-label">Capital introdus (USD)</div>
                <div class="summary-value">${global_total_in_usd:,.2f}</div>
                <div class="summary-label">BVB convertit estimativ • Crypto la valoarea actuală</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with s3:
        st.markdown(
            f"""
            <div class="summary-card">
                <div class="summary-label">Cash total (USD est.)</div>
                <div class="summary-value">${total_cash_usd:,.2f}</div>
                <div class="summary-label">PIE OT cash + BVB cash convertit</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with s4:
        best_text = "N/A" if best_position is None else f"{best_position['ticker']} {best_position['return_pct']:.2f}%"
        st.markdown(
            f"""
            <div class="summary-card">
                <div class="summary-label">Best Performer</div>
                <div class="summary-value" style="font-size:1.16rem;">{best_text}</div>
                <div class="summary-label">Top poziție dintre assets trackable</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Portfolio Buckets</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Ordine: Crypto, BVB, PIE OT, PIE 20, AI TECH</div>', unsafe_allow_html=True)

    for result in portfolio_results:
        if result["mode"] == "crypto_manual":
            row_pct = result["today_pnl_pct"]
            row_label = f"Today {row_pct:+.2f}%"
            sub_line = f"Spot value: ${result['current_usd']:,.2f}"
        elif result["mode"] == "bvb_manual":
            row_pct = result["invested_change_pct"]
            row_label = f"Invested {row_pct:+.2f}%"
            sub_line = f"RON total: {result['total_ron']:,.2f} | Est. USD: ${result['current_usd']:,.2f}"
        elif result["mode"] == "manual_with_positions":
            row_pct = result["invested_change_pct"]
            row_label = f"Invested {row_pct:+.2f}%"
            sub_line = f"Invested now: ${result['invested_now']:,.2f} | Cash: ${result['cash_total']:,.2f}"
        else:
            row_pct = result["change_pct"]
            row_label = f"{row_pct:+.2f}%"
            cash_line = f" | Cash: ${result['cash_total']:,.2f}" if result["cash_total"] else ""
            sub_line = f"Investit: ${result['invested_total']:,.2f}{cash_line}"

        pill_class = "pill-pos" if row_pct >= 0 else "pill-neg"

        st.markdown(
            f"""
            <div class="bucket-card">
                <div class="bucket-line">
                    <div>
                        <div class="asset-name">{result['name']}</div>
                        <div class="bucket-kicker">{sub_line}</div>
                    </div>
                    <div>
                        <div class="bucket-value">${result['current_usd']:,.2f}</div>
                        <div class="{pill_class}" style="margin-top:6px;">{row_label}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    for result in portfolio_results:
        if result["mode"] == "crypto_manual":
            expander_suffix = f"Today {result['today_pnl_pct']:+.2f}%"
        elif result["mode"] == "bvb_manual":
            expander_suffix = f"Invested {result['invested_change_pct']:+.2f}%"
        elif result["mode"] == "manual_with_positions":
            expander_suffix = f"Invested {result['invested_change_pct']:+.2f}%"
        else:
            expander_suffix = f"{result['change_pct']:+.2f}%"

        with st.expander(
            f"{result['name']} • ${result['current_usd']:,.2f} • {expander_suffix}",
            expanded=False
        ):
            if result["mode"] == "crypto_manual":
                st.markdown(
                    f"""
                    <div class="exchange-box">
                        <div class="summary-label">Est. Total Value</div>
                        <div class="exchange-value">${result['current_usd']:.2f}</div>
                        <div class="{'summary-positive' if result['today_pnl'] >= 0 else 'summary-negative'}">
                            Today's PnL: ${result['today_pnl']:+.2f} ({result['today_pnl_pct']:+.2f}%)
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"""
                    <div class="notice-box" style="margin-bottom:12px;">
                        {result['note']}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                for i in range(0, len(result["positions"]), 2):
                    cols = st.columns(2)
                    for j, coin in enumerate(result["positions"][i:i + 2]):
                        with cols[j]:
                            st.markdown(
                                f"""
                                <div class="crypto-card">
                                    <div style="display:flex; justify-content:space-between; gap:12px;">
                                        <div>
                                            <div class="crypto-symbol">{coin['symbol']}</div>
                                            <div class="crypto-name">{coin['name']}</div>
                                        </div>
                                        <div>
                                            <div class="crypto-amount">{coin['amount']}</div>
                                            <div class="crypto-value">${coin['value']:.2f}</div>
                                        </div>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                continue

            if result["mode"] == "bvb_manual":
                st.markdown(
                    f"""
                    <div class="notice-box">
                        <b>Capital investit inițial:</b> {result['invested_cost_basis_ron']:.2f} RON<br>
                        <b>Valoare investită acum:</b> {result['invested_now_ron']:.2f} RON<br>
                        <b>Randament pe investiție:</b> {result['invested_change_pct']:+.2f}%<br>
                        <b>Cash:</b> {result['cash_ron']:.2f} RON<br>
                        <b>Valoare totală:</b> {result['total_ron']:.2f} RON<br>
                        <b>Estimare USD:</b> ${result['current_usd']:.2f}<br>
                        <b>Curs estimat USD/RON:</b> {result['usdron_rate']:.4f}<br><br>
                        {result['note']}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                for i, pos in enumerate(result["positions"]):
                    badge_row = (
                        f'<span class="bvb-badge bvb-ron">{pos["market_value_ron"]:.2f} RON</span>'
                        f'<span class="bvb-badge bvb-usd">${pos["market_value_ron"] / result["usdron_rate"]:.2f}</span>'
                    )
                    st.markdown(
                        f"""
                        <div class="crypto-card">
                            <div style="display:flex; justify-content:space-between; gap:16px; align-items:flex-start;">
                                <div>
                                    <div class="crypto-symbol">{pos['ticker']}</div>
                                    <div class="crypto-name">{pos['name']}</div>
                                    <div style="margin-top:10px;">{badge_row}</div>
                                </div>
                                <div style="text-align:right;">
                                    <div class="crypto-amount">{pos['market_price_ron']:.2f} RON</div>
                                    <div class="crypto-value">Cantitate: {pos['quantity']} | Cost mediu: {pos['cost_avg_ron']:.2f} RON</div>
                                    <div class="crypto-value">P/L: {pos['profit_loss_ron']:+.2f} RON | {pos['return_pct']:+.2f}%</div>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                continue

            if result["mode"] == "manual_with_positions":
                st.markdown(
                    f"""
                    <div class="notice-box">
                        <b>Capital investit inițial:</b> ${result['invested_cost_basis']:.2f}<br>
                        <b>Valoare investită acum:</b> ${result['invested_now']:.2f}<br>
                        <b>Randament pe investiție:</b> {result['invested_change_pct']:+.2f}%<br>
                        <b>Cash:</b> ${result['cash_total']:.2f}<br>
                        <b>Valoare totală:</b> ${result['total_now']:.2f}<br><br>
                        {result['note']}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.caption(f"Data intrării: {result['buy_date']:%d.%m.%Y}")

                cols = st.columns(4)
                target_weight = 100 / result["ticker_count"] if result["ticker_count"] else 0

                for i, pos in enumerate(result["positions"]):
                    current_weight = (
                        pos["current_value"] / result["total_positions_value"] * 100
                        if result["total_positions_value"] else 0
                    )
                    with cols[i % 4]:
                        st.metric(
                            label=pos["ticker"],
                            value=f"${pos['price']:.2f}",
                            delta=f"{pos['return_pct']:.2f}%"
                        )
                        st.caption(f"Țintă: {target_weight:.2f}% | Acum: {current_weight:.2f}%")
                        st.caption(f"Valoare poziție: ${pos['current_value']:.2f}")
                        st.caption(f"P/L: ${pos['profit_loss']:+.2f}")

                if result["failed"]:
                    st.warning("Simboluri neîncărcate:")
                    for item in result["failed"]:
                        st.write(f"- {item}")
                continue

            st.caption(f"Data intrării: {result['buy_date']:%d.%m.%Y}")

            cols = st.columns(4)
            target_weight = 100 / result["ticker_count"] if result["ticker_count"] else 0

            for i, pos in enumerate(result["positions"]):
                current_weight = (
                    pos["current_value"] / result["total_positions_value"] * 100
                    if result["total_positions_value"] else 0
                )
                with cols[i % 4]:
                    st.metric(
                        label=pos["ticker"],
                        value=f"${pos['price']:.2f}",
                        delta=f"{pos['return_pct']:.2f}%"
                    )
                    st.caption(f"Țintă: {target_weight:.2f}% | Acum: {current_weight:.2f}%")
                    st.caption(f"Valoare poziție: ${pos['current_value']:.2f}")
                    st.caption(f"P/L: ${pos['profit_loss']:+.2f}")

            if result["failed"]:
                st.warning("Simboluri neîncărcate:")
                for item in result["failed"]:
                    st.write(f"- {item}")

with right:
    st.markdown('<div class="sidebar-card"><div class="sidebar-title">Allocation (USD)</div>', unsafe_allow_html=True)

    total_value = sum(x["Valoare"] for x in portfolio_totals)
    colors = [green, blue, orange, "#94a3b8", red, "#8b5cf6", "#06b6d4"]

    current_angle = 0
    segments = []
    legend_html = ""

    for i, item in enumerate(portfolio_totals):
        color = colors[i % len(colors)]
        pct = (item["Valoare"] / total_value * 100) if total_value else 0
        angle = pct * 3.6
        segments.append(f"{color} {current_angle:.2f}deg {current_angle + angle:.2f}deg")
        legend_html += f"""
        <div class="legend-item">
            <div class="legend-color" style="background:{color};"></div>
            <div class="legend-text">
                {item['Categorie']}<br>
                <span class="legend-sub">${item['Valoare']:,.2f} ({pct:.1f}%)</span>
            </div>
        </div>
        """
        current_angle += angle

    donut_style = ", ".join(segments)

    st.markdown(
        f"""
        <div style="display:flex; justify-content:center; margin:8px 0 16px 0;">
            <div style="
                width:220px;
                height:220px;
                border-radius:50%;
                background: conic-gradient({donut_style});
                position:relative;
                box-shadow:{shadow};
            ">
                <div style="
                    position:absolute;
                    top:50%;
                    left:50%;
                    transform:translate(-50%, -50%);
                    width:112px;
                    height:112px;
                    border-radius:50%;
                    background:{donut_center};
                    border:1px solid {border};
                    display:flex;
                    flex-direction:column;
                    align-items:center;
                    justify-content:center;
                    color:{text_main};
                    text-align:center;
                ">
                    <div style="color:{text_soft}; font-size:12px;">Total</div>
                    <div style="font-size:17px; font-weight:800;">${total_value:,.0f}</div>
                </div>
            </div>
        </div>
        {legend_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="sidebar-card">
            <div class="sidebar-title">FX Estimate</div>
            <div style="color:{text_main}; font-size:1.1rem; font-weight:800;">1 USD = {usdron_rate:.4f} RON</div>
            <div style="color:{text_soft}; font-size:0.84rem; margin-top:4px;">Folosit pentru conversia BVB în USD</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if best_position:
        st.markdown(
            f"""
            <div class="sidebar-card">
                <div class="sidebar-title">Top Performer</div>
                <div style="color:{text_main}; font-size:1.1rem; font-weight:800;">{best_position['ticker']}</div>
                <div style="color:{green}; font-weight:700; margin-top:4px;">{best_position['return_pct']:+.2f}%</div>
                <div style="color:{text_soft}; font-size:0.84rem; margin-top:4px;">{best_position['portfolio']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if worst_position:
        st.markdown(
            f"""
            <div class="sidebar-card">
                <div class="sidebar-title">Weakest Performer</div>
                <div style="color:{text_main}; font-size:1.1rem; font-weight:800;">{worst_position['ticker']}</div>
                <div style="color:{red}; font-weight:700; margin-top:4px;">{worst_position['return_pct']:.2f}%</div>
                <div style="color:{text_soft}; font-size:0.84rem; margin-top:4px;">{worst_position['portfolio']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.caption("Date de la Yahoo Finance • Tema implicită este Light • Total Assets este în USD • BVB este convertit estimativ din RON • Crypto folosește valorile manuale din exchange • PIE OT separă investiția de cash")
