To run application on your local machine:
1) Create ./PKparser/config.ini file with following contents
    ```Git config
   [Telegram]
    api_id = <telegram api id>
    api_hash = <telegram api hash>
    username = bot
    channel_url = https://t.me/<channel name>
   ```
2) Run
   ```
   docker compose build --no-cache
   docker compose run tg_scraper
   ```
   from the root directory
3) Enter phone number for your telegram account and access code, when asked.
Bot token would not suffice!