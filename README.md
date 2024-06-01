# Web-Scraping-Car
It´s a basic python web-scraping using [requests](https://requests.readthedocs.io/en/latest/) to get content from page (html) and 
[beautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to filter and get html elements easily. 
The main objective is find latest cars ads in sites. There are two implementations
one to find in the site [Icarros](https://www.icarros.com.br/ache/listaanuncios.jsp) and another to find in [webmotors](https://www.webmotors.com.br/).

> - The file `src/main.py` contains examples of use;
> - The scraping result is store on folder `results/[site] (icarros/webmotors)` at root of project;
> - There are a file called `results/[site]/found_results.json` in each site folder. 
> This file stores results already found 
> to facilitate find new ads (future impl can store data in nosql database);
> - Icarros impl stores an additional file (html - with searched cars images) beyond found_results.

## Commands to install required dependencies

- This project uses `python 3.11`.
- `pip install -r requirements.txt`