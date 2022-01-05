# Epub conversion

This script is used to convert the markdown files, which we generate from epub files with the help of `Calibre`, into TEI XML.


## Prerequisites

This script has no external dependencies. It expects the source files in `.txt` files at the location given in the `SOURCE_PATH` constant. It will attempt to write the resulting `.xml` files to the location given in the `SAVE_PATH` constant. If this location is not empty, it will issue a warning, but proceed to (over)write the files there.


## Usage

```bash
python epubs.py
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
