House Price Prediction

House Price Prediction is an academic machine learning application that combines a Random Forest regression model with a Streamlit web interface to demonstrate residential property price estimation. The project includes data preparation, model training, model persistence, interactive prediction, budget comparison, and MySQL-based account management.

Users can enter property details, select a purchase or rental scenario, and compare the resulting estimate against a budget. The current implementation is an educational prototype; its estimates should not be interpreted as validated real estate valuations.

Objectives

Demonstrate an end-to-end machine learning workflow for a regression problem.

Provide an interactive interface for entering residential property attributes.

Illustrate purchase-price estimation and a rule-based monthly rent approximation.

Compare an estimated amount with a user-defined budget.

Integrate registration, login, and profile management with a relational database.

Features

Property estimation: Generates an estimate using a saved Random Forest model.

Property categories: Provides Flat, Studio Flat, PG, and Bungalow selections with category-specific inputs.

Purchase and rental modes: Supports purchase estimates and a fixed-factor rental approximation.

Location tiers: Applies predefined adjustment factors for three city tiers.

Budget comparison: Displays the difference between the estimate and the entered budget.

Account management: Includes registration, login, logout, and username/password updates.

Web presentation: Includes a home page, shared header and footer, custom CSS, and a property image gallery.

Command-line prediction: Provides an alternative interactive prediction script.

The gallery and testimonials are static interface content, not a live property feed or evidence of model performance.

Technology Stack

Component

Technology

Programming language

Python

Web interface

Streamlit

Data processing

pandas, NumPy

Machine learning

scikit-learn, RandomForestRegressor

Model persistence

joblib

Account database

MySQL Server, mysql-connector-python

Training environment

Jupyter Notebook

Additional libraries

Matplotlib, Seaborn, Pillow

Repository Structure

Path

Purpose

dataset/housing_data.csv

Housing dataset used by the training notebook

notebook/housing_model_training.ipynb

Data preparation, training, evaluation, and model export

models/house_price_model.pkl

Saved model loaded by the application

src/app.py

Main Streamlit application

src/predict.py

Interactive command-line prediction script

src/components/header.py

Shared header

src/components/footer.py

Shared footer

src/css/style.css

Application styles

src/pages/landing_page.py

Home page content

src/pages/login.py

Login interface

src/pages/register.py

Account registration

src/pages/profile.py

Account profile updates

Installation and Local Setup

1. Prerequisites

Install the following:

Python and pip. The committed training notebook records Python 3.13.3.

Git, or download and extract the repository ZIP.

MySQL Server, running locally. MySQL CLI is a client and requires a running server.

An internet connection for dependency installation and externally hosted interface images.

Dependency versions are not currently pinned. A fresh installation may require compatibility adjustments, particularly when loading the saved scikit-learn model.

2. Clone the Repository

git clone https://github.com/IamGroot786/House_Price_Prediction.git
cd House_Price_Prediction

3. Create and Activate a Virtual Environment

On Windows PowerShell:

python -m venv .venv
.\.venv\Scripts\Activate.ps1

On Windows Command Prompt:

python -m venv .venv
.venv\Scripts\activate.bat

On macOS or Linux:

python3 -m venv .venv
source .venv/bin/activate

4. Install Dependencies

For the web application and prediction script:

python -m pip install --upgrade pip
python -m pip install streamlit pandas numpy scikit-learn joblib mysql-connector-python Pillow

For notebook execution and model training, also install:

python -m pip install notebook ipykernel matplotlib seaborn

The repository does not currently include a requirements file. These commands are based on the imports in the committed source code and notebook.

5. Configure MySQL

Connect to your local MySQL server using an administrative account:

mysql -u root -p

Create the application database and a minimal users table compatible with the current account-management queries:

CREATE DATABASE IF NOT EXISTS house_price_prediction;
USE house_price_prediction;

