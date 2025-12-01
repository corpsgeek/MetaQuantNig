"""
MetaQuant Nigeria - Complete Project Structure Setup Script
Creates the entire directory structure and initial configuration files
"""

import os
from pathlib import Path

def create_project_structure():
    """Create the complete MetaQuant Nigeria project structure"""
    
    # Root directory
    root = Path("metaquant_nigeria")
    
    # Directory structure
    structure = {
        # Source code
        "src": {
            "__init__.py": "",
            
            # Data collection modules
            "data_collection": {
                "__init__.py": "",
                "idia_scraper.py": "# IDIA orderbook scraper using Selenium/Playwright",
                "ngx_scraper.py": "# NGX corporate actions scraper",
                "base_scraper.py": "# Base scraper class with common functionality",
                "scraper_manager.py": "# Orchestrates all scrapers",
            },
            
            # Database operations
            "database": {
                "__init__.py": "",
                "models.py": "# SQLAlchemy ORM models",
                "db_manager.py": "# Database connection and session management",
                "timeseries_db.py": "# TimescaleDB specific operations for tick data",
                "queries.py": "# Common SQL queries",
                "migrations": {
                    "__init__.py": "",
                    "001_initial_schema.sql": "-- Initial database schema",
                }
            },
            
            # Feature engineering
            "features": {
                "__init__.py": "",
                "orderbook_features.py": "# Microstructure features from orderbook",
                "corporate_action_features.py": "# Event-driven features",
                "technical_features.py": "# Technical indicators",
                "cross_sectional_features.py": "# Sector rotation, market breadth",
                "regime_features.py": "# Volatility regime detection",
                "feature_pipeline.py": "# Feature computation pipeline",
            },
            
            # Machine learning
            "ml": {
                "__init__.py": "",
                "data_preparation.py": "# Train/test splits, preprocessing",
                "models": {
                    "__init__.py": "",
                    "base_model.py": "# Base ML model interface",
                    "lightgbm_model.py": "# LightGBM implementation",
                    "xgboost_model.py": "# XGBoost implementation",
                    "ensemble_model.py": "# Model ensembling",
                },
                "backtesting.py": "# Walk-forward backtesting engine",
                "model_registry.py": "# Save/load trained models",
                "hyperparameter_tuning.py": "# Optuna-based tuning",
            },
            
            # Portfolio construction
            "portfolio": {
                "__init__.py": "",
                "optimizer.py": "# Mean-variance optimization (cvxpy)",
                "position_sizing.py": "# Risk-based position sizing",
                "rebalancer.py": "# Portfolio rebalancing logic",
                "constraints.py": "# Investment constraints (sector limits, etc.)",
            },
            
            # Execution & trading
            "execution": {
                "__init__.py": "",
                "order_manager.py": "# Order placement and tracking",
                "execution_algos.py": "# TWAP, VWAP algorithms",
                "slippage_model.py": "# Transaction cost estimation",
            },
            
            # Risk management
            "risk": {
                "__init__.py": "",
                "risk_metrics.py": "# VaR, CVaR, drawdown calculations",
                "position_limits.py": "# Risk limit monitoring",
                "stress_testing.py": "# Scenario analysis",
            },
            
            # Analytics & reporting
            "analytics": {
                "__init__.py": "",
                "performance.py": "# Performance metrics (Sharpe, Sortino, etc.)",
                "attribution.py": "# Performance attribution",
                "visualizations.py": "# Plotting utilities",
                "reports.py": "# Report generation",
            },
            
            # Utilities
            "utils": {
                "__init__.py": "",
                "logger.py": "# Logging configuration",
                "config.py": "# Configuration management",
                "validators.py": "# Data validation utilities",
                "constants.py": "# Constants (tickers, sectors, etc.)",
                "helpers.py": "# General helper functions",
            },
        },
        
        # GUI Application
        "gui": {
            "__init__.py": "",
            "main_app.py": "# Main ttkbootstrap application",
            "views": {
                "__init__.py": "",
                "dashboard_view.py": "# Main dashboard",
                "data_collection_view.py": "# Scraper controls and status",
                "feature_engineering_view.py": "# Feature computation interface",
                "model_training_view.py": "# ML model training interface",
                "backtesting_view.py": "# Backtesting results viewer",
                "portfolio_view.py": "# Current portfolio positions",
                "analytics_view.py": "# Performance charts and metrics",
            },
            "widgets": {
                "__init__.py": "",
                "custom_widgets.py": "# Reusable custom widgets",
                "charts.py": "# Matplotlib/Plotly chart widgets",
                "tables.py": "# Treeview tables for data display",
            },
            "styles": {
                "themes.py": "# Custom ttkbootstrap themes",
            },
        },
        
        # Configuration
        "config": {
            "config.yaml": "# Main configuration file",
            "database.yaml": "# Database connection settings",
            "scrapers.yaml": "# Scraper settings (URLs, intervals)",
            "features.yaml": "# Feature engineering parameters",
            "models.yaml": "# ML model hyperparameters",
            "portfolio.yaml": "# Portfolio construction settings",
            ".env.example": "# Environment variables template",
        },
        
        # Data directories
        "data": {
            "raw": {
                ".gitkeep": "",
            },
            "processed": {
                ".gitkeep": "",
            },
            "models": {
                ".gitkeep": "",
            },
            "backtest_results": {
                ".gitkeep": "",
            },
        },
        
        # Logs
        "logs": {
            ".gitkeep": "",
        },
        
        # Tests
        "tests": {
            "__init__.py": "",
            "test_data_collection": {
                "__init__.py": "",
                "test_idia_scraper.py": "",
                "test_ngx_scraper.py": "",
            },
            "test_database": {
                "__init__.py": "",
                "test_models.py": "",
                "test_queries.py": "",
            },
            "test_features": {
                "__init__.py": "",
                "test_orderbook_features.py": "",
                "test_feature_pipeline.py": "",
            },
            "test_ml": {
                "__init__.py": "",
                "test_models.py": "",
                "test_backtesting.py": "",
            },
            "test_portfolio": {
                "__init__.py": "",
                "test_optimizer.py": "",
            },
        },
        
        # Documentation
        "docs": {
            "README.md": "# MetaQuant Nigeria Documentation",
            "architecture.md": "# System Architecture",
            "data_schema.md": "# Database Schema",
            "api_reference.md": "# API Reference",
            "user_guide.md": "# User Guide",
        },
        
        # Scripts
        "scripts": {
            "setup_database.py": "# Initialize databases",
            "run_scrapers.py": "# Run data collection",
            "train_models.py": "# Train ML models",
            "backtest.py": "# Run backtests",
            "generate_report.py": "# Generate performance reports",
        },
        
        # Notebooks for analysis
        "notebooks": {
            ".gitkeep": "",
            "01_data_exploration.ipynb": "",
            "02_feature_analysis.ipynb": "",
            "03_model_experiments.ipynb": "",
            "04_backtest_analysis.ipynb": "",
        },
    }
    
    def create_structure(base_path, structure_dict):
        """Recursively create directory structure"""
        for name, content in structure_dict.items():
            path = base_path / name
            
            if isinstance(content, dict):
                # It's a directory
                path.mkdir(parents=True, exist_ok=True)
                create_structure(path, content)
            else:
                # It's a file
                path.parent.mkdir(parents=True, exist_ok=True)
                if not path.exists():
                    with open(path, 'w') as f:
                        f.write(content)
    
    # Create the structure
    create_structure(root, structure)
    
    # Create root-level files
    root_files = {
        "README.md": """# MetaQuant Nigeria

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
""",
        
        "requirements.txt": """# Core dependencies
pandas>=2.1.0
numpy>=1.24.0
scipy>=1.11.0
scikit-learn>=1.3.0

# Database
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
alembic>=1.12.0

# Web scraping
selenium>=4.15.0
playwright>=1.40.0
beautifulsoup4>=4.12.0
requests>=2.31.0
lxml>=4.9.0

# Machine learning
lightgbm>=4.1.0
xgboost>=2.0.0
optuna>=3.4.0
hmmlearn>=0.3.0

# Portfolio optimization
cvxpy>=1.4.0

# Time series
statsmodels>=0.14.0

# Visualization
matplotlib>=3.8.0
plotly>=5.18.0
seaborn>=0.13.0

# GUI
ttkbootstrap>=1.10.1
pillow>=10.1.0

# Configuration
pyyaml>=6.0
python-dotenv>=1.0.0

# Utilities
loguru>=0.7.0
tqdm>=4.66.0
joblib>=1.3.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.12.0

# Code quality
black>=23.11.0
flake8>=6.1.0
mypy>=1.7.0
""",
        
        ".gitignore": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Database
*.db
*.sqlite
*.sqlite3

# Logs
logs/*.log
*.log

# Data
data/raw/*
data/processed/*
!data/raw/.gitkeep
!data/processed/.gitkeep

# Models
data/models/*.pkl
data/models/*.joblib
!data/models/.gitkeep

# Environment
.env
.venv
config/.env

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Jupyter
.ipynb_checkpoints/
*.ipynb

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# Temporary
*.tmp
temp/
""",
        
        "setup.py": """from setuptools import setup, find_packages

setup(
    name="metaquant-nigeria",
    version="0.1.0",
    description="Quantitative trading system for Nigerian equities",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        line.strip() 
        for line in open('requirements.txt').readlines()
        if line.strip() and not line.startswith('#')
    ],
    python_requires=">=3.9",
)
""",
        
        "pyproject.toml": """[tool.black]
line-length = 100
target-version = ['py39', 'py310', 'py311']
include = '\\.pyi?$'

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
addopts = "-v --cov=src --cov-report=html --cov-report=term"
""",
    }
    
    for filename, content in root_files.items():
        filepath = root / filename
        with open(filepath, 'w') as f:
            f.write(content)
    
    print(f"✅ Project structure created at: {root.absolute()}")
    print("\n📁 Directory tree:")
    print_tree(root)
    
    print("\n🚀 Next steps:")
    print("1. cd metaquant_nigeria")
    print("2. python -m venv venv")
    print("3. source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
    print("4. pip install -r requirements.txt")
    print("5. Copy config/.env.example to config/.env and configure")
    print("6. python scripts/setup_database.py")

def print_tree(directory, prefix="", max_depth=3, current_depth=0):
    """Print directory tree structure"""
    if current_depth >= max_depth:
        return
    
    try:
        entries = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name))
    except PermissionError:
        return
    
    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        current_prefix = "└── " if is_last else "├── "
        print(f"{prefix}{current_prefix}{entry.name}")
        
        if entry.is_dir() and not entry.name.startswith('.'):
            extension = "    " if is_last else "│   "
            print_tree(entry, prefix + extension, max_depth, current_depth + 1)

if __name__ == "__main__":
    create_project_structure()