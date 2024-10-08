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


# Onsite

## Change log format
Title - date and/or version when rendering in UI. Leverage greptile to fetch version from packaging.

## References
Release notes or other related links in change logs

## Search
By features, versions, time, natural language. Change logs can be stored as vector embeddings for retrieval based on queries.

## Peristence
Archive older logs, most times the recent change logs will be referred or more relevant, so the older ones can be archived and loaded only when searched for. 
The logs itself can be json as we discussed, better than txt when storing more than one fields for each change log, like content, feature tags, date, version etc.

## Labels
The feature tags or labels creation is an intersting problem in itself that came up during our discussion. Multiple ways to approach it, we can maintain a hashmap of keyword to it's synonyms and go from there.

