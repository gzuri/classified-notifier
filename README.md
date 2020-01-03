# CRO Classfied crawler

Python script to notify you on Slack with new classifieds on [Njuskalo](https://www.njuskalo.hr/) and [Oglasnik](https://www.oglasnik.hr/)

## Configuration

1. Make sure you have python3 installed
2. Rename config.py.template to config.py
3. Configure your search links in the config.py
    - to get a search link go to the classified site, enter search parameters, copy the URL of the search page

## Usage

```bash
python3 app.py --db ./classified.db
```