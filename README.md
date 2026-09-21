# House Price Prediction

House Price Prediction is an academic machine learning application that combines a
Random Forest regression model with a Streamlit interface for residential property
price estimation. It includes data preparation, training, model persistence,
interactive prediction, budget comparison, and MySQL account management.

Users can select purchase or rental scenarios and compare an estimate with a
budget. This is an educational prototype; estimates are not validated real estate
valuations.

## Objectives and features

- Demonstrate an end-to-end regression workflow.
- Estimate prices for Flat, Studio Flat, PG, and Bungalow selections.
- Illustrate purchase prices and a rule-based monthly rental approximation.
- Apply location-tier factors and compare estimates with a budget.
- Support registration, login, logout, and profile updates using MySQL.
- Provide a home page, property gallery, custom styling, and a command-line interface.

The gallery and testimonials are static interface content, not a live property
feed or evidence of model performance.

## Technology stack

| Component | Technology |
| --- | --- |
| Language | Python 3.13 |
| Web interface | Streamlit |
| Data processing | pandas, NumPy |
| Machine learning | scikit-learn, RandomForestRegressor |
| Model persistence | joblib |
| Accounts | MySQL Server, mysql-connector-python |
| Training | Jupyter Notebook, Matplotlib, Seaborn |

## Repository structure

| Path | Purpose |
| --- | --- |
| `dataset/housing_data.csv` | Housing dataset |
| `notebook/housing_model_training.ipynb` | Preparation, training, evaluation, and export |
| `models/house_price_model.pkl` | Saved model |
| `src/app.py` | Main Streamlit application and routing |
| `src/predict.py` | Interactive command-line prediction |
| `src/accounts.py` | Shared database access, validation, and password handling |
| `src/components/` | Header, footer, and prediction interface |
| `src/pages/` | Home, login, registration, and profile pages |
| `src/css/style.css` | Shared styles |
| `database/` | Initial schema and password-column upgrade |
| `requirements.txt` | Application dependencies |
| `tests/` | Account and page regression tests |

## Installation and local setup

### 1. Prerequisites and clone

Install Python 3.13, Git, and MySQL Server. MySQL CLI is a client and requires a
running server. Internet access is needed to install dependencies and load
externally hosted interface images.

```powershell
 git clone https://github.com/IamGroot786/House_Price_Prediction.git
 cd House_Price_Prediction
```

### 2. Create and activate the environment

