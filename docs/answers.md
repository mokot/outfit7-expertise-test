# Questions and Answers

## Table of Contents

- [Question1](#question1)
- [Question2](#question2)
- [Question3](#question3)

---

### Answer to sub-question of Problem 2:

> With a "sanity check", we found that the SuperNetwork report for September 16,
> 2017 was meaningless. We came to this conclusion by checking the name of the
> data columns, the correctness of the type of all data, the date format, the
> name of the application and the platform, and the meaning of the number of
> requests and impressions. For the latter, we found that it is meaningless for
> the My Talking Ben application, since the number of impressions cannot be
> greater than the number of requests, which consequently means that the report
> for the given day and the given application is meaningless and needs to be
> corrected or removed.

---

### What do you think could also go wrong, besides the examples above? And what kind of “sanity checks” would you implement to prevent the importing of “bad” reports? <span id="question1"></span>

---

> There are many things that could go wrong, for example the data could be
> mixed up according to the column name, which should be fixed, the columns
> could just be wrongly named or placed in a meaningful order. Also, the date
> could be in the wrong format, but it would still be the date and consistent
> for the entire file. The names of applications and platforms could be invalid
> or non-existent, which means that the entries of such data should be ignored.
> With the number of requests and impressions, in addition to the above
> problem, we must pay attention to the fact that the data is numerical. As for
> the last revenue column, we must pay attention to know in which currency the
> revenue is entered and only then convert it into a single currency that is
> stored in the database. I would prevent the entry of incorrect or bad reports
> by implementing security mechanisms that would recognize the above problems
> and deal with them accordingly. The only solution to some problems is to
> delete the inappropriate entry, which will unfortunately result in losing the
> data (or requesting it from the provider again). However, where it would be
> possible, for example a case where the number of impressions is inadequate,
> I would try to make an ML model that would be able to predict the number in
> the event of a wrong entry, thus retaining the data, but at the cost of
> actual accuracy.

### Apps7 would now like to retrieve many kinds of data from 30+ different adNetworks. Their APIs can fail unexpectedly, data can be incomplete and need to be reimported later, etc… How would you design a system so all these unexpected situations could be managed with minimal overhead? What kind of (existing) technologies would you use? <span id="question2"></span>

---

> I would try to make a system that would handle most of the possible
> unpredictable events in the simplest and most transparent way, and if there
> were any errors, the data could be easily updated and corrected. For data
> processing (data transformation) I would choose [Apache Spark](https://spark.apache.org/),
> because of its parallel processing capabilities. For building straightforward
> and modular data pipelines, I would choose [Apache Airflow](https://airflow.apache.org/).
> I would use [Apache Kafka](https://kafka.apache.org/) for data collection and
> transportation. For storing the data and using computing and cloning features,
> I would use [Snowflake](https://www.snowflake.com/) or [Amazon Redshift](https://aws.amazon.com/redshift/)
> as a cloud-based data warehouse. For data visualization, I would use [Tableau](https://www.tableau.com/).

### Which [Google Cloud Platform](https://cloud.google.com/products/) products would you choose and how would you use them to build your application? <span id="question3"></span>

---

> I would choose the following Google Cloud Platform products:
>
> - [BigQuery](https://cloud.google.com/bigquery): I would use the product for
>   storing and working with data, writing direct SQL queries, and interactive
>   data analysis.
> - [Dataprep](https://cloud.google.com/dataprep): I would use the product to
>   research, clean, and prepare structured and unstructured data.
> - [Data Fusion](https://cloud.google.com/data-fusion): I would use the
>   product to create and maintain data pipelines, as well as use their visual
>   user interface for easier deployment of ETL/ELT pipelines.
> - [Looker](https://cloud.google.com/looker): I would use the product for
>   visualizing data, embedded analytics, and using LookML (Looker's modeling language).
>
> I would also consider using [Data Studio](https://cloud.google.com/datastudio),
>   [Dataproc](https://cloud.google.com/dataproc), and [Dataflow](https://cloud.google.com/dataflow).
