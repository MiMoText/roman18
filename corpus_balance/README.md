# Corpus Balance

Scripts and/or Jupyter notebooks in this directory describe and analyse the status quo of the corpus with respect to criteria like author gender, year of first publication, narrative form etc. It then compares it to the "baseline" of the BGRF.


## Usage

All the python dependencies are listed in `requirements.txt`. You can use `pip` or a similar tool to install them with

```
pip install -r requirements.txt
```

After that, you can start the notebook as usual with
```
jupyter notebook balance_analysis.ipynb
```

Part of the notebook uses data from our Wikibase instance. For this, you need to have access to the campus net of the University Trier. Everything else should be freely accessible.


## Testing

Some of the more intricate utility functions have been outsourced into their own `utils.py` module. For these, unit tests are provided in `test/test_utils.py`. To run the test suite, simply execute the following from the `corpus_balance/` directory:

```
python -m unittest discover
```

Failing test cases are regressions and should therefore be considered as bugs. 