Title: PostgreSQL timestamps: With or without time zone?
Author: Vineet Naik
Date: 2023-12-06
Tags: postgresql
Category: programming
Summary: PostgreSQL provides the timestamp type in two variants - with time zone and without time zone. How to decide which one to use?
Status: published

I am currently building a toy project to learn Rust and VueJS. Like
most applications it needs to store data and I'm using PostgreSQL (PG)
as the database due to familiarity. When creating the db schema I had
to make a choice - should the timestamp column be with or without time
zone?

I've often run into this question and based on my superficial
understanding and the fact that both variants take up same space in
postgresql, I've always chosen `WITH TIME ZONE` and moved on. If
there's no additional cost, "with" must be better than "without",
right? But there's definitely more to it, otherwise why would the db
provide options?

Incidentally, some timestamps in my application are critical to the
business logic and not merely the usual `created_at` and `updated_at`
columns. Any processing such as time zone conversions or
adding/subtracting intervals is something I'd happily let the database
take care of, so it's important for me to have correct up front
understanding of how the two variants will behave with various
date/time functions and operators (particularly `AT TIME ZONE` and
`INTERVAL` for the above mentioned use cases).

While the official documentation does cover these topics, I found it a
bit terse at first. Things became clear to me only after actually
trying out some queries and then the docs started making sense. In
this blog post I'll try to explain the difference between the two
variants using the same queries that helped me understand it. I'll
also include some practical examples to help decide which one to use
when.

Henceforth in this post, I'll refer to the "WITH" variant as
_timestamp**z**_ and the "WITHOUT" variant as just _timestamp_. Official
docs use the same terminology.

Before diving into the queries, here's my setup:

- PostgreSQL version 16.0 running inside a linux container (using
  podman) on MacOS.

- The time zone of the podman machine, and hence the container is UTC.

- The local time zone on the host machine (MacOS) is 'Asia/Kolkata' or
  Indian standard time (IST) which is `UTC+530`.

- Finally, the `timezone` setting configured for the server is
  UTC. This is an important piece of information, we'll see why in a
  few minutes.

Let's start by running a simple query that outputs the current
timestamp. I'm using the `now` function to do this. At the time of
running the query, the local time here in India is 6:36PM

```sql
postgres=# select now();
      now
-------------------------------
 2023-11-28 13:06:48.961341+00
(1 row)
```

As you can see, the result is displayed in UTC (notice the `+00`
suffix) and that's because the value of the `timezone` setting
configured for the server is UTC. Also note that this value is time
zone aware and hence a _timestamp**z**_.

It's possible to override the `timezone` setting per session so let's
confirm the above by setting it to another time zone.

```sql
postgres=# set timezone = 'US/Pacific';
SET
postgres=# select now();
      now
-------------------------------
2023-11-28 05:17:43.352201-08
(1 row)
```

And now the result is displayed as per 'US/Pacific' time.

Internally, postgresql stores timestamp values in UTC and as per my
understanding, there's no way to configure this. The result that gets
displayed is implicitly converted from UTC (internal representation)
into a time zone which can either be configured for the server or set
(overridden) for the psql session. Henceforth, I'll refer to it as the
_client time zone_ <a id="footnote-1-ref"
href="#footnote-1"><sup>1</sup></a>.

Before proceeding further, I'll just reset the client time zone back
to UTC.

```sql
postgres=# set timezone = 'UTC';
SET
```

For the the next set of examples, we'll create a test table with 3
fields,

1. an int (to be used as an identifier),
2. a _timestamp**z**_, 
3. a _timestamp_

And then we'll insert a row with the current timestamp in both the
timestamp columns.

```sql
CREATE TABLE test (
id int,
tsz timestamp with time zone,
ts timestamp without time zone
);

INSERT INTO test VALUES (1, now(), now());
```

And now let's run a query.

