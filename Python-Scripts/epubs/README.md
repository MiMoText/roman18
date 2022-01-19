# Epub conversion

This script is used to convert the markdown files, which we generate from epub files with the help of `Calibre`, into TEI XML.


## Prerequisites

This script uses LXML for the XML handling. You can install it with your prefered package management tool, e.g. `pip` or `conda`:

```
pip install lxml    # or
conda install -c anaconda lxml 
```


## Usage

The script expects the source files in `.txt` files at the location given in the `SOURCE_PATH` constant. It will attempt to write the resulting `.xml` files to the location given in the `SAVE_PATH` constant. If this location is not empty, it will issue a warning, but proceed to (over)write the files there. 

If you are fine with these defaults, you can simply run the script like this:

```bash
python epubs.py
```


## Configuration

The runtime parameters can be modified by using command line arguments (recommended) or by overwriting the respective constants in the script itself. To list all available options just run:

```bash
python epubs.py --help
```

If you e.g. want to convert only a single source file, you could run:

```bash
python epubs.py -s path/to/file.txt
```

The script tries to determine the correct handling for source files from various origins, e.g. wikisource or rousseauonline.ch. If the auto-detection fails, you can enforce usage of a certain source dialect by specifying a `-d` / `--force-dialect` parameter:

```bash
python epubs.py -s path/to/file.txt -d "WIKISOURCE"
```

Available dialects are at the moment "WIKISOURCE", "WIKISOURCE_NC" (wikisource without any chapters), "ROUSSEAU" and "BASE". If you are just interested which dialect the auto-detection would choose, without actually converting the file, you can issue the `--only-probe-dialect` option:

```bash
python epubs.py -s path/to/file.txt --only-probe-dialect
```


## Tests

The test suite can be run by executing the following inside this directory:

```bash
python3 -m unittest discover
```

Failing tests are regressions and should therefore be considered as bugs.


## Known issues

- The XML build up of the main text body currently does not differentiate between different orders of headings. Every heading will result in its own chapter div element.
- The script can not differentiate between regular chapters and letters (in epistolary novels).
