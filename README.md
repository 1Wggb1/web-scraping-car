# Web-Scraping-Car
It´s a basic python 'web-scraping' to get content from site simulating page request from server.
**The intent of project is find out new ad´s for car in sites, but is flexible to find out another items too.**

## Features
Today there are three implementations:
- [Icarros](https://www.icarros.com.br/ache/listaanuncios.jsp);
- [webmotors](https://www.webmotors.com.br/);
- [olx](https://www.olx.com.br/).

## Code discovery
> - The file `main.py` contains examples of use;
> - The scraping result is store on folder `results/[site] (icarros/webmotors)` at root of project;
> - There are a file called `results/[site]/found_results.json` in each site folder (working like a database - storing results already found);
> - In future the impl can store data in nosql database;
> - <font color="red">The project has a github action to search ad on providers according a scheduled task<font color="red">;
> - <font color="red">It's possible to receives notification on email/telegram (currently in json format) - Here, mail/telegram bot configurations is necessary and git action too<font color="red">;
> - See actions configurations [here](/.github/workflows/actions.yml).

## Commands to configure and install required dependencies
This project uses `python 3.11+`;

### Creating a python virtual environment
- `python3 -m venv venv`

### Activating venv
- `source venv/bin/activate`

### Installing required project deps 
- `pip install -r requirements.txt`