```sql
postgres=# select * from test;
 id |          tsz              |            ts
----+-------------------------------+----------------------------
 1  | 2023-11-28 13:28:35.944451+00 | 2023-11-28 13:28:35.944451
(1 row)
```

As expected, `tsz` has an extra time zone component in the output
(notice the `+00`) which is missing in `ts`. For reference, the
current time in IST at the time of running the above query is 6:58PM.

One problem with inserting data using the `now` function is that the
value keeps changing, which I feel is a cognitive overhead when trying
to make sense of the results. To avoid that, let's insert another row
in the table but this time I'll explicitly specify a timestamp along
with a time zone.

```sql
postgres=# insert into test values (2, '2023-11-28 21:00+530', '2023-11-28 21:00+530');
INSERT 0 1

postgres=# select * from test where id = 2;
 id |       tsz          |         ts
----+------------------------+---------------------
  2 | 2023-11-28 15:30:00+00 | 2023-11-28 21:00:00
(1 row)
```

Note that the exact same value `2023-11-28 21:00+530` was inserted
(along with the time zone) in the two columns. But in the output,
`tsz` is interpreted in UTC (again because of configured `timezone`
setting) whereas `ts` is returned as it is.

This is what's happening:

1. At the time of insertion, `tsz` being a _timestamp**z**_ is aware
   of the specified time zone offset `+530` (IST). Before storing the
   value, it gets internally converted to UTC.

2. But `ts`, being just a _timestamp_, the time zone offset is
   disregarded while storing it.

3. At the time of interpreting the result of the select query, `tsz`
   gets converted to client time zone of UTC. But `ts` is returned as
   it is.

As you can see, in case of `tsz` the result that we get is very much
affected by the implicit conversion from the input time zone to the
client time zone. What if we do the conversion explicitly?


```sql
postgres=# SELECT
postgres-# tsz AT TIME ZONE 'Asia/Kolkata' as tsz,
postgres-# ts AT TIME ZONE 'Asia/Kolkata' as ts
postgres-# FROM
postgres-# test
postgres-# WHERE
postgres-# id = 2;
     tsz         |           ts
---------------------+------------------------
 2023-11-28 21:00:00 | 2023-11-28 15:30:00+00
(1 row)
```

Wow! What's going on here?

1. `tsz` was converted to 'Asia/Kolkata' time zone. This makes
   sense. It's the same value we had inserted.

2. `ts` was converted to UTC which may come as a surprise.

3. And in case you missed it - the value of `tsz` is a _timestamp_
   whereas the value of `ts` is a _timestamp**z**_!

Before drawing any conclusions, let's try converting to some other
time zone, say 'US/Pacific':

```sql
postgres=# SELECT
postgres-# tsz at time zone 'US/Pacific' as tsz,
postgres-# ts at time zone 'US/Pacific' as ts
postgres-# FROM
postgres-# test
postgres-# WHERE
postgres-# id = 2;
     tsz         |           ts
---------------------+------------------------
 2023-11-28 07:30:00 | 2023-11-29 05:00:00+00
(1 row)
```

The above observations still check out. This is what's going on:

When the `AT TIME ZONE` operator is applied to a _timestamp**z**_, it
converts the stored value in UTC to the specified time zone and
returns a _timestamp_.

When the `AT TIME ZONE` operator is applied to a _timestamp_, it
assumes the stored value in the specified time zone (Asia/Kolkata or
US/Pacific in the above queries) and converts it into the client time
zone i.e. UTC. The result is a _timestamp**z**_.

In other words, `AT TIME ZONE` adds time zone to a _timestamp_ value
that lacks it. Whereas, it shifts time zone of a time zone aware
_timestamp**z**_ value to the specified time zone and returns a value
without a time zone.

