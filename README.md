# pytest-tg-notify #

This project shows how to collect all tests results, running by pytest with pytest-xdist, and send general result via Telegram, using bot.

All you need is type your bot token and chat id into config.yaml parameters.

You can modify this project to sending information via email or other notification apps.

Modules in project:
- helpers/readers.py: yaml reader (for config.yaml);
- lib/bot.py: declare telegram bot;
- lib/config.py: config file;
- tests/test.py: file with tests examples;
- config.yaml: file for storage parameters;
- conftest.py: general pytest file with fixtures;
- requirements.txt: list of required python mudules.

Required modules:
- pytest;
- filelock;
- PyYAML;
- pytest-xdist.
