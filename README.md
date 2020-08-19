# Discord Bot

A simple bot for discord which can perform the following things

1. Reply **hey** to your **hi**.
2. Return you top 5 links for any query using Google search
3. Return you the perviously searched keywords matching to a given value

This uses [asyncio](https://docs.python.org/3/library/asyncio.html) library hence only support python 3.5+ 

## Command Usage

**!google keyword**  -> return you top 5 links from Google search

**!recent key**   -> return the keywords from your past google search where  old_keyword ~= key

## Setup
Create a `.env` or setup environment following environment varibales

1. DISCORD_TOKEN
2. GOOGLE_SEARCH_ENGINE_KEY
3. GOOGLE_API_KEY

To get `GOOGLE_SEARCH_ENGINE_KEY` and `GOOGLE_API_KEY` checkout the [Custom Search JSON API](https://developers.google.com/custom-search/v1/overview)

To create application and setup bot on discord follow this [guide](https://discordpy.readthedocs.io/en/latest/discord.html) 

```bash
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

## Start Bot
```bash
(env)$ python main.py
```