CREATE TABLE IF NOT EXISTS users (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

Configure the mysql.connector.connect(...) settings in each of these files to match your local server:

src/pages/login.py

src/pages/register.py

src/pages/profile.py

The database name must match the database created above. The current code stores connection settings directly in these files; it does not automatically read a .env file.

Account security: The current prototype stores user passwords in plain text and includes hardcoded database credentials. Use disposable local demonstration accounts. Password hashing and externalized credentials are required before public deployment. Do not commit your own database credentials.

6. Start the Web Application

Run this command from the repository root:

python -m streamlit run src/app.py

Open the local URL shown in the terminal, typically http://localhost:8501.

Open Login, then Create Account to register.

Sign in and select Predict.

Choose the transaction type, property category, and location tier.

Enter the property details and budget.

Select Estimate Price to view the estimate and budget difference.

For rental mode, enter a monthly rental budget so that the comparison uses the same time period as the estimated rent.

7. Run the Command-Line Interface

From the repository root:

python src/predict.py

Follow the prompts to select purchase or rent, choose a property category, and enter its attributes. This script loads the saved model directly and does not use the web login flow. It also does not apply the web application's location-tier adjustment.

Model Training and Evaluation

The committed notebook contains a dataset summary of 1,460 records and 81 original columns. It constructs ten model inputs:

area, bedrooms, bathrooms, floors, parking, garden, sharing, meal_included, building_age, and house_type.

The target is SalePrice. Training uses:

Setting

Value

Estimator

RandomForestRegressor

Number of trees

200

Training/test split

80% / 20%

Split random state

42

Model random state

42

Saved notebook test R²

Approximately 0.8509

The R² value is a recorded notebook result, not a newly reproduced benchmark. It is not equivalent to an 85.09% prediction accuracy claim.

To run training:

cd notebook
python -m notebook

Open housing_model_training.ipynb and execute its cells in order with the installed environment selected as the kernel. Its relative paths expect execution from the notebook directory. The final export overwrites models/house_price_model.pkl.

The notebook generates some features randomly without a fixed NumPy seed, so rerunning it may produce a different score even though the model and split use fixed random states.

Current Estimation Rules

After obtaining the model output, the web application applies these fixed location factors:

Location selection

Multiplier

Tier 1 City

1.5

Tier 2 City

1.2

Tier 3 City

0.9

For rental mode, the adjusted estimate is multiplied by 0.005 to produce an approximate monthly amount. These factors are manually defined assumptions; they are not learned from location-specific or rental training data.

Known Limitations

The following issues exist in the current implementation and should be addressed before treating the application as a reliable valuation system:

Dataset and currency alignment: The model uses the dataset's SalePrice values, while the interface labels results in rupees. The code does not establish an INR conversion or validate these values against an Indian housing market. The dataset follows the Ames/Kaggle House Prices schema; source and currency documentation should be made explicit.

Randomly assigned features: The notebook randomly generates garden and house_type, so those fields do not represent observed property characteristics.

Constant training features: sharing and meal_included are always zero during training. Their effects cannot be learned from this training data.

Floor definition mismatch: The notebook assigns TotRmsAbvGrd to floors, although that source field represents rooms above ground.

Property-category encoding mismatch: Training generates house-type codes from 1 to 4, while the web app encodes categories from 0 to 3. The command-line script uses 1 to 4, but the training labels are still randomly assigned.

Input consistency: The interfaces supply different defaults and available fields for some categories. Building age is calculated relative to a fixed year of 2025 in training.

Evaluation scope: The saved score comes from one train/test split. It does not validate the app's subsequent location and rent adjustments.

Deployment readiness: Dependency pinning, secure account handling, and automated verification remain future work.

Troubleshooting

Problem

Suggested action

Missing Python module

Activate the virtual environment and install the dependencies listed above.

MySQL connection fails

Confirm MySQL Server is running and check the connection settings in all three account pages.

Unknown database or missing users table

Run the database initialization SQL above.

Model file not found

Confirm models/house_price_model.pkl exists or execute the training notebook to export it.

Model compatibility warning or loading error

Use a compatible scikit-learn environment or retrain and export the model in the same environment used to run the app.

Notebook cannot find the CSV

Run the notebook with notebook as its working directory and confirm the dataset exists.

Images do not load

Check internet access; the interface uses externally hosted images.

Future Improvements

Replace synthetic feature assignments with documented, observed property data.

Standardize preprocessing and category encoding across training and both prediction interfaces.

Align the dataset, currency, geography, and supported property types.

Add baseline comparisons, cross-validation, MAE, RMSE, and error analysis.

Replace fixed rental and location assumptions with validated data-driven approaches.

Add a dataset exploration dashboard and feature-importance analysis.

Secure account management and centralize database configuration.

Add pinned dependencies and automated checks.

Author

Aditya Rawal
GitHub: IamGroot786

Dataset Reference

The committed dataset follows the schema of House Prices: Advanced Regression Techniques. Consult the original source for dataset context and applicable usage terms.