The above explanation is not much different from the one in the
[official
docs](https://www.postgresql.org/docs/current/functions-datetime.html#FUNCTIONS-DATETIME-ZONECONVERT),
although it's much easier to understand by actually trying out these
queries.

Let's see what happens if we apply the `AT TIME ZONE` operator twice.

```sql
postgres=# SELECT
postgres-# tsz AS tsz_orig,
postgres-# tsz AT TIME ZONE 'US/Pacific' AS tsz_once,
postgres-# (tsz AT TIME ZONE 'US/Pacific') AT TIME ZONE 'US/Pacific' AS tsz_twice
postgres-# FROM
postgres-# test
postgres-# WHERE
postgres-# id = 2;
    tsz_orig        |      tsz_once       |        tsz_twice
------------------------+---------------------+------------------------
 2023-11-28 15:30:00+00 | 2023-11-28 07:30:00 | 2023-11-28 15:30:00+00
```

As you can see, `tsz_twice` is exactly equal to `tsz_orig`. This means
`AT TIME ZONE` applied for the second time cancels out the effect of
applying it once, in terms of both, adding the offset as well as
converting the data type. If you try the same query with `ts`, you'll
find that it behaves similarly.

Before proceeding to the next section on deciding which one to use
when, one important observation about explicit v/s implicit time zone
conversions:

- When we convert time zone explicitly using `AT TIME ZONE`, the
   value and type of both variants are affected (_timestamp**z**_ gets
   converted to timestamp and vice versa).

- On the other hand, implicit conversion to client time zone affects
  only _timestamp**z**_ values. Moreover only the value changes (offset
  gets added) but the type stays the same (_timestamp**z**_ remains
  _timestamp**z**_).

Take away: If you want time zone conversion in the result, always do
so explicitly using `AT TIME ZONE`, even if the target time zone
happens to be the same as client time zone.

### When should you use timestampz?

In case of _timestamp**z**_, the db takes into account the specified time
zone and converts it into UTC at the time of insertion. Hence, it's
suitable in places where we want to capture an exact instant in
time. Regardless of the time zone of the user/client/app, it will
always be stored in UTC and at the time of reading we have a choice to
convert it into the required time zone.

The `created_at` and `updated_at` columns are a good example of where
_timestamp**z**_ is suitable. Imagine that these fields are part of a
`messages` table that's used in a typical chat application. Suppose
there are two users located in different time zones sending messages
to each other using this app. When storing a message in the db, we
want to capture the exact instant in time and store it in the
`created_at` column. While displaying the messages to each user, we
can convert them to their respective time zones.

This also means that a timestamp value in the db will continue to
represent the same instant in time even if the `timezone` setting is
changed. After all, `timezone` setting is nothing but default time
zone for the `psql` client.

In short, if you want to represent an instant or moment in time, this
is the way to go.

### When should you use timestamp?

In case of _timestamp_, the value stored in the db is without any time
zone context. At the time of reading it from the db, the application
may attach a time zone context to it if required.

Here is a an example use case for _timestamp_ which might be a bit
contrived (or not!). Consider a reminder app which allows its users to
add entries specifying the date and time of the day at which they want
to be reminded of something. It's reasonable for such an app to assume
that the users want to be reminded as per their local time zone. Now
imagine a particular user of this app who stays in India but has to
travel to Singapore next week for a business meeting. Before departing
from India, she sets a reminder for 8:20AM on coming Tuesday, i.e. at
a time when she'd be in Singapore. Here, the current time
zone of the user is irrelevant at the time of creating the reminder,
so there's no point in storing it as a _timestamp**z**_. A time zone
context will have to be attached to it only when the time comes
(i.e. the reminder is due), which may be in an unknown time zone!

In this case, the app can use a _timestamp_ type to store a time zone
agnostic time value in the db and at the time of reading, it can
attach the time zone context to it as per the current time zone of the
user. Think of it as asking the db,

> The user has set a reminder for 5th Dec 8:20AM. What would be the
> instant in time if the user is currently located in Singapore?
> Please return it in the time zone I (client) prefer.

Let's try this out with an actual value. Suppose the user sets the
reminder for `2023-12-05 08:20:00`. Being a _timestamp_ type, this
value will be stored in the db as it is. At the time of querying, the
app can ask the db to convert it to the `timezone` setting (UTC for
simplicity <a id="footnote-2-ref" href="#footnote-2"><sup>2</sup></a>)
considering the local time zone of 'Asia/Singapore'.

```sql
CREATE TABLE reminders (
user_id int,
topic text,
remind_at timestamp without time zone
);

INSERT INTO reminders
VALUES (1, 'pre-book cab', '2023-12-05 08:20:00');

SELECT
topic
FROM
reminders
WHERE
user_id = 1
AND now() >= remind_at AT TIME ZONE 'Asia/Singapore';
```

In the where clause above, both the L.H.S and R.H.S will be
_timestamp**z**_ values in the client time zone. Whereas the user's
current time zone 'Asia/Singapore' is something that can be obtained
and/or periodically synced from the application frontend (web browser
or mobile app).

For e.g. if the query is run inside a per minute cronjob <a
id="footnote-3-ref" href="#footnote-3"><sup>3</sup></a>, then the one
that gets triggered at 00:20 UTC on 5th Dec will return the above
reminder (Singapore being 8 hours ahead of UTC - considering UTC as
the server time as well as the client time zone).

### What if time zones don't matter (for your app)?

I haven't mentioned any case where time zones don't matter. In my
experience, I've yet to come across such a (realistic) use case. If
you happen to know any, please let me know. In today's well connected
world, there's always a possibility - what if the user travels to
another country with a different time zone? In case of a personal
project, that user would be you. Even in case of those apps that are
meant to be operational in only one specific region (eg. cab booking,
food delivery etc.), there could be reasons to support multiple time
zones e.g. what if some one staying in the US wants to use
Zomato/Swiggy to order food for their family or friends in India <a
id="footnote-4-ref" href="#footnote-4"><sup>4</sup></a>.

### Final thoughts

The decision about which variant of timestamp to use for a particular
column is an important one and needs to be taken at the time of schema
design. Always using _timestamp**z**_ just because there's no extra
cost in storing data is a lazy choice which may come back to bite you
later. At that point, it'd be impossible to fix it without introducing
hard coded assumptions and performing time zone conversion gymnastics
in business logic. Thinking about time zones right from the beginning
may also simply the system by letting the db perform the necessary
time zone operations instead of the application code, which I believe
is a win.

---

### References

1. <https://www.postgresql.org/docs/current/datatype-datetime.html>

2. <https://www.postgresql.org/docs/current/functions-datetime.html#FUNCTIONS-DATETIME-ZONECONVERT>

3. <https://www.enterprisedb.com/postgres-tutorials/postgres-time-zone-explained>


### Footnotes

<b id="footnote-1">1</b>. Even though the `timezone` setting is
configured for the server, it represents the time zone in which a
timestamp value is displayed to the client. Hence "client time zone"
is an appropriate name for it. Think of it as the default client time
zone that the server will use if the client doesn't set one. <a
href="#footnote-1-ref">&#8617;</a>

<b id="footnote-2">2</b>. It's always easier to use UTC as the
reference for calculating offsets. Hence it's usually recommended to
use UTC as the application time. I believe it's the same reason why
PostgreSQL (if you consider it a _server application_) internally
stores timestamps in UTC only. <a href="#footnote-2-ref">&#8617;</a>

<b id="footnote-3">3</b>. For the sake of this example, I am
considering a simple implementation of the reminder app that uses a
per minute cronjob as the "timer", that triggers a polling query to
fetch all reminders due in a 1 min time window. I doubt if real world
reminder apps would be using cronjob for the timer, but a similar
query could be used with any timer implementation. <a
href="#footnote-3-ref">&#8617;</a>

<b id="footnote-4">4</b>. Not sure if Zomato, Swiggy support this use
case but it'd be commendable if they do. <a
href="#footnote-4-ref">&#8617;</a>
