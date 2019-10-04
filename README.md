# Urban Dict Bot

A twitter bot written as an integration to [Urban Dictionary](https://www.urbandictionary.com/) 
allowing fun workflow around various "urban" meanings of a given word in a presentable way.


- [Motivation](#motivation)
- [Features](#features)
- [Installation](#installation)
    - [Pre-Requisites](#pre-requisites)
    - [System Setup](#system-setup)
    - [Application Setup](#application-setup)
- [Getting Started](#getting-started)
    - [Following](#following)
    - [Mentions](#mentions)
    - [Status Update](#status-update)
- [Usage](#usage)
    - [Advanced API](#advanced-api)
- [Applications](#applications)
- [Why?](#why)
    

## Motivation

- Create funny threads on twitter where a bot can pop-up and 
reply to obscure words with a completely out-of-context meaning.

- Idea majorly inspired after reading 
Donald Trump's "Covfefe" tweet.

- Bot can "follow" certain people and make a visual tweet 
of one of the obscure words in their tweet or be tagged by a user to reply a meaning to a word.

![](https://github.com/SlapBot/urban-dict-bot/blob/master/screenshots/0.gif)


## Features

- Replies a definition to a term by rendering the Urban Dictionary UI in phantomJS and posting the screenshot because IT LOOKS COOL.
- The screenshot contains the Meaning, Example, Tags and Author (This couldn't have been done with twitter's character limit)
- Logs all replies in an effective manner to keep track of bot's activity as well as to avoid posting duplicate messages.
- Follows certain users and makes an image reply of one of their obscure words in the tweet.
- Listens to its tags and replies the meanings of the word requested by user in the thread.
- Updates a status as a meaning to a key thats trending on Urban Dictionary for that moment.


## Installation

### Pre-requisites

1. Python3
2. pip
3. virtualenv

### System Setup

1. Run: `sudo apt-get update`
2. Install libfontconfig: `sudo apt-get install libfontconfig`
3. Create a twitter bot at: `https://developer.twitter.com/en/apps/`
4. Fill in credentials at: `config.ini` file.
    - Leave the `follow_ids` and `status_title` for now.


### Application Setup

1. Clone the repo: `git clone https://github.com/slapbot/urban-dict-bot`
2. Cd into the directory: `cd urban-dict-bot`
3. Create a virtualenv for python: `virtualenv urban-dict-bot-env`
4. Activate the virtualenv:
    - Linux: `source urban-dict-bot-env/bin/activate`
    - Windows: `sources urban-dict-bot-env/Scripts/activate` (You need to download a different binary of phantomJS)
5. Upgrade your pip to latest version: pip install --upgrade pip
6. Install the application dependencies: `pip install -r requirements.txt`
7. Install the nltk packages: `python install_nltk_deps.py`
8. Give executing permissions to phantomJS: `chmod +x phantomjs-2.1.1-linux-x86_64/bin/phantomjs`


## Getting Started

### Following

Add in the configuration of bot at `config.ini` file:
```
# Write the ids of people your bot wants to follow separated by a comma.
follow_ids=396469661,790080344,386788466,204832963,25073877,75821706,1339835893,44196397
# In order to find follow_id of your user -> Try this: https://tweeterid.com/
```

Run the worker `python track_users.py` which translates as follows:
```
from urban_dict.twitter_get import TwitterGet


tg = TwitterGet(flag="follows")
tg.stream_follow(tg.follow_ids)

```

This would start tracking the tweets of the given follow_ids and whenever it finds an obscure word tweeted by your target, 
It would reply the "urban" meaning of that word in a thread by rendering the urban dictionary web templated image.


### Mentions

![](https://github.com/SlapBot/urban-dict-bot/blob/master/screenshots/2.gif)

Run the worker `python track_mentions.py` which translates as follows:
```
from urban_dict.twitter_get import TwitterGet


tg = TwitterGet(flag="mentions")
tg.stream_track(tg.handle)

```

This would start listening to any mention with the format, `@bot-handle define Nihilism` or @bot-handle Nihilism`. 
A reply will be made explaining the meaning of term "Nihilism" by rendering the urban dictionary web templated image.

### Status Update

![](https://github.com/SlapBot/urban-dict-bot/blob/master/screenshots/1.gif)

Add in the configuration of bot at `config.ini` file:
```
# Write the message bot will post with the meaning.
status_title=Word Of The Day
```

Run the worker `python status_update.py` which translates as follows:
```
from urban_dict.status_updater import StatusUpdater


su = StatusUpdater()
su.make_status()

```

This command will find the trending words at Urban Dictionary and 
choose one of them to post the definition of the term as screenshot rendered by phantomJS so it looks kinda nice.

## Usage

The API is super straightforward and intuitive to understand and consume, 
taking a look at the `urban_dict` should give you a rough understanding of its functioning.

### Advanced API

- `urban_dict/workflow.py`: Managing the workflow around stream workers:
    - `mentions`: This method allows you to reply back to the tags, 
    `parse_mention_term` method suggests the boolean logic of how a word gets selected to defined.
    - `follows`: This method allows you to reply to the users you are following.
    - Both of these methods and majorly the class `Workflow` should give you everything you require to create your different 
    version of the bot.
- `urban_dict/twitter_get.py`: Managing the streams API from twitter and feeding it to the Workflow class:
    - `stream_follow`: Method allows you to follow certain user_ids activity and respond appropriately
    - `stream_track`: Method allows you to track certain keywords (in our case we are tracking our own bot's username)
- `status_updater.py`: Simple class used to scrape and render Urban Dictionary trending words to be posted to Twitter via their API.
- `utils/`: Contains small utility classes to manage configuration and logging of the events in the project.
- `core/`: Heart of the project with dedicated classes dealing with different aspects of the project.

## Applications

- Follow celebrities and make witty remarks to their obscure tweets.
- Hate your colleague making annoying ranting tweets with no context involved? Give him a taste of his own medicine
- Someone being ignorant about modern interpretation of a given word? Tag the bot to the meaning in the thread.
- Its fun.

## Why?

Okay - this is a tricky one, its again an old project of mine where I had an idea to post sarcastic remarks via Urban Dict, 
So I created this bot long time ago. It was only after I built that I realized it wasn't the brightest idea to build.

But here we are - I am on a marathon of uploading my old projects to open-source.
