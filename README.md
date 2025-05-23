# Data Preprocessor Module (Colab) 🛠️
This Google Colab notebook is a dedicated module for applying common data preprocessing techniques to a raw dataset (typically in CSV format). It provides an interactive UI to configure and apply these transformations, preparing the data for machine learning model training.

## Purpose

The primary goal of this module is to:
1.  Enable users to **upload a dataset**.
2.  Provide controls to define and apply **missing value imputation** strategies.
3.  Offer methods for **categorical feature encoding** (One-Hot Encoding, Label Encoding).
4.  Allow **numerical feature scaling** (StandardScaler, MinMaxScaler).
5.  Output a **cleaned, preprocessed dataset** ready for model training or further analysis.

This module is conceptualized as the second "microservice" in a series of modular Colab notebooks, typically following a "Data Loader & Validator" module.

## Features

* **Interactive CSV Upload:** Load the dataset to be preprocessed.
* **Column Type Configuration:** Interactively review and confirm numerical and categorical columns.
* **Missing Value Imputation:**
    * Strategies for numerical columns: `mean`, `median`, or `None`.
    * Strategies for categorical columns: `most_frequent`, `constant` fill, or `None`.
* **Categorical Encoding:**
    * Select specific categorical columns for encoding.
    * Choose between `One-Hot Encoding` or `Label Encoding`, or `None`.
* **Numerical Scaling:**
    * Select specific numerical columns for scaling (including those newly created by One-Hot Encoding).
    * Choose between `StandardScaler` or `MinMaxScaler`, or `None`.
* **Preview & Status:** View the head of the processed DataFrame and status messages.
* **Download Processed Data:**
    * Option to download the transformed data as a `CSV` file.
    * Option to download the transformed data as a `Pickle` file (preserves data types better).

## Order of Operations

Preprocessing steps are applied in the following sequence:
1.  Missing Value Imputation
2.  Categorical Encoding
3.  Numerical Scaling

## How It Fits in a Workflow

1.  **Input:** A CSV file containing a dataset (ideally, one that has already been loaded and initially explored, e.g., output from a "Data Loader" module).
2.  **Process:** User configures and applies imputation, encoding, and scaling steps via the UI.
3.  **Output:**
    * A preprocessed pandas DataFrame (available in the Colab environment as `df_processed`).
    * Downloadable `processed_data.csv` and `processed_data.pkl` files. These can serve as input to a "Model Trainer" module.

## Setup (within Google Colab)

1.  Open the notebook in Google Colab.
2.  Run the cells in order. The necessary Python libraries (`pandas`, `numpy`, `scikit-learn`, `ipywidgets`) are installed automatically.
3.  No external API keys or special configurations are needed.

## Usage Instructions

1.  **Run Cells:** Execute the Colab cells sequentially.
    * Cell 1: Displays the introduction.
    * Cell 2: Installs libraries and performs setup.
    * Cell 3: Renders the main UI.
    * Cell 4: Defines the backend preprocessing logic (triggered by button clicks in UI).
2.  **Upload Data:**
    * Click the "Upload Raw CSV" button in Section 1 of the UI.
    * Select the CSV file from your local system.
    * A preview of the original data and auto-detected column types will appear.
3.  **Configure Column Types (Section 2):**
    * Review the "Numerical Cols" and "Categorical Cols" selections. Adjust these `SelectMultiple` widgets if the auto-detection was not perfect for your specific needs.
4.  **Configure Preprocessing Steps (Sections 3-5):**
    * **Missing Value Imputation:** Choose your strategies for numerical and categorical columns. If 'constant' is chosen for categorical, specify the fill value.
    * **Categorical Encoding:** Select the categorical columns you wish to encode and the method (`One-Hot Encode`, `Label Encode`, or `None`).
    * **Numerical Scaling:** Select the numerical columns to scale (note: options here will update if One-Hot Encoding creates new numerical columns) and the scaling method.
5.  **Apply Preprocessing (Section 6):**
    * Click the "Apply Preprocessing" button.
    * Status messages will appear in the main output area at the bottom.
    * A preview of the first 5 rows of the processed data will be shown.
6.  **Download Processed Data (Section 6):**
    * After successful preprocessing, the "Download Processed CSV" and "Download Processed Pickle" buttons will be enabled. Click them to save your transformed dataset.

## Output of this Module

* **DataFrame in Memory:** The processed data is stored in a pandas DataFrame named `df_processed`.
* **Downloadable Files:** `processed_data.csv` and `processed_data.pkl`.

## Future Enhancements (Conceptual)

* More sophisticated encoding options (e.g., Target Encoding, Feature Hashing).
* Feature creation capabilities (e.g., polynomial features, date part extraction).
* Outlier detection and handling methods.
* Dimensionality reduction techniques (PCA).
* Option to save and load preprocessing pipeline steps (e.g., a scikit-learn `Pipeline` object).

## Contributing

As a conceptual module, improvements can be made directly within the Colab notebook structure.
1.  Fork the (conceptual) repository.
2.  Create a new branch.
3.  Commit your changes.
4.  Push to the branch.
5.  Open a Pull Request.

