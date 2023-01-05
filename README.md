# youtube-analytics
Using youtube analytics API to gather data about web3dev youtube channel


# Setup

## Setup auth credentials
Before running it locally, we have to set up authorization credentials for the project:

1. Create or select a project in [Google API Console](https://console.cloud.google.com/)

2. Enable [Youtube Analytics API](https://console.developers.google.com/apis/library/youtubeanalytics.googleapis.com) for your project.

3. At the top of the [Credentials](https://console.developers.google.com/apis/credentials) page, select the OAuth consent screen tab. Select an Email address, enter a Product name if not already set, and click the Save button.

4. On the [Credentials](https://console.developers.google.com/apis/credentials) page, click the Create credentials button and select Oatuh client ID.

5. Select the application type Other, enter the name, and click the Create button.

6. Download the JSON (button right of the client ID)

7. Put that downloaded JSON inside the file secrets.json (as shown on secrets.json.example)

## Setup libraries

Run:

`pip install -r requirements.txt`

to install dependencies.

# Running the script

Simply run 

`python3 analytics.py`

And answer the prompts! Authenticate your account on google and you are good to go.
