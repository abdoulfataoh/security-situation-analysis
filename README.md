# security situation analysis

In this project, we use artificial intelligence models to analyze security situation in Burkina Faso

# Configuration 

We use `poetry` for virtual environment and dependencies management.

- To install poetry with pip

  ```sh
    python -m pip install poetry
  ```

- To install project dependancies, run the below command from project root folder

  ```sh
  poetry install
  ```

- Enable virtual environment

  ```sh
  poetry shell
  ``` 

# General architecture
<p align="center">
    <img width="320" src="https://github.com/abdoulfataoh/security-situation-analysis/blob/main/doc/architecture.png">
</p>


# Run project

```python start.py``` to run scrapers

```streamlit run streamlit``` to run user gui with streamlit
