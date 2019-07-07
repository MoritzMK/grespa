# GRESPA Scraper

The spiders can be run locally in the shell or with the webapp. The following part describes the
local installation and configuration necessary to run the scrapy spiders.

## Dependencies

Installation details are provided by the readme located in the projects root directory.
Just install conda and the grespa-appointment environment.

### Run Spider from shell

To run the spiders locally, issue the crawl command from the scrapy project directory (so, where the `scrapy.cfg` is).
You can list available spiders and run them. As before, we export the env variables before running the actual command.

To pass parameters to the spider use the `-a` flag. Example for the author_details spider:
`scrapy crawl author_details -L INFO -a author_id="No2ot2YAAAAJ" -o details.json -t json`
This command passes also the output to a json file and sets the logging level to INFO.
