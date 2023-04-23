# Echolalia Persian Poems Dataset
## Overview
The Echolalia Persian Poems Dataset is a collection of nearly 2000 poems from around the world translated in Persian. This dataset has been scraped from [Echolalia](https://echolalia.ir) using Python programming language.

## Files
* `scrape.py`: This file contains the code used for scraping [Echolalia](https://echolalia.ir) to extract the poems' data.
* `echolalia.txt`: This file contains the collected data in JSON format.
* `links.txt`: This file contains the links to the poets' pages in JSON format.

## Data Format
Each line of the `echolalia.txt` file represents a JSON object containing the following fields:

* title: Title of the poem.
* link: Link to the poem's webpage on echolalia.com.
* poem: The content of the poem.
* poet_nationality: The nationality of the poet.
* poet_name: The name of the poet.
* poet_link: The link to the poet's webpage on [Echolalia](https://echolalia.ir).


Each line of the `links.txt` file represents a JSON object containing the following fields:

* poet_nationality: The nationality of the poet.
* poet_name: The name of the poet.
* poet_link: The link to the poet's webpage on [Echolalia](https://echolalia.ir).

## Basic Preprocessing Steps
The following preprocessing steps have been applied to the data:

* Removal of URLs
* Removal of hashtags
* Removal of HTML tags
* Removal of footnotes starting with "پانویس ها"
* Removal of extra information starting with "توضیحات بخش"

*Note that the dataset needs further preprocessing.*

## Acknowledgments
The data has been collected from [Echolalia](https://echolalia.ir). Special thanks to the website for providing access to the data.