Run these commands from the project root. For an existing working `venv`, skip
creation and activate it directly.

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
python -m venv venv
venv\Scripts\activate.bat
```

macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Use `deactivate` to leave the environment. If VS Code has a different interpreter
selected, run **Python: Select Interpreter**, choose `venv\Scripts\python.exe` on
Windows, and open a new terminal.

Verify activation with `python -c "import sys; print(sys.executable)"` and
`python -m pip --version`; both should point inside this project's `venv`.
Virtual environments contain absolute paths in activation scripts and launchers,
so recreate them after moving or renaming the project. Editing only `pyvenv.cfg`
does not repair those launchers.

The original local environment was repaired while retaining its packages. Its
previous scripts are backed up locally in `venv/activation-repair-backup.zip`;
the environment and backup are not included in Git.

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

For notebook execution and training, also install:

```powershell
python -m pip install notebook ipykernel matplotlib seaborn
```

The requirements file pins Streamlit, joblib, and scikit-learn to the verified
application environment, with version bounds for pandas and the MySQL connector.

### 4. Configure MySQL

Start MySQL Server and connect using your local administrative account:

```text
mysql -u root -p
```

For a new database, execute `database/schema.sql` in your MySQL client. For an
existing database, inspect `SHOW CREATE TABLE users` first:

- `username` must have a unique index; the app accepts up to 30 characters.
- `password` must be at least `VARCHAR(255)` to hold password hashes. If needed,
  execute `database/upgrade_password_storage.sql`.
- Use InnoDB for transactional account updates.

If a username unique index is missing, resolve any existing duplicate usernames
before running `ALTER TABLE users ADD UNIQUE KEY users_username_unique (username);`.
The password-column upgrade widens the column without changing existing values.
It was already applied to the original local database during the audit. Starting
the app does not migrate the database automatically.

Connection settings are centralized in `src/accounts.py` and read from environment
variables or an ignored `.streamlit/secrets.toml` file:

| Environment variable | Default |
| --- | --- |
| `DB_HOST` | `localhost` |
| `DB_PORT` | `3306` |
| `DB_USER` | `root` |
| `DB_PASSWORD` | Empty |
| `DB_NAME` | `house_price_prediction` |

For example, set the password in the PowerShell terminal that launches the app:

```powershell
$env:DB_PASSWORD = 'your-local-mysql-password'
```

Alternatively, create `.streamlit/secrets.toml` locally:

```toml
[mysql]
host = "localhost"
port = 3306
user = "root"
password = "your-local-mysql-password"
database = "house_price_prediction"
```

Environment variables override the secrets file. A `.env` file is not loaded
automatically. Do not commit credentials. The original local connection settings
were preserved in an ignored secrets file; a fresh clone must configure its own.

New accounts and password changes use salted PBKDF2-SHA256 hashes. Existing
plaintext passwords remain usable and are upgraded when changed through Profile.

### 5. Start the web application

```powershell
python -m streamlit run src/app.py
```

Activation is optional on Windows; this also works:

```powershell
.\venv\Scripts\python.exe -m streamlit run src/app.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`.
Register through **Login → Create Account**, sign in, and select **Predict**.
Choose the transaction, property category, and location tier; enter the property
details and budget, then select **Estimate Price**. For rental mode, enter a
monthly rental budget to match the estimated amount's time period.

Home and account pages remain available if the saved model is missing; Predict
displays an error.

### 6. Run the command-line interface

```powershell
python src/predict.py
```

Follow the prompts to choose purchase or rent and enter property attributes.
This script loads the model directly, has no login flow, and does not apply the
web application's location-tier factors.

## Model training and evaluation

The committed notebook records 1,460 records and 81 original columns. It constructs
ten inputs: `area`, `bedrooms`, `bathrooms`, `floors`, `parking`, `garden`, `sharing`,
`meal_included`, `building_age`, and `house_type`. The target is `SalePrice`.

| Setting | Value |
| --- | --- |
| Estimator | RandomForestRegressor |
| Trees | 200 |
| Training/test split | 80% / 20% |
| Split and model random states | 42 |
| Recorded notebook test R² | Approximately 0.8509 |

This score is a recorded notebook result, not a newly reproduced benchmark or an
85.09% prediction accuracy claim.

```powershell
cd notebook
python -m notebook
```

Open `housing_model_training.ipynb` and execute its cells in order. Relative paths
expect the notebook directory as the working directory. The final export
overwrites `models/house_price_model.pkl`. Some features are generated randomly
without a fixed NumPy seed, so rerunning can produce a different score.

## Current estimation rules

The web app applies these fixed multipliers after model prediction:

| Location tier | Multiplier |
| --- | --- |
| Tier 1 City | 1.5 |
| Tier 2 City | 1.2 |
| Tier 3 City | 0.9 |

Rental mode multiplies the adjusted estimate by `0.005` to approximate a monthly
amount. These factors are manually defined assumptions, not learned from
location-specific or rental training data.

## Known limitations

- **Dataset and currency:** The model predicts dataset `SalePrice` values, while
  the interface labels amounts in rupees. No INR conversion or Indian-market
  validation is established. Dataset source and currency need explicit documentation.
- **Synthetic features:** Training randomly assigns `garden` and `house_type`.
  These do not represent observed property characteristics.
- **Constant features:** `sharing` and `meal_included` are always zero during
  training, so their effects cannot be learned.
- **Floor definition:** Training maps `TotRmsAbvGrd` (rooms above ground) to `floors`.
- **Category encoding:** Training generates house-type codes from 1 to 4, while
  the web interface uses 0 to 3. The CLI uses 1 to 4, but training labels are random.
- **Input consistency:** Interfaces use different defaults and available fields
  for some categories. Training calculates building age relative to 2025.
- **Evaluation:** One train/test split does not validate the app's location or
  rental adjustments.
- **Account migration:** Legacy plaintext passwords remain until users change them.
  Password hashing and regression tests alone do not establish deployment readiness.

## Verification

With the environment activated:

```powershell
python -B -m unittest discover -s tests -v
```

The tests use simulated database connections and Streamlit's AppTest. They do not
create, change, or delete real accounts. Coverage includes validation, password
hashing, transaction failures, page routing, logout, and saved-model prediction.

## Troubleshooting

| Problem | Action |
| --- | --- |
| Missing Python module | Activate this project's environment and install `requirements.txt`. |
| Activation or pip uses an old path | Recreate a moved environment; confirm the interpreter and pip paths. |
| MySQL connection fails | Check the running server and environment variables or local secrets. |
| Unknown database or missing table | Run the database initialization SQL. |
| Password save fails on an old schema | Check the password-column width and apply the upgrade SQL. |
| Model missing | Check `models/house_price_model.pkl` or export it from the notebook. |
| Model compatibility error | Install the declared dependencies or retrain in the runtime environment. |
| Notebook cannot find CSV | Run it from `notebook` and confirm the dataset exists. |
| Images do not load | Check access to the external image hosts. |

## Future improvements

- Replace synthetic features with documented, observed property data.
- Standardize preprocessing and category encoding across training and both interfaces.
- Align the dataset, currency, geography, and supported property types.
- Add baselines, cross-validation, MAE, RMSE, and error analysis.
- Replace fixed location and rent factors with validated models.
- Add dataset exploration and feature-importance analysis.
- Complete legacy password migration and further deployment hardening.
- Automate the regression suite in CI and expand integration coverage.

## Author and dataset reference

Aditya Rawal — GitHub: [IamGroot786](https://github.com/IamGroot786).

The dataset follows the schema of *House Prices: Advanced Regression Techniques*.
Consult its original source for context and applicable usage terms.
