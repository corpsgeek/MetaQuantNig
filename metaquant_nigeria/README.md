# MetaQuant Nigeria

Quantitative trading system for Nigerian equities with ML-powered alpha generation.

## Features
- Real-time orderbook data collection from IDIA
- Corporate actions scraping from NGX
- Advanced feature engineering (microstructure, events, technicals)
- Machine learning models (LightGBM, XGBoost)
- Portfolio optimization and risk management
- Interactive GUI built with ttkbootstrap

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Configure databases: Edit `config/database.yaml`
3. Set up environment: Copy `config/.env.example` to `config/.env`
4. Initialize database: `python scripts/setup_database.py`
5. Run GUI: `python -m gui.main_app`

## Documentation
See `docs/` for detailed documentation.
