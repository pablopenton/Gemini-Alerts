# Gemini API Alerts
A CLI tool aimed at obtaining the price, percentage, and volume deviation for Gemini-traded currencies.


## Setup Instructions

This repo assumes the use of pipenv for Python virtual environment setup and includes a Pipfile and Pipfile.lock, but can also be setup with other tools (e.g., poetry) using the included requirements.txt file.

The CLI tool supports specifying a specific currency or none at all. If none are supplied, then it attempts to capture data for all Gemini-traded currencies. This tool seems to be most reliable with btcusd.

CLI arguments match as described in submission example.

```buildoutcfg
python gem_alerts.py -c btcusd -t pricechange -d 1
```

## Requirements

 - Python 3 (this was developed in 3.8)
 - Requests

## Considerations for Further Improvements

The Gemini sandbox API often returned no historical data for certain currencies, especially for volume data. These situations and exception handling in general could be implemented much more competently and in a DRYer fashion.

Other considerations include:

 - Refactoring GeminiAPI object wrapper to use URI mapping rather than dedicated methods for each URI
 - Better handling of user input for nonexistent currencies, typos, etc.
 - Unittests for accuracy of math/conclusions provided by functions.

## General Approach

An CLI args handler function was implemented in an attempt to handle the different possible scenarios. A dedicated function was then created to handle each of the three main functions of the CLI tool (price deviation, percentage deviation, volume deviation). An object wrapper was then created to facilitate interacting with the Gemini REST API.

### Time Completed
~ 4 hours
