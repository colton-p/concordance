# Concordance data prep

```
make taylor
```
runs the following steps:
- extract lyrics
- clean text: normalize whitespace, remove verse/chorus markers
- tokenize: with spacy library
- concord: group by words, with list of usages 

Output to `data/conc` suitable for use in concordance (client)[https://github.com/colton-p/concordance/client].