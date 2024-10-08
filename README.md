# Change log generation

## Set up
Install dependencies - 

`pip install -r requirements.txt`

## Generate logs 
Spin up the flask server with - 

`python app.py`

Generate product change logs.

The cli generate_changelog.sh can be used to generate the change log (takes optional time-period cmdline arg as number of days).
Generate change log with default two days - 

`./generate_changelog.sh  `

or 

Generate change log with time period as 4 days - 

`./generate_changelog.sh  --time-period 4`

Change log will be generated, appended to the change_log/change_log.txt file.

## View logs
To view the change logs in UI -
Open http://127.0.0.1:3000 (the port flask server is running on) in browser.
