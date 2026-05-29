import streamlit as st
import yfinance as yf
from datetime import date
import xml.etree.ElementTree as ET
import json
import time
import hmac
import hashlib
from urllib.parse import urlencode
from urllib.request import Request, urlopen

st.set_page_config(page_title="Family Assets Dashboard", layout="wide", page_icon="📈")

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
            max-width: 900px;
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

        .asset-name {{
            color: {text_main};
            font-size: 1rem;
            font-weight: 700;
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

        .bank-logo {{
            display:inline-flex;
            align-items:center;
            justify-content:center;
            width:26px;
            height:26px;
            border-radius:8px;
            margin-right:8px;
            font-size:14px;
            font-weight:800;
            vertical-align:middle;
        }}

        .logo-ing {{
            background:#ff6200;
            color:white;
        }}

        .logo-revolut {{
            background:#111827;
            color:white;
        }}

        .subasset-title {{
            color:{text_main};
            font-size:1rem;
            font-weight:800;
            margin:14px 0 8px 0;
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

ECB_XML_URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
USD_RON_FALLBACK = 4.45
EUR_USD_FALLBACK = 1.08
BINANCE_BASE_URL = "https://api.binance.com"
BINANCE_STABLE_ASSETS = {"USDT", "USDC", "FDUSD", "BUSD", "TUSD", "USDP", "USDS", "DAI", "USD"}

REVOLUT_REFERENCE_DATE = date(2026, 5, 29)
REVOLUT_START_BALANCE_RON = 22536.00
REVOLUT_ANNUAL_RATE = 0.025
REVOLUT_WITHHOLDING_TAX = 0.10
ING_NL_ALEX_EUR = 3000.00


def http_get_json(url: str, headers=None):
    request = Request(url, headers=headers or {"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def has_binance_secrets():
    return "BINANCE_API_KEY" in st.secrets and "BINANCE_API_SECRET" in st.secrets


def binance_public_get(path: str, params=None):
    query = f"?{urlencode(params)}" if params else ""
    return http_get_json(f"{BINANCE_BASE_URL}{path}{query}")


def binance_signed_get(path: str, params=None):
    api_key = st.secrets["BINANCE_API_KEY"]
    api_secret = st.secrets["BINANCE_API_SECRET"]

    request_params = dict(params or {})
    request_params["timestamp"] = int(time.time() * 1000)
    request_params["recvWindow"] = 5000

    query = urlencode(request_params)
    signature = hmac.new(
        api_secret.encode("utf-8"),
        query.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    return http_get_json(
        f"{BINANCE_BASE_URL}{path}?{query}&signature={signature}",
        headers={"X-MBX-APIKEY": api_key, "User-Agent": "Mozilla/5.0"},
    )


def safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def build_binance_symbol_candidates(asset_code: str):
    candidates = []

    if asset_code not in BINANCE_STABLE_ASSETS:
        candidates.append((f"{asset_code}USDT", 1.0))
        candidates.append((f"{asset_code}BTC", "BTCUSDT"))
        candidates.append((f"{asset_code}ETH", "ETHUSDT"))
        candidates.append((f"{asset_code}BNB", "BNBUSDT"))

    return candidates


def resolve_binance_asset_prices(asset_code: str, last_prices, open_prices):
    if asset_code in BINANCE_STABLE_ASSETS:
        return 1.0, 1.0

    for base_symbol, quote_symbol in build_binance_symbol_candidates(asset_code):
        if isinstance(quote_symbol, float):
            if base_symbol in last_prices and base_symbol in open_prices:
                return last_prices[base_symbol], open_prices[base_symbol]
            continue

        if (
            base_symbol in last_prices and base_symbol in open_prices
            and quote_symbol in last_prices and quote_symbol in open_prices
        ):
            return (
                last_prices[base_symbol] * last_prices[quote_symbol],
                open_prices[base_symbol] * open_prices[quote_symbol],
            )

    return None, None


def get_binance_crypto_snapshot():
    if not has_binance_secrets():
        return None, "fallback"

    try:
        account = binance_signed_get("/api/v3/account", {"omitZeroBalances": "true"})

        assets = []
        symbols_needed = set()

        for balance in account.get("balances", []):
            asset_code = balance.get("asset", "")
            free_qty = safe_float(balance.get("free"))
            locked_qty = safe_float(balance.get("locked"))
            quantity = free_qty + locked_qty

            if quantity <= 0:
                continue

            assets.append({
                "asset": asset_code,
                "quantity": quantity,
            })

            for base_symbol, quote_symbol in build_binance_symbol_candidates(asset_code):
                symbols_needed.add(base_symbol)
                if isinstance(quote_symbol, str):
                    symbols_needed.add(quote_symbol)

        if not assets:
            return {
                "positions": [],
                "total_now": 0.0,
                "today_pnl": 0.0,
                "today_pnl_pct": 0.0,
                "source": "Binance API",
            }, None

        market_params = {"symbols": json.dumps(sorted(symbols_needed))}
        prices = binance_public_get("/api/v3/ticker/price", market_params)
        ticker_24h = binance_public_get("/api/v3/ticker/24hr", market_params)

        last_prices = {
            item["symbol"]: safe_float(item["price"])
            for item in prices
            if "symbol" in item and "price" in item
        }
        open_prices = {
            item["symbol"]: safe_float(item["openPrice"])
            for item in ticker_24h
            if "symbol" in item and "openPrice" in item
        }

        positions = []
        total_value = 0.0
        total_open_value = 0.0

        for asset_item in assets:
            asset_code = asset_item["asset"]
            quantity = asset_item["quantity"]
            last_usdt, open_usdt = resolve_binance_asset_prices(asset_code, last_prices, open_prices)

            if last_usdt is None:
                positions.append({
                    "symbol": asset_code,
                    "name": asset_code,
                    "amount": f"{quantity:.8f}".rstrip("0").rstrip("."),
                    "value": 0.0,
                    "today_pnl": 0.0,
                    "today_pnl_pct": 0.0,
                    "pricing_status": "unpriced",
                })
                continue

            current_value = quantity * last_usdt
            open_value = quantity * open_usdt
            pnl_value = current_value - open_value
            pnl_pct = (pnl_value / open_value * 100) if open_value else 0.0

            positions.append({
                "symbol": asset_code,
                "name": asset_code,
                "amount": f"{quantity:.8f}".rstrip("0").rstrip("."),
                "value": current_value,
                "today_pnl": pnl_value,
                "today_pnl_pct": pnl_pct,
                "pricing_status": "ok",
            })

            total_value += current_value
            total_open_value += open_value

        positions.sort(key=lambda item: item["value"], reverse=True)

        total_pnl = total_value - total_open_value
        total_pnl_pct = (total_pnl / total_open_value * 100) if total_open_value else 0.0

        return {
            "positions": positions,
            "total_now": total_value,
            "today_pnl": total_pnl,
            "today_pnl_pct": total_pnl_pct,
            "source": "Binance API",
        }, None
    except Exception as exc:
        return None, str(exc)


def get_live_ecb_fx():
    try:
        with urlopen(ECB_XML_URL, timeout=15) as response:
            xml_bytes = response.read()

        root = ET.fromstring(xml_bytes)
        rates = {}
        fx_date = None

        for elem in root.iter():
            if "time" in elem.attrib:
                fx_date = elem.attrib["time"]
            if "currency" in elem.attrib and "rate" in elem.attrib:
                rates[elem.attrib["currency"]] = float(elem.attrib["rate"])

        eurusd = rates["USD"]
        eurron = rates["RON"]
        usdron = eurron / eurusd

        return {
            "eurusd": eurusd,
            "eurron": eurron,
            "usdron": usdron,
            "source": "ECB live",
            "date": fx_date,
        }
    except Exception:
        eurusd = EUR_USD_FALLBACK
        usdron = USD_RON_FALLBACK
        eurron = eurusd * usdron
        return {
            "eurusd": eurusd,
            "eurron": eurron,
            "usdron": usdron,
            "source": "fallback",
            "date": None,
        }


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


def update_best_worst(position, best_position, worst_position):
    if best_position is None or position["return_pct"] > best_position["return_pct"]:
        best_position = position
    if worst_position is None or position["return_pct"] < worst_position["return_pct"]:
        worst_position = position
    return best_position, worst_position


def compound_daily_balance_with_tax(start_balance: float, annual_rate: float, tax_rate: float, reference_date: date):
    today = date.today()
    days_elapsed = max((today - reference_date).days + 1, 0)

    gross_daily_rate = annual_rate / 365
    net_daily_rate = gross_daily_rate * (1 - tax_rate)

    current_balance = start_balance * ((1 + net_daily_rate) ** days_elapsed)
    net_interest_earned = current_balance - start_balance
    net_yield_pct = (net_interest_earned / start_balance * 100) if start_balance else 0

    gross_interest_today = current_balance * gross_daily_rate
    tax_today = gross_interest_today * tax_rate
    net_interest_today = gross_interest_today - tax_today

    return {
        "days_elapsed": days_elapsed,
        "gross_daily_rate": gross_daily_rate,
        "net_daily_rate": net_daily_rate,
        "current_balance": current_balance,
        "net_interest_earned": net_interest_earned,
        "net_yield_pct": net_yield_pct,
        "gross_interest_today": gross_interest_today,
        "tax_today": tax_today,
        "net_interest_today": net_interest_today,
    }


fx = get_live_ecb_fx()
eurusd_rate = fx["eurusd"]
usdron_rate = fx["usdron"]
eurron_rate = fx["eurron"]

ALEX_ASSETS = [
    {
        "name": "🪙 Crypto Spot",
        "display_html": "🪙 Crypto Spot",
        "mode": "crypto_binance_fallback",
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
        "note": "Dacă există cheile Binance în Streamlit secrets, crypto devine live din cont. Altfel rămâne fallback pe valorile manuale de mai jos.",
    },
    {
        "name": "RO BVB Principal",
        "display_html": "🇷🇴 RO BVB Principal",
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
        "note": "BVB folosește valorile manuale din broker. Conversia în USD și EUR este estimată prin cursurile live ECB.",
    },
    {
        "name": "💰 PIE OT Investimental",
        "display_html": "💰 PIE OT Investimental",
        "mode": "manual_with_positions",
        "tickers": ["LIN", "XOM", "PLD", "NEE", "MSFT", "AMZN", "WMT", "META", "JPM", "LLY"],
        "buy_date": date(2024, 7, 22),
        "amount_per_stock": 37.33,
        "cash_now": 0.0,
        "extra_buys": [
            {"ticker": "WMT", "buy_date": date(2026, 5, 29), "amount": 23.79, "quantity": 0.20521216},
            {"ticker": "AMZN", "buy_date": date(2026, 5, 29), "amount": 30.17, "quantity": 0.11124680},
            {"ticker": "JPM", "buy_date": date(2026, 5, 29), "amount": 32.41, "quantity": 0.10953809},
            {"ticker": "META", "buy_date": date(2026, 5, 29), "amount": 36.97, "quantity": 0.05924594},
            {"ticker": "LLY", "buy_date": date(2026, 5, 29), "amount": 36.98, "quantity": 0.03339839},
            {"ticker": "NEE", "buy_date": date(2026, 5, 29), "amount": 40.71, "quantity": 0.47184244},
            {"ticker": "XOM", "buy_date": date(2026, 5, 29), "amount": 37.34, "quantity": 0.25473274},
            {"ticker": "PLD", "buy_date": date(2026, 5, 29), "amount": 41.72, "quantity": 0.28962407},
            {"ticker": "LIN", "buy_date": date(2026, 5, 29), "amount": 43.11, "quantity": 0.08610826},
            {"ticker": "MSFT", "buy_date": date(2026, 5, 29), "amount": 47.51, "quantity": 0.10747925},
        ],
        "note": "PIE OT include cumpărările suplimentare din 29.05.2026. Cash-ul a fost investit complet, deci valoarea este urmărită integral prin poziții.",
    },
    {
        "name": "📈 Alex PIE 20",
        "display_html": "📈 Alex PIE 20",
        "mode": "calculated",
        "tickers": ["COST", "V", "ORCL", "JNJ", "HD", "XOM", "CAT", "MSFT", "WMT", "MA", "AMZN", "GOOG", "BRK-B", "NVDA", "TSLA", "JPM", "LLY", "META", "AVGO", "AAPL"],
        "buy_date": date(2026, 5, 19),
        "amount_per_stock": 54.91,
        "cash_additions": [],
    },
    {
        "name": "🤖 AI TECH",
        "display_html": "🤖 AI TECH",
        "mode": "calculated",
        "tickers": ["AMAT", "MU", "MSTR", "AMD", "MRVL", "ASML", "TSM", "SNPS", "SNDK", "NTNX", "INTC", "AVGO", "CDNS", "ON"],
        "buy_date": date(2026, 5, 26),
        "amount_per_stock": 78.44,
        "cash_additions": [],
    },
    {
        "name": "ING NL Alex",
        "display_html": '<span class="bank-logo logo-ing">I</span>ING NL Alex',
        "mode": "savings_eur_fixed",
        "balance_eur": ING_NL_ALEX_EUR,
        "note": "Cont de economii simplu în EUR. Pentru moment este tratat ca sold fix, fără dobândă automată.",
    },
]

ANDREEA_ASSETS = [
    {
        "name": "Revolut Andreea",
        "display_html": '<span class="bank-logo logo-revolut">R</span>Revolut Andreea',
        "mode": "savings_ron_daily",
        "start_balance_ron": REVOLUT_START_BALANCE_RON,
        "reference_date": REVOLUT_REFERENCE_DATE,
        "annual_rate": REVOLUT_ANNUAL_RATE,
        "withholding_tax": REVOLUT_WITHHOLDING_TAX,
        "note": "Dobânda brută este 2.50% pe an, cu impozit de 10% reținut la sursă. Soldul se compune zilnic pe baza dobânzii nete.",
    },
]

st.sidebar.markdown('<div class="sidebar-title">Control Panel</div>', unsafe_allow_html=True)
if st.sidebar.button("Refresh Manual", use_container_width=True):
    st.rerun()


def process_asset(asset, best_position, worst_position):
    display_html = asset.get("display_html", asset["name"])

    if asset["mode"] in {"crypto_manual", "crypto_binance_fallback"}:
        binance_snapshot, binance_error = get_binance_crypto_snapshot()

        if binance_snapshot is not None:
            current_usd = binance_snapshot["total_now"]
            basis_usd = current_usd

            return {
                "name": asset["name"],
                "display_html": display_html,
                "mode": "crypto_binance",
                "current_usd": current_usd,
                "current_eur": current_usd / eurusd_rate,
                "current_ron": current_usd * usdron_rate,
                "basis_usd": basis_usd,
                "today_pnl": binance_snapshot["today_pnl"],
                "today_pnl_pct": binance_snapshot["today_pnl_pct"],
                "positions": binance_snapshot["positions"],
                "note": asset["note"],
                "source": binance_snapshot["source"],
                "api_error": None,
            }, best_position, worst_position

        current_usd = asset["total_now"]
        basis_usd = asset["total_now"]
        return {
            "name": asset["name"],
            "display_html": display_html,
            "mode": "crypto_manual",
            "current_usd": current_usd,
            "current_eur": current_usd / eurusd_rate,
            "current_ron": current_usd * usdron_rate,
            "basis_usd": basis_usd,
            "today_pnl": asset["today_pnl"],
            "today_pnl_pct": asset["today_pnl_pct"],
            "positions": asset["positions"],
            "note": asset["note"],
            "source": "Manual fallback",
            "api_error": binance_error,
        }, best_position, worst_position

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
        current_eur = total_ron / eurron_rate

        return {
            "name": asset["name"],
            "display_html": display_html,
            "mode": "bvb_manual",
            "positions": positions,
            "invested_cost_basis_ron": invested_cost_basis_ron,
            "invested_now_ron": invested_now_ron,
            "cash_ron": cash_ron,
            "total_ron": total_ron,
            "invested_change_pct": invested_change_pct,
            "total_change_pct": total_change_pct,
            "current_usd": current_usd,
            "current_eur": current_eur,
            "current_ron": total_ron,
            "basis_usd": basis_usd,
            "note": asset["note"],
        }, best_position, worst_position

    if asset["mode"] == "manual_with_positions":
        positions = []
        failed = []
        total_positions_value = 0.0
        invested_cost_basis = 0.0
        extra_buys = asset.get("extra_buys", [])

        for ticker in asset["tickers"]:
            try:
                history = load_history(ticker)
                if history.empty:
                    failed.append(f"{ticker}: Fără istoric")
                    continue

                current_price = float(history["Close"].iloc[-1])
                base_buy_price = get_price_on_or_before(history, asset["buy_date"])
                if base_buy_price is None:
                    failed.append(f"{ticker}: Fără preț la data {asset['buy_date']:%d.%m.%Y}")
                    continue
            except Exception as e:
                failed.append(f"{ticker}: {e}")
                continue

            invested_amount = asset["amount_per_stock"]
            total_quantity = asset["amount_per_stock"] / base_buy_price

            for lot in extra_buys:
                if lot["ticker"] != ticker:
                    continue

                lot_amount = lot["amount"]
                lot_quantity = lot.get("quantity")

                if lot_quantity is None:
                    lot_buy_price = get_price_on_or_before(history, lot["buy_date"])
                    if lot_buy_price is None:
                        failed.append(f"{ticker}: Fără preț la data {lot['buy_date']:%d.%m.%Y}")
                        continue
                    lot_quantity = lot_amount / lot_buy_price

                invested_amount += lot_amount
                total_quantity += lot_quantity

            current_value = total_quantity * current_price
            profit_loss = current_value - invested_amount
            return_pct = (profit_loss / invested_amount * 100) if invested_amount else 0

            position = {
                "ticker": ticker,
                "price": current_price,
                "invested": invested_amount,
                "quantity": total_quantity,
                "current_value": current_value,
                "profit_loss": profit_loss,
                "return_pct": return_pct,
                "portfolio": asset["name"],
            }
            positions.append(position)
            invested_cost_basis += invested_amount
            total_positions_value += current_value
            best_position, worst_position = update_best_worst(position, best_position, worst_position)

        cash_total = asset.get("cash_now", 0.0)
        invested_now = total_positions_value
        total_now = invested_now + cash_total
        basis_usd = invested_cost_basis + cash_total
        invested_change_pct = ((invested_now - invested_cost_basis) / invested_cost_basis * 100) if invested_cost_basis else 0
        total_change_pct = ((total_now - basis_usd) / basis_usd * 100) if basis_usd else 0

        return {
            "name": asset["name"],
            "display_html": display_html,
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
            "current_eur": total_now / eurusd_rate,
            "current_ron": total_now * usdron_rate,
            "basis_usd": basis_usd,
        }, best_position, worst_position

    if asset["mode"] == "savings_eur_fixed":
        current_eur = asset["balance_eur"]
        current_usd = current_eur * eurusd_rate
        current_ron = current_eur * eurron_rate
        basis_usd = current_usd

        return {
            "name": asset["name"],
            "display_html": display_html,
            "mode": "savings_eur_fixed",
            "balance_eur": current_eur,
            "current_usd": current_usd,
            "current_eur": current_eur,
            "current_ron": current_ron,
            "basis_usd": basis_usd,
            "change_pct": 0.0,
            "note": asset["note"],
        }, best_position, worst_position

    if asset["mode"] == "savings_ron_daily":
        revolut = compound_daily_balance_with_tax(
            asset["start_balance_ron"],
            asset["annual_rate"],
            asset["withholding_tax"],
            asset["reference_date"],
        )

        current_ron = revolut["current_balance"]
        current_usd = current_ron / usdron_rate
        current_eur = current_ron / eurron_rate
        basis_usd = asset["start_balance_ron"] / usdron_rate

        return {
            "name": asset["name"],
            "display_html": display_html,
            "mode": "savings_ron_daily",
            "start_balance_ron": asset["start_balance_ron"],
            "current_ron": current_ron,
            "current_usd": current_usd,
            "current_eur": current_eur,
            "basis_usd": basis_usd,
            "days_elapsed": revolut["days_elapsed"],
            "annual_rate": asset["annual_rate"],
            "withholding_tax": asset["withholding_tax"],
            "net_interest_earned_ron": revolut["net_interest_earned"],
            "net_yield_pct": revolut["net_yield_pct"],
            "gross_interest_today": revolut["gross_interest_today"],
            "tax_today": revolut["tax_today"],
            "net_interest_today": revolut["net_interest_today"],
            "reference_date": asset["reference_date"],
            "note": asset["note"],
        }, best_position, worst_position

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

    return {
        "name": asset["name"],
        "display_html": display_html,
        "mode": "calculated",
        "tickers": asset["tickers"],
        "buy_date": asset["buy_date"],
        "positions": positions,
        "failed": failed,
        "cash_total": cash_total,
        "invested_total": invested_total,
        "total_positions_value": total_positions_value,
        "current_usd": current_usd,
        "current_eur": current_usd / eurusd_rate,
        "current_ron": current_usd * usdron_rate,
        "basis_usd": basis_usd,
        "change_pct": change_pct,
        "ticker_count": len(asset["tickers"]),
    }, best_position, worst_position


def build_group(name, display_html, results):
    current_usd = sum(r["current_usd"] for r in results)
    basis_usd = sum(r["basis_usd"] for r in results)
    change_pct = ((current_usd - basis_usd) / basis_usd * 100) if basis_usd else 0

    return {
        "name": name,
        "display_html": display_html,
        "results": results,
        "current_usd": current_usd,
        "current_eur": current_usd / eurusd_rate,
        "current_ron": current_usd * usdron_rate,
        "basis_usd": basis_usd,
        "change_pct": change_pct,
    }


def render_bucket_row(display_html, sub_line, current_usd, badge_text, positive=True):
    pill_class = "pill-pos" if positive else "pill-neg"
    st.markdown(
        f"""
        <div class="bucket-card">
            <div class="bucket-line">
                <div>
                    <div class="asset-name">{display_html}</div>
                    <div class="bucket-kicker">{sub_line}</div>
                </div>
                <div>
                    <div class="bucket-value">${current_usd:,.2f}</div>
                    <div class="{pill_class}" style="margin-top:6px;">{badge_text}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_crypto_detail(result):
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
            <b>Sursă:</b> {result.get('source', 'Manual')}<br><br>
            {result['note']}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if result.get("api_error") and result.get("source") == "Manual fallback":
        st.warning(f"Binance API indisponibil, s-a folosit fallback manual: {result['api_error']}")

    for i in range(0, len(result["positions"]), 2):
        cols = st.columns(2)
        for j, coin in enumerate(result["positions"][i:i + 2]):
            with cols[j]:
                pricing_line = ""
                if coin.get("pricing_status") == "unpriced":
                    pricing_line = '<div class="crypto-value">Fără pereche de preț detectată în Binance</div>'
                elif "today_pnl_pct" in coin:
                    pricing_line = f'<div class="crypto-value">{coin["today_pnl_pct"]:+.2f}% today</div>'

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
                                {pricing_line}
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def render_bvb_detail(result):
    st.markdown(
        f"""
        <div class="notice-box">
            <b>Capital investit inițial:</b> {result['invested_cost_basis_ron']:.2f} RON<br>
            <b>Valoare investită acum:</b> {result['invested_now_ron']:.2f} RON<br>
            <b>Randament pe investiție:</b> {result['invested_change_pct']:+.2f}%<br>
            <b>Cash:</b> {result['cash_ron']:.2f} RON<br>
            <b>Valoare totală:</b> {result['total_ron']:.2f} RON<br>
            <b>Estimare USD:</b> ${result['current_usd']:.2f}<br>
            <b>Estimare EUR:</b> €{result['current_eur']:.2f}<br><br>
            {result['note']}
        </div>
        """,
        unsafe_allow_html=True,
    )

    for pos in result["positions"]:
        badge_row = (
            f'<span class="bvb-badge bvb-ron">{pos["market_value_ron"]:.2f} RON</span>'
            f'<span class="bvb-badge bvb-usd">${pos["market_value_ron"] / usdron_rate:.2f}</span>'
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


def render_pie_ot_detail(result):
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
            st.caption(f"Investit: ${pos['invested']:.2f}")

    if result["failed"]:
        st.warning("Simboluri neîncărcate:")
        for item in result["failed"]:
            st.write(f"- {item}")


def render_calculated_detail(result):
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


def render_ing_detail(result):
    st.markdown(
        f"""
        <div class="notice-box">
            <b>Cont:</b> {result['display_html']}<br>
            <b>Sold EUR:</b> €{result['balance_eur']:.2f}<br>
            <b>Estimare USD:</b> ${result['current_usd']:.2f}<br>
            <b>Estimare RON:</b> {result['current_ron']:.2f} RON<br><br>
            {result['note']}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_revolut_detail(result):
    st.markdown(
        f"""
        <div class="notice-box">
            <b>Cont:</b> {result['display_html']}<br>
            <b>Sold inițial:</b> {result['start_balance_ron']:.2f} RON<br>
            <b>Sold curent:</b> {result['current_ron']:.2f} RON<br>
            <b>Dobândă brută estimată azi:</b> {result['gross_interest_today']:.2f} RON<br>
            <b>Impozit reținut azi:</b> {result['tax_today']:.2f} RON<br>
            <b>Dobândă netă estimată azi:</b> {result['net_interest_today']:.2f} RON<br>
            <b>Dobândă netă acumulată:</b> {result['net_interest_earned_ron']:.2f} RON<br>
            <b>Randament net:</b> {result['net_yield_pct']:+.4f}%<br>
            <b>Dobândă anuală brută:</b> {result['annual_rate'] * 100:.2f}%<br>
            <b>Impozit la sursă:</b> {result['withholding_tax'] * 100:.0f}%<br>
            <b>Zile compuse:</b> {result['days_elapsed']}<br>
            <b>Estimare USD:</b> ${result['current_usd']:.2f}<br>
            <b>Estimare EUR:</b> €{result['current_eur']:.2f}<br><br>
            {result['note']}
        </div>
        """,
        unsafe_allow_html=True,
    )


best_position = None
worst_position = None

alex_results = []
for asset in ALEX_ASSETS:
    result, best_position, worst_position = process_asset(asset, best_position, worst_position)
    alex_results.append(result)

andreea_results = []
for asset in ANDREEA_ASSETS:
    result, best_position, worst_position = process_asset(asset, best_position, worst_position)
    andreea_results.append(result)

alex_group = build_group(
    "ING NL Alex Total",
    '<span class="bank-logo logo-ing">I</span>ING NL Alex Total',
    alex_results,
)
andreea_group = build_group(
    "Revolut Andreea",
    '<span class="bank-logo logo-revolut">R</span>Revolut Andreea',
    andreea_results,
)

family_groups = [alex_group, andreea_group]

global_total_now_usd = sum(group["current_usd"] for group in family_groups)
global_total_in_usd = sum(group["basis_usd"] for group in family_groups)
global_total_now_eur = global_total_now_usd / eurusd_rate
global_total_now_ron = global_total_now_usd * usdron_rate
global_total_in_eur = global_total_in_usd / eurusd_rate
global_total_in_ron = global_total_in_usd * usdron_rate
global_profit_usd = global_total_now_usd - global_total_in_usd
global_profit_pct = (global_profit_usd / global_total_in_usd * 100) if global_total_in_usd else 0

st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">Family Dashboard</div>
        <div class="hero-title">My Assets</div>
        <div class="hero-subtitle">
            Dashboard extins cu crypto, BVB, PIE-uri și economii de familie. Vezi inițial totalul pe persoană, iar în interiorul lui Alex se deschid toate activele lui.
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
                <div class="summary-label">Total Assets (EUR)</div>
                <div class="summary-value">€{global_total_now_eur:,.2f}</div>
                <div class="summary-label">Capital introdus: €{global_total_in_eur:,.2f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with s3:
        st.markdown(
            f"""
            <div class="summary-card">
                <div class="summary-label">Total Assets (RON)</div>
                <div class="summary-value">{global_total_now_ron:,.2f} RON</div>
                <div class="summary-label">Capital introdus: {global_total_in_ron:,.2f} RON</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with s4:
        st.markdown(
            f"""
            <div class="summary-card">
                <div class="summary-label">Capital introdus (USD)</div>
                <div class="summary-value">${global_total_in_usd:,.2f}</div>
                <div class="summary-label">BVB și economiile sunt convertite live</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Family Buckets</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">La început vezi doar Alex și Andreea. În interiorul lui Alex apare tot ce are.</div>', unsafe_allow_html=True)

    for group in family_groups:
        render_bucket_row(
            group["display_html"],
            f"~€{group['current_eur']:,.2f} | ~{group['current_ron']:,.2f} RON",
            group["current_usd"],
            f"{group['change_pct']:+.2f}%",
            group["change_pct"] >= 0,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander(f"{alex_group['name']} • ${alex_group['current_usd']:,.2f} • {alex_group['change_pct']:+.2f}%", expanded=False):
        st.markdown('<div class="section-title">Alex Assets</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Crypto, BVB, PIE-uri și economiile lui Alex</div>', unsafe_allow_html=True)

        for result in alex_group["results"]:
            if result["mode"] in {"crypto_manual", "crypto_binance"}:
                row_pct = result["today_pnl_pct"]
                badge = f"Today {row_pct:+.2f}%"
                sub_line = f"Spot value: ${result['current_usd']:,.2f} | {result.get('source', 'Manual')}"
            elif result["mode"] == "bvb_manual":
                row_pct = result["invested_change_pct"]
                badge = f"Invested {row_pct:+.2f}%"
                sub_line = f"{result['total_ron']:,.2f} RON | ~${result['current_usd']:,.2f} | ~€{result['current_eur']:,.2f}"
            elif result["mode"] == "manual_with_positions":
                row_pct = result["invested_change_pct"]
                badge = f"Invested {row_pct:+.2f}%"
                sub_line = f"Invested now: ${result['invested_now']:,.2f} | Cash: ${result['cash_total']:,.2f}"
            elif result["mode"] == "savings_eur_fixed":
                row_pct = 0.0
                badge = "Fixed +0.00%"
                sub_line = f"€{result['balance_eur']:,.2f} | ~${result['current_usd']:,.2f} | ~{result['current_ron']:,.2f} RON"
            else:
                row_pct = result["change_pct"]
                badge = f"{row_pct:+.2f}%"
                cash_line = f" | Cash: ${result['cash_total']:,.2f}" if result["cash_total"] else ""
                sub_line = f"Investit: ${result['invested_total']:,.2f}{cash_line}"

            render_bucket_row(
                result["display_html"],
                sub_line,
                result["current_usd"],
                badge,
                row_pct >= 0,
            )

        for result in alex_group["results"]:
            st.markdown(f'<div class="subasset-title">{result["display_html"]}</div>', unsafe_allow_html=True)

            if result["mode"] in {"crypto_manual", "crypto_binance"}:
                render_crypto_detail(result)
            elif result["mode"] == "bvb_manual":
                render_bvb_detail(result)
            elif result["mode"] == "manual_with_positions":
                render_pie_ot_detail(result)
            elif result["mode"] == "calculated":
                render_calculated_detail(result)
            elif result["mode"] == "savings_eur_fixed":
                render_ing_detail(result)

    with st.expander(f"{andreea_group['name']} • ${andreea_group['current_usd']:,.2f} • {andreea_group['change_pct']:+.2f}%", expanded=False):
        st.markdown('<div class="section-title">Andreea Assets</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Pentru moment apare contul Revolut cu dobândă zilnică netă</div>', unsafe_allow_html=True)

        revolut_result = andreea_group["results"][0]
        render_bucket_row(
            revolut_result["display_html"],
            f"{revolut_result['current_ron']:,.2f} RON | azi net: {revolut_result['net_interest_today']:.2f} RON | ~€{revolut_result['current_eur']:,.2f}",
            revolut_result["current_usd"],
            f"Net {revolut_result['net_yield_pct']:+.2f}%",
            revolut_result["net_yield_pct"] >= 0,
        )
        render_revolut_detail(revolut_result)

with right:
    st.markdown('<div class="sidebar-card"><div class="sidebar-title">Allocation (Family • USD)</div>', unsafe_allow_html=True)

    total_value = sum(group["current_usd"] for group in family_groups)
    colors = [orange, "#06b6d4"]

    current_angle = 0
    segments = []
    legend_html = ""

    for i, group in enumerate(family_groups):
        color = colors[i % len(colors)]
        pct = (group["current_usd"] / total_value * 100) if total_value else 0
        angle = pct * 3.6
        segments.append(f"{color} {current_angle:.2f}deg {current_angle + angle:.2f}deg")
        legend_html += f"""
        <div class="legend-item">
            <div class="legend-color" style="background:{color};"></div>
            <div class="legend-text">
                {group['name']}<br>
                <span class="legend-sub">${group['current_usd']:,.2f} ({pct:.1f}%)</span>
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

    fx_date_text = fx["date"] if fx["date"] else "n/a"

    st.markdown(
        f"""
        <div class="sidebar-card">
            <div class="sidebar-title">FX Live</div>
            <div style="color:{text_main}; font-size:1rem; font-weight:800;">1 USD = {usdron_rate:.4f} RON</div>
            <div style="color:{text_main}; font-size:1rem; font-weight:800; margin-top:6px;">1 EUR = {eurron_rate:.4f} RON</div>
            <div style="color:{text_soft}; font-size:0.84rem; margin-top:6px;">Sursă: {fx['source']} | Data: {fx_date_text}</div>
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

st.caption("FX live din ECB • Total Assets în USD, EUR și RON • În Family Buckets vezi inițial doar Alex și Andreea • În interiorul lui Alex apare tot ce are")
