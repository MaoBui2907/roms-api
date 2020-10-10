# Emulator roms browser

## Structure

- crawler: scrapy spider crawl from romsmodes.com
- server: api server serve client
- client
  - computer: GUI linux app with tkinter

## Crawler:

- require python>=3, scrapy, azure-cosmos, toml
- store cosmos database config in */crawler/tom/db.toml* with keys: **ACCOUNT_URI**, **ACCOUNT_KEY**

## Server:

- require python>=3, flask, toml, azure-cosmos
- store cosmos database config in */server/db.toml* with keys: **ACCOUNT_URI**, **ACCOUNT_KEY**

## Client:

### Computer:

- require python>=3, tkinter, pillow, requests
