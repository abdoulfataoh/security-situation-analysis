# security situation analysis

In this project, we use artificial intelligence models to analyze security situation in Burkina Faso

# Configuration 

We use `poetry` for virtual environment and dependencies management.

- Install poetry with pip
  ```sh
  python -m pip install poetry
  ```

- Install project dependancies, run the below command from project root folder
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

- Run scrapers
  ```sh
  python start.py
  ```
- Run user gui with streamlit
  ```sh
  streamlit run streamlit
  ```
