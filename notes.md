- seperate what's new from what's fixed
- it's for customers
- version number

Example---
Having support search by tags
List

## Version 1.0012

Intro in 1-2 sentences

`date` 

`tag1`, `tag2`,...`tag3`.

### What's new?

### Fixes




# CLI Design

input -> repo, timeframe, (ideally persisted date of last release), tags (optional)

process -> github QL to grab changes, greptile to generate changelog

output -> in command line for now


# Further ideas
There's scope to refactor and have all rest apis separated on the flask server in app.py. Having CLI to trigger change log compilation.
Explore github APIs to get the diff directly over the time period instead of for each commit. 
Further improvements to prompt passed to greptile.