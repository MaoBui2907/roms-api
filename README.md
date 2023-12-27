# Emulator roms browser

## Structure

- crawler: scrapy spider crawl from ~~romsmodes.com~~ (2023 status is offline) romsgames.net
- server: api server serve client
- client
  - computer: GUI app with tkinter
- CosmosDB from Microsoft Azure:
  - `/roms`
  - `/regions`
  - `/categories`

## Crawler:

- require python>=3, scrapy, azure-cosmos, toml
- store cosmos database config `.env` with template as `.env.template`

## Server:

- require python>=3, flask, toml, azure-cosmos
- store cosmos database config `.env` with template as `.env.template`

## Client:

### Computer - Linux or Windows:
- Run binary execution file or
- Build from source that require python>=3, tkinter, pillow, requests

