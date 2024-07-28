
[![](https://dcbadge.limes.pink/api/server/https://discord.gg/7f7GVAKfFf)](https://discord.gg/7f7GVAKfFf)

![PyPI - Version](https://img.shields.io/pypi/v/discord.py?style=for-the-badge)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/discord.py?style=for-the-badge&color=%23e3a93d)




# Biometric Machine

A Discord bot designed for the [**KIIT HIVE**](https://discord.gg/7f7GVAKfFf) server. It streamlines member verification by authenticating users through their KIIT University email addresses. The bot requests the user's KIIT email, sends a One-Time Password (OTP), verifies the user upon correct OTP entry, and automatically assigns roles based on the user's roll number. This process ensures a secure environment exclusive to verified KIIT University community members.


## Features

- Email OTP Verification
- Automatic Role Based on Roll Number


## Roadmap

- Adding database to store already verified emails.
- Add blacklist command to ban a email.


## Contributing

Contributions are always welcome! They can be anything like - 
- Code Optimization
- New/Better Feature Implementation
- Bug fixing
- Documentation Update

## Run Locally

Clone the project

```bash
  git clone https://github.com/arthishaxom/biometric-machine
```

Go to the project directory

```bash
  cd biometric-machine
```

Install dependencies (Better if you use a [virtual environment](https://www.youtube.com/watch?v=Y21OR1OPC9A&t=144s))

```bash
  pip install -r requirements.txt
```

Create a file `config.py` & put your tokens and api_keys accordingly
- you can use [resend](https://resend.com/emails) for testing as brevo requires you to get a domain
- replace the relevant code in [funcs.py](utils/funcs.py)
```bash
  DISCORD_TOKEN = "your_token"
  BREVO_KEY = "brevo_api_key" 
  GUILD_ID = testing_guild_id
```

Start the bot
```bash
py main.py
```

## Acknowledgements
- [itsabhinavism](https://github.com/itsabhinavism) - Helped in ideation of Bot 