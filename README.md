# House Price Prediction

Streamlit house price estimator with MySQL accounts.

## Run locally (PowerShell)

```powershell
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run src/app.py
```

Run these commands from the project folder. In Command Prompt, activate with
`venv\Scripts\activate.bat` instead. Use `deactivate` to leave the environment.
If VS Code already has a different interpreter selected, run **Python: Select
Interpreter** and choose `venv\Scripts\python.exe`, then open a new terminal.

Verify activation with `python -c "import sys; print(sys.executable)"` and
`python -m pip --version`; both should point inside this project's `venv`.
Activation is optional: `.\venv\Scripts\python.exe -m streamlit run src/app.py`
also works directly.

Use Python 3.13 to create a fresh environment with `python -m venv venv`, then
install `requirements.txt`. Virtual environments contain absolute paths in
activation scripts and executable launchers, so recreate them after moving or
renaming the project. Editing only `pyvenv.cfg` does not repair those launchers.
The local environment's stale paths were repaired while retaining its installed
packages; the previous scripts are backed up in `venv/activation-repair-backup.zip`.

The MySQL server must be running. Connection settings use environment variables:
`DB_HOST` (default `localhost`), `DB_PORT` (`3306`), `DB_USER` (`root`),
`DB_PASSWORD` (empty by default), and `DB_NAME` (`house_price_prediction`).
Set them in the terminal that launches Streamlit. Alternatively, create
`.streamlit/secrets.toml` with a `[mysql]` section containing `host`, `port`,
`user`, `password`, and `database`. Environment variables override these values.
This local secrets file is ignored by Git. A `.env` file is not loaded
automatically. The previous hardcoded database password has been removed from
the page code. The existing local connection settings were preserved in the
ignored secrets file during the audit.

For a new database, run `database/schema.sql` in your MySQL client.
For an existing database, check `SHOW CREATE TABLE users` first:

- `password` must be at least `VARCHAR(255)` to store password hashes. If needed,
  run `database/upgrade_password_storage.sql` (already applied to the local
  database during the audit).
- `username` must have a unique index so simultaneous registrations cannot create
  duplicates. If missing, resolve any existing duplicate usernames before running
  `ALTER TABLE users ADD UNIQUE KEY users_username_unique (username);`.
- Use the InnoDB engine for transactional account updates.

New accounts and password changes store salted PBKDF2-SHA256 hashes. Existing
plaintext passwords remain usable and are upgraded when changed through Profile.
Starting the app does not migrate the database. The one-time local schema upgrade
only widened the password column; it did not change any existing account values.

The saved model belongs in `models/house_price_model.pkl`. Home and account pages
remain available if it is missing; the Predict page displays an error.

## Verification

```powershell
.\venv\Scripts\python.exe -B -m unittest discover -s tests -v
```

These regression tests use simulated database connections and Streamlit's AppTest;
they do not create, change, or delete real accounts.
