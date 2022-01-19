#!/usr/bin/env python3
'''
This Script generates an xml-file from txt-data.
'''

import argparse
import logging
from pathlib import Path

import lxml.etree as ET

from dialects.dialects import EpubDialects

# set a path where your data are saved
SOURCE_PATH = 'sources/'
# set a path where you want to save your data
RESULTS_PATH = 'results/'
# Force usage of a specific epub source dialect.
# If set to something other than None it skips the auto-detection of the most
# appropriate dialect.
# Valid values are: 'BASE', 'ROUSSEAU', 'WIKISOURCE', 'WIKISOURCE_NC' and None
FORCE_DIALECT = None
# Whether to print low-level debug messages
VERBOSE = False

# Namespace to use during XML creation
NSMAP = {
    'tei': 'http://www.tei-c.org/ns/1.0',
    'xml': 'http://www.w3.org/XML/1998/namespace',
}


def determine_dialect(text, force_dialect=None):
    '''Factory function which parses the text and returns a appropriate dialect object.'''
    # If `force_dialect` is given, skip auto-detection.
    if force_dialect is not None and force_dialect != '':
        Dialect = EpubDialects[force_dialect]
    else:
        Dialect = None
        if 'www.rousseauonline.ch' in text:
            Dialect = EpubDialects['ROUSSEAU']
        elif 'Exporté de Wikisource' in text:
            # Determine whether there are chapters or not.
            if text.count('\n### ') > 1:
                Dialect = EpubDialects['WIKISOURCE']
            else:
                Dialect = EpubDialects['WIKISOURCE_NC']
        if Dialect is None:
            logging.warning('could not recognize a known source dialect')
            Dialect = EpubDialects['BASE']

    return Dialect.value()


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


def dialect_arg(string):
    if not string:
        return None
    try:
        EpubDialects[string]
        msg = '\n'.join((
            f'the requested source dialect {string} does not exist.',
            'Valid options are:',
            '\n'.join([d.name for d in EpubDialects])
        ))
        logging.warning(msg)
        return string
    except KeyError:
        return None


def main(config):
    source = Path(config.source_path)
    files = [source] if source.is_file() else source.iterdir()

    prepare(config.results_path)

    for src_file in files:
        if src_file.is_file() and src_file.name.endswith('.txt'):
            logging.debug(f'Processing {src_file}')
            text = open_file(src_file)
            dialect = determine_dialect(text, config.force_dialect)

            if config.only_probe_dialect:
                logging.warning(f'"{src_file}" would use dialect {dialect}')
                return
            
            else:
                logging.debug(f'using source dialect "{dialect}"')
                xml = dialect.transform(text, src_file.name)
                write_results(xml, config.results_path, src_file.name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert markdown file (generated from epub) to TEI.'
    )
    parser.add_argument(
        '-s', '--source-path',
        metavar='SOURCE_PATH',
        default=SOURCE_PATH,
        help='path to directory where plain text input files are, or to one specific txt file'
    )
    parser.add_argument(
        '-r', '--results-path',
        metavar='RESULTS_PATH',
        default=RESULTS_PATH,
        help='path to directory where resulting xml files will be stored'
    )
    parser.add_argument(
        '-d', '--force-dialect',
        type=dialect_arg,
        metavar='DIALECT',
        default=FORCE_DIALECT,
        help='force usage of a specific epub source dialect, skipping the auto-detection'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='wether to display low-level debugging messages'
    )
    parser.add_argument(
        '--only-probe-dialect',
        action='store_true',
        help='if used, only check which dialects would be used'
    )
    args = parser.parse_args()

    loglevel = logging.DEBUG if args.verbose else logging.WARNING
    logging.basicConfig(format='%(asctime)s -- %(message)s', datefmt='%Y-%m-%d %I:%M:%S', level=loglevel)
    logging.debug('running with the following options')
    logging.debug(args)
    main(args)