### Scrapper

_How to execute scrapper ?_
```shell
  pip install scrapy bs4
```
```shell
  scrapy runspider ./scrapper/physics_scrapper.py -o content.csv -t csv
```

_To process scrapped content run the following script_
```shell
    python ./text_processing/processor.py
```