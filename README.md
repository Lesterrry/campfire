# 🔥 Campfire
![Platform](https://img.shields.io/badge/platform-Unix-gray)
## What is it
Campfire monitors the internet and informs you about any changes
## How to use
1. Clone the repo
2. Modify `config.yaml`
3. Modify `index.yaml` (see [Index file syntax](#index-file-syntax))
## Index file syntax
I'm too lazy to explain everything thoroughly, so just examine the file and scripts if you like\
__Ceremonies:__
1. `code-check`: watching for http status code to change\
    Props:
    - `url` – site url
2. `class-check`: watching for html class' property to change\
    Props:
    - `url` – site url
    - `status_class` – html class to watch
3. `lookup`: watching if a specific key exists within the website text\
    Props:
    - `url` – site url
    - `key` – needle to look for
4. `osa-lookup` (experimental): looking for keys using AppleScript\
    Props:
    - `url` – site url
    - `soldout_key` – text which says the item is gone
    - `in_stoke_key` – text which says the item is there
