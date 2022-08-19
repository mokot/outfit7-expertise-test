# Instructions

## Table of Contents

- [Problem1](#problem-1-collecting-data-in-containers)
- [Problem2](#problem-2-analysing-data)
- [Problem3](#problem-3-reliable-design)

## Problem 1: Collecting data in containers

You are working for a company called Apps7 that makes mobile games. These games display ads from a few major adNetworks. Because we are interested in ad performance, each adNetwork provides us with daily reports which come in the form of CSV files. Each report contains the following data: app id, platform (iOS, Android), amount of revenue, number of requests and impressions.
We want to store all data reported by adNetworks in a uniform way so that Apps7 can later use it for various analytical purposes.

Apps7 has contacted you to help them develop such an application.

### A short glossary

- AdNetwork - [Advertising Network](https://en.wikipedia.org/wiki/Advertising_network)
- Request - Counted whenever an app requests an ad to be displayed. [More](https://medium.com/knowledgebase/what-is-request-impression-fill-rate-ctr-and-ecpm-c3d7db01e021).
- Impression - Counted whenever an ad is actually displayed in an app. [More](https://medium.com/knowledgebase/what-is-request-impression-fill-rate-ctr-and-ecpm-c3d7db01e021).

### Application requirements

Please submit your application all related scripts and files included. The application should take adNetwork and date as input parameters. It should then retrieve each report for these input parameters from the URLs provided below and store it in a database. All retrieved reports should be saved to the same table called “daily_report”.

For this test we have prepared some dummy reports for two sample adNetworks: “SuperNetwork” and “AdUmbrella” and the following dates: 2017-09-15 and 2017-09-16. When designing your solution, keep in mind that any (past) date is valid and that many more adNetwork reports might be implemented later.

Available adNetwork report details:

- SuperNetwork ([2017-09-15](https://storage.googleapis.com/expertise-test/supernetwork/report/daily/2017-09-15.csv), [2017-09-16](https://storage.googleapis.com/expertise-test/supernetwork/report/daily/2017-09-16.csv))
- AdUmbrella ([2017-09-15](https://storage.googleapis.com/expertise-test/reporting/adumbrella/adumbrella-15_9_2017.csv), [2017-09-16](https://storage.googleapis.com/expertise-test/reporting/adumbrella/adumbrella-16_9_2017.csv))

### Technical requirements:

1. Use Java or Python to develop your solution.
2. Feel free to use any external library of your choice (e.g. persistence library).
3. Please send us either a zip archive with all the source code or a link to the project on GitHub or Bitbucket.
4. Make sure that your solution is production ready, so apply all the techniques that you would when writing code in a real-life situation (or at least write what would you do differently).
5. Solution should be containerized (Docker).
6. Please provide a Readme file which describes how to build and use your application.
7. If something is not clear, you are free to make some assumptions. In that case, make sure they are documented in the Readme file. It should also contain any extra information or explanation that you think might be useful to anybody reading about your solution.

## Problem 2: Analysing data

A coworker from the Apps7 analytics team has told you that one of the dummy reports above doesn’t look OK. Unfortunately, he forgot to say which one. Do a “sanity check” on the collected data and write an answer giving a short description of how you figured out which report is not OK.

What do you think could also go wrong, besides the examples above? And what kind of “sanity checks” would you implement to prevent the importing of “bad” reports?

## Problem 3: Reliable design

1. Apps7 would now like to retrieve many kinds of data from 30+ different adNetworks. Their APIs can fail unexpectedly, data can be incomplete and need to be reimported later, etc… How would you design a system so all these unexpected situations could be managed with minimal overhead? What kind of (existing) technologies would you use?
2. Which [Google Cloud Platform](https://cloud.google.com/products/) products would you choose and how would you use them to build your application?

In your project files please include an **answers.txt** file with short answers to Problems 2 and 3. Keep in mind that there are no right or wrong answers!
