'''
This Script generates an xml-file from txt-data.
'''

import logging
from pathlib import Path

import lxml.etree as ET

from dialects.dialects import EpubDialects

#set a path where your data are saved
SOURCE_PATH = "sources/"
#set a path where you want to save your data
SAVE_PATH = 'results/'

# Namespace to use during XML creation
NSMAP = {
    'tei': 'http://www.tei-c.org/ns/1.0',
    'xml': 'http://www.w3.org/XML/1998/namespace',
}


def determine_dialect(text):
    '''Factory function which parses the text and returns a appropriate dialect object.'''
    Dialect = None
    if 'www.rousseauonline.ch' in text:
        Dialect = EpubDialects['rousseauonline']
    elif 'Exporté de Wikisource' in text:
        Dialect = EpubDialects['wikisource']
    if Dialect is None:
        logging.warn('could not recognize a known source dialect')
    return Dialect()


def open_file(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    return text


def prepare(save_path):
    '''Ensure that the configured `SAVE_PATH` exists.'''
    p = Path(save_path)
    p.mkdir(parents=True, exist_ok=True)
    
    if any(p.iterdir()):
        msg = f'SAVE_PATH "{p.absolute()}" is not empty, we might override previous results.'
        logging.warning(msg)
    
    return p


def write_results(xml, save_path, file_name):
    """Write results to configured `SAVE_PATH`."""
    name = file_name.replace('.txt', '.xml')
    p = Path(save_path) / name
    p = str(p.absolute())
    
    logging.debug(f'writing results to {p}.')
    
    # Pretty-print the xml.
    ET.indent(xml)
    xml.write(p, encoding='utf-8')


def main():
    logging.basicConfig(level=logging.WARNING)

    prepare(SAVE_PATH)

    for src_file in Path(SOURCE_PATH).iterdir():
        if src_file.is_file() and src_file.name.endswith('.txt'):
            logging.debug(f'Processing {src_file}')
            text = open_file(src_file)
            dialect = determine_dialect(text)
            logging.debug(f'identified source dialect as {dialect}')

            xml = dialect.transform(text, src_file.name)
            write_results(xml, SAVE_PATH, src_file.name)


if __name__ == '__main__':
    main()