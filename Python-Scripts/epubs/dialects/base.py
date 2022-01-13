from datetime import date
from itertools import takewhile
from pathlib import Path
import re

import lxml.etree as ET
from lxml.etree import QName


class EpubBaseDialect:
    '''
    Base class for all epub source dialects. Inherit from this and overwrite
    some of its methods to create your own dialects.
    '''

    NAMESPACES = {
        'tei': 'http://www.tei-c.org/ns/1.0',
        'xml': 'http://www.w3.org/XML/1998/namespace',
    }

    def transform(self, text, filename):
        '''Convert a text to TEI XML.
        
        This is probably the only method that should ever get called by an end user.
        To modify the transformation process, create a new Epub Dialect by
        subclassing this class and overriding one or more of its other methods.
        '''
        text = self.clean_up(text)
        name = filename.removesuffix('.txt')
        xml = self.build_header_xml(file_name=name)
        tei = xml.getroot()
        
        titlepage, rest = self.split_titlepage(text)

        # Create the various parts of the <text>.
        front = self.build_titlepage_xml(titlepage)
        body, fns = self.build_body_xml(rest)
        back = self.build_back_xml(fns)
        
        text_node = ET.Element('text')
        text_node.append(front)
        text_node.append(body)
        text_node.append(back)

        tei.append(text_node)

        tree = ET.ElementTree(tei)
        return tree


    def build_back_xml(self, footnotes):
        '''Create notes in a back section at the end of the document.
    
        If there are no footnotes, create an empty <back>.
        '''
        nsmap = self.__class__.NAMESPACES
        back = ET.Element('back', nsmap=nsmap)
    
        def _create_elem(key, value):
            elem = ET.Element('note')
            elem.attrib[QName(nsmap.get('xml'), 'id')] = f'N{key}'
            elem.text = value
            elem = self.insert_italics_xml(elem)
            return elem
        
        if footnotes != {}:
            fns = [_create_elem(k, v) for k, v in footnotes.items()]
            notes = ET.SubElement(back, 'div', attrib={'type': 'notes'})
            notes.extend(fns)
        
        return back


    def build_titlepage_xml(self, text):
        '''Wrap the elements of the titlepage in appropriate XML elements.'''
        front = ET.Element('front')
        titlepage = ET.Element('div', attrib={'type': 'titlepage'})
        
        # Wrap lines in either head or paragraph tags.
        for line in text.split('\n'):
            line = line.strip()
            if line and line.startswith('#'):
                h = ET.Element('head')
                h.text = line.replace('#', '').strip()
                titlepage.append(h)
            elif line:
                p = ET.Element('p')
                p.text = line.strip()
                titlepage.append(p)
        front.append(titlepage)
        return front


    def build_body_xml(self, text):
        '''Wrap elements of the text body in appropriate XML elements.'''
        chapters = self.split_chapters(text)
        body = ET.Element('body')
        footnotes = {}

        for chapter in chapters:
            xml, footnotes = self.build_chapter_xml(chapter, footnotes)
            body.append(xml)
    
        return body, footnotes


    def build_chapter_xml(self, chapter, footnotes):
        '''Given the text of one chapter, create the appropriate XML markup.'''
        offset = max(footnotes.keys()) if footnotes != {} else 0
        text, notes = self.parse_footnotes(chapter, offset)
        footnotes.update(notes)

        markup = ET.Element('div', attrib={'type': 'chapter'})
        
        for line in text.split('\n'):
            if line.startswith('#'):            
                node = ET.SubElement(markup, 'head')
                node.text = line.replace('#', '').strip()
            elif line:
                node = ET.SubElement(markup, 'p')
                node.text = line.strip()
            
            # Insert additional markup inside the new node.
            node = self.insert_fn_markers_xml(node)
            node = self.insert_italics_xml(node)

        return markup, footnotes


    def build_header_xml(self, root=None, metadata={}, file_name=''):
        '''Build an xml tree from a text template.'''
        nsmap = self.__class__.NAMESPACES
        templ_path = Path(__file__).resolve()
        templ_path = templ_path.parent / '..' / 'templates' / 'teiHeader-Template.xml'
        print(templ_path)
        parser = ET.XMLParser(remove_blank_text=True)
        xml = ET.parse(str(templ_path), parser)

        # Pre-fill some known values.
        today = date.today().isoformat()
        xml_id = file_name or 'TODO'
        tei = xml.getroot()
        tei.attrib[QName(nsmap.get('xml'), 'id')] = xml_id
        #print(ET.tostring(tei))
        change_path = f"//{ET.QName(nsmap.get('tei'), 'revisionDesc')}/{ET.QName(nsmap.get('tei'), 'change')}"
        change = xml.find(change_path)
        change.attrib['when'] = today

        if metadata != {}:
            raise NotImplementedError('Auto-fill-in of metadata is not yet supported – sorry!')

        if root is not None:
            root.insert(0, xml)
            return root
        return xml


    def clean_up(self, text):
        '''Delete and/or replace unnecessary text artifacts.'''
        text = (
            text.replace('&', '&amp;')
                .replace('\!', '')
                .replace('\*', '*')
                .replace('* * *', '')
                .replace('\(', '(')
                .replace('\)', ')')
        )
        
        # Delete empty lines.
        lines = [line for line in text.split('\n') if line.strip()]
        # Delete all lines after '# ****À propos de cette édition électronique'
        lines = takewhile(lambda l: not l.startswith('# ****À propos de cette édition électronique'), lines)

        text = '\n'.join(lines)
        return text


    def insert_fn_markers_xml(self, node):
        '''Update paragraph with <ref> nodes for the footnote markers.
        
        This relies on the numerical markers being correct, i.e. if footnotes are
        numbered for each chapter individually, they should have been corrected
        with `parse_footnotes()` beforehand.
        '''
        mark_pattern = r'\\\[(\d+)\\\]'
        segments = re.split(mark_pattern, node.text or '')
        tail_segments = re.split(mark_pattern, node.tail or '')

        # Check if there are actually footnote markers in this node's text.
        if len(segments) > 1:
            last_node = node
            i = 0
            while i < len(segments):
                segment = segments[i]
                # Case 1: Text at the start of the node. This is stored in the `text` property
                #         of the node itself.
                if not segment.isnumeric() and i == 0:
                    node.text = segment
                # Case 2: Regular text after at least one `ref` has been created.
                #         This should be the `tail` of the previously created `ref` node.
                elif not segment.isnumeric():
                    last_node.tail = segment
                # Case 3: Marker segment. This is stored as a `ref` child node without `text`. 
                #         Further text will be appended to the `tail` property of this node.
                elif segment.isnumeric():
                    number = f'#N{segment}'
                    fn_node = ET.SubElement(node, 'ref', attrib={'target': number})
                    last_node = fn_node
                i += 1

        # Check if there are footnote markers in this node's tail.
        if len(tail_segments) > 1:
            last_node = node
            i = 0
            while i < len(tail_segments):
                segment = segments[i]
                # Case 1: Normal text at the start of the tail. This should remain tail.
                if not segment.isnumeric() and i == 0:
                    node.tail = segment
                # Case 2: Normal text somewhere in the middle or at the end of tail.
                #         This should be the tail of a previously created node.
                elif not segment.isnumeric():
                    last_node.tail = segment
                # Case 3: Footnote marker. Create a new sub node of the parent (!)
                #         of the current node.
                elif segment.isnumeric():
                    number = f'#N{segment}'
                    parent = last_node.getparent()
                    fn_node = ET.SubElement(parent, 'ref', attrib={'target': number})
                    last_node = fn_node
                i += 1

        # Do the same for all child nodes of the current node.
        for child in node.getchildren():
            self.insert_fn_markers_xml(child)

        return node

    def insert_italics_xml(self, node):
        '''Given a paragraph node, insert a hi node for italics if applicable.'''
        # Non-greedy pattern (i.e. match as little as possible) for italic text segments.
        # Immediately following the first '*' there needs to be a letter or number (as opposed to
        # whitespace or punctuation), else it is a stand-alone asterisk like in "the marquis of *".
        italic = r'(\*[\w\d].*?\*)'
        segments = re.split(italic, node.text or '')
        tail_segments = re.split(italic, node.tail or '')

        # Check if there are actually italic segments in the node's text.
        if len(segments) > 1:
            # Process italics:
            last_node = node
            i = 0
            while i < len(segments):
                seg = segments[i]
                # Case 1: non-italic at the start of the paragraph. This should be
                #         in the `text` part of the paragraph.
                if not seg.startswith('*') and i == 0:
                    node.text = seg
                # Case 2: non-italic somewhere in the middle of the paragraph. This is
                #         supposed to be the `tail` of a previously created <hi> node.
                elif not seg.startswith('*'):
                    last_node.tail = seg
                # Case 3: italic text. Create a new <hi> node and set its text content.
                #         Then append it to the paragraph.
                elif seg.startswith('*'):
                    content = seg.strip('*')
                    new_node = ET.SubElement(node, 'hi', attrib={'rend': 'italic'})
                    new_node.text = content
                    last_node = new_node
                i += 1
        
        # Check if there are italic segments in the node's tail.
        if len(tail_segments) > 1:
            last_node = node
            i = 0
            while i < len(tail_segments):
                seg = tail_segments[i]
                # Case 1: non-italic at the start of the tail. This should remain
                #         in the `tail` of this node (while all the following text
                #         shouldn't).
                if not seg.startswith('*') and i == 0:
                    node.tail = seg
                # Case 2: non-italic somewhere in the middle or at the end of the
                #         tail. This should be in the `tail` of a previously created
                #         <hi> node.
                elif not seg.startswith('*'):
                    last_node.tail = seg
                # Case 3: italic text. Create a new <hi> node and set its text content.
                #         Append it to the parent (!) of the current node.
                elif seg.startswith('*'):
                    content = seg.strip('*')
                    parent = last_node.getparent()
                    new_node = ET.SubElement(parent, 'hi', attrib={'rend': 'italic'})
                    new_node.text = content
                    last_node = new_node
                i += 1
        
        # Do the same for all child nodes of the current node.
        for child in node.getchildren():
            self.insert_italics_xml(child)

        return node


    def parse_footnotes(self, text, fn_offset=0):
        '''Given a string, identify footnotes and replace their markers.
        
        Sometimes, footnotes in a document are numbered per chapter. In the final
        TEI, we put all the footnotes in a designated <back> section. So we need to
        renumber them first. The parameter `fn_offset` gives the number of footnotes
        we have already seen in previous chapters.
        '''
        mark_pattern = r'(\\\[)(\d+)(\\\])'
        markers = [m[1] for m in re.findall(mark_pattern, text)]
        notes = [re.search(f'\n{n}\.\s↑\s+(.*?)\s*\n', text).group(1) for n in markers]

        # Replace markers with updated numbering based of offset of this chapter.
        text = re.sub(
            mark_pattern,
            lambda match: f'{match.group(1)}{(int(match.group(2))+fn_offset)}{match.group(3)}',
            text)
        # Delete actual notes at the end of the chapter. They will eventually be inserted
        # in the <back> of the document.
        text = re.sub(r'\d+?\.\s↑\s+(.*?)\s*?\n', '', text)

        # Map updated markers to corresponding footnote text.
        footnotes = {int(m)+fn_offset: n for m, n in zip(markers, notes)}

        return text, footnotes


    def split_titlepage(self, text):
        '''Split on the second occurence of "### ".'''
        # How to recognize the end of the titlepage
        marker = '\n### '
        end_of_titlepage = text.find(marker, text.find(marker)+len(marker))
        # Add 1 to index so that the newline still belongs to the titlepage.
        titlepage, rest = text[:end_of_titlepage+1], text[end_of_titlepage+1:]
        return titlepage, rest


    def split_chapters(self, text):
        '''Split on occurrences of "### ".
        
        The main reason why we want to process chapters individually is that often footnotes
        are internally numbered per chapter.
        '''
        pattern = r'(###\s.+?)\s*\n'
        segments = [s for s in re.split(pattern, text) if s]

        # No chapters:
        if len(segments) == 1:
            chapters = [text]
        # Segments start with chapter heading:
        elif segments[0].startswith('### '):
            chapters = [f'{h}\n{t}\n' for h, t in zip(segments[0::2], segments[1::2])]
        # Segments start with chapter without heading:
        else:
            chapters = [segments[0]]
            chapters.extend([f'{h}\n{t}\n' for h, t in zip(segments[1::2], segments[2::2])])

        return chapters