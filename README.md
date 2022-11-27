### Scrapper

_How to execute scrapper ?_
```shell
  pip install scrapy bs4
```
```shell
  scrapy runspider ./scrapper/physics_scrapper_uncategorized.py -o uncategorized_corpus.csv -t csv
```
```shell
  scrapy runspider ./scrapper/physics_scrapper_categorized.py -o categorized_corpus.csv -t csv
```
_To process scrapped content run the following script_
```shell
    python ./text_processing/processor.py
```