# Schemas

Current versions of the ELTeC schema in RELAX NG  are available from this repository, either for download to your
local system, or directly via HTTP.

PLEASE NOTE THAT THE ELTEC-2 SCHEMA IS ENTIRELY PROVISIONAL AND HAS NOT YET BEEN TESTED

To check whether a text is valid against an ELTeC schema in oXygen, insert PIs like the following at the
start of the document:

```
    <?xml-model href="https://github.com/COST-ELTEC/Schemas/raw/master/eltec-1.rng" type="application/xml" 
            schematypens="http://relaxng.org/ns/structure/1.0"?>
    <?xml-model href="https://github.com/COST-ELTEC/Schemas/raw/master/eltec-1.rng" type="application/xml" 
            schematypens="http://purl.oclc.org/dsdl/schematron"?>
```
or, if you have downloaded this repository to a location on your system:

```
    <?xml-model href="/path/to/eltec-1.rng" type="application/xml" 
            schematypens="http://relaxng.org/ns/structure/1.0"?>
    <?xml-model href="/path/to/eltec-1.rng" type="application/xml" 
            schematypens="http://purl.oclc.org/dsdl/schematron"?>

```
The RELAXNG schema contains embedded schematron rules, which oXygen validates in a second pass

# Documentation

For complete documentation of each schema, please read
- https://distantreading.github.io/Schema/eltec-0.html (level 0)
- https://distantreading.github.io/Schema/eltec-1.html (level 1)
- https://distantreading.github.io/Schema/eltec-2.html (level 2)

A copy of this documentation is also available in this repository in the folder `Doc`

# ODD sources

The schemas and their documentation are produced by processing a TEI-conformant ODD specification, which
is also available from this repository, in the folder `ODD`. 


