Title: Using postgresql's enum types with Korma
Author: Vineet Naik
Date: 2014-02-24
Tags: clojure, postgresql
Category: clojure
Summary: 
Status: published


I have been playing with Clojure on the side for a few months and
these days I am trying to build a simple webapp using compojure,
enlive and korma. One problem I faced early on was getting
postgresql's enum type to work with korma. Insert and select queries
using strings for enum type values failed. In the end, I could get it
working but finding help online or from the docs wasn't easy. So I
thought it's a good chance to write my first blog post about Clojure
;-)

The example I will be using is a stripped down version of a table from
the app which has a field named `impact` that can either be "positive"
or "negative". The name of the table is `activities` and for
simplicity, I have skipped primary keys, foreign key relations and
other irrelevant details.

```sql
    CREATE TYPE impact_types AS ENUM ('positive', 'negative');
    CREATE TABLE activities (
        title varchar(140) NOT NULL,
        impact impact_types
    );
```

Let's insert a row using the terminal client and then execute a query
to get it. This works perfectly fine.

```sql
    INSERT INTO activities VALUES ('some activity', 'positive');
    SELECT * FROM activities WHERE impact = 'positive';
         title     |  impact
    ---------------+----------
     some activity | positive
    (1 row)
```

To do this in Clojure using korma, we first need to define a
connection (that I'll skip) and then an entity representing the
`activities` table.

```clojure
    (use 'korma.core)
    (defentity activities)
```

But now if we try to insert a row using korma by specifying the
`impact` value as a string, it fails as follows,

```clojure
    (insert activities (values {:title "another activity" :impact "negative"}))
```

```text
    Failure to execute query with SQL:
    INSERT INTO "activities" ("impact", "title") VALUES (?, ?)  ::  [negative another activity]
    PSQLException:
     Message: ERROR: column "impact" is of type impact_types but expression is of type character varying
      Hint: You will need to rewrite or cast the expression.
      Position: 54
     SQLState: 42804
     Error Code: 0
    PSQLException ERROR: column "impact" is of type impact_types but expression is of type character varying
      Hint: You will need to rewrite or cast the expression.
      Position: 54  org.postgresql.core.v3.QueryExecutorImpl.receiveErrorResponse (QueryExecutorImpl.java:2157)
```

Same thing happens when executing a query with `impact` as a string in
the `where` clause.

Fortunately, the postgresql jdbc library does pretty well in terms of
showing sensible error messages and hints. As you can see, it says we
need to rewrite or cast the expression. But which type of object does
it expect?  There is nothing mentioned about this in the docs. Turns
out that the object is of class `org.postgresql.util.PGObject`. In
fact, we can find this by looking at the results of the select query
closely.

```clojure
    (select activities)
    ;; [{:impact #<PGobject positive>, :title "some activity"}]
    (class (:impact (first (select activities))))
    ;; org.postgresql.util.PGobject
```

As per the
[documentation of PGObject](http://jdbc.postgresql.org/documentation/publicapi/org/postgresql/util/PGobject.html),
it's used to describe any type that is unknown by JDBC
standards. Let's write a helper function to do this conversion..

```clojure
    (import '(org.postgresql.util PGobject))

    (defn str->pgobject
      [type value]
      (doto (PGobject.)
        (.setType type)
        (.setValue value)))
```

.. and try our earlier insert query again,

```clojure
    (insert activities
      (values {:title "another activity"
               :impact (str->pgobject "impact_types" "negative")}))
```

And now it works!

From the docs, it's also quite trivial to convert a `pgobject` to a
string at the time of post-processing the results.

```clojure
    (.getValue (:impact (first (select activities))))
    ;; "positive"
```

The only annoyance is that we will need to remember to do these
conversions as a preprocessing step before running insert/update and a
post-processing step after getting query results. But korma has got us
covered with `prepare` and `transform` functions that can be specified
for applying common mutations to data. Read more about it in the
[docs](http://sqlkorma.com/docs#entities).

```clojure
    (defn transform-for-impact
      [{impact :impact :as act}]
      (if impact
        (assoc act :impact (.getValue impact))
        act))

    (defn prepare-for-impact
      [{impact :impact :as act}]
      (if impact
        (assoc act :impact (pgobject "impact_types" impact))
        act))

    ;; modified entity definition
    (defentity activities
      (transform transform-for-impact)
      (prepare prepare-for-impact))
```

```clojure
    (select activities)
    ;; ({:impact "positive", :title "some activity"} {:impact "negative", :title "another activity"})
```

Note however that we would still need to explicitly pass a `pgobject`
instance to `where` in order to filter the results by impact. We can
still reuse the `prepare-for-impact` on the map passed to `where`
though.

Hope this post was helpful.

PS: If you are a Clojure veteran and think the above code could be
better or more idiomatic, please point it out. I am only getting
started :-)


**Edit (2nd March 2014):** Fixed `*-for-impact` functions to handle
the case where the `impact` field is not included in the map.
