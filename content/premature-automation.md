Title: Premature automation
Author: Vineet Naik
Date: 2025-02-24
Tags: checklists
Category: engineering
Summary: When and why I prefer checklists over automated scripts
Status: published

<i>This began as a paragraph in the [previous article about recurring
checklists]({filename}/recurring-checklists-org-mode.md), but it
expanded to a point where I felt it deserved to be a separate
article.</i>

As software engineers, whenever we encounter repeated tasks, our
natural reaction is to automate them. While investing in automation
does payoff in the long term, I have come to realize that it’s more
practical to maintain checklists instead of automation in many
situations. I have come across two such cases broadly:

1. When the task is business critical and has many steps or sub tasks
   involving high risk changes, it often makes more sense for humans
   to manually perform the workflow, carefully verifying the state of
   the system after every step.

2. When the task is not repeated as often, spending time in automation
   may not be justified.

Here’s an example of the first case - I was once part of a team that
was tasked with migrating multiple PostgreSQL clusters across AWS
regions. Each cluster had multiple databases with varying levels of
business criticality and SLA guarantees. So even though the end goal
was the same for every database, the migration strategies were vastly
different —

* For small databases, specially the ones where we could afford a few
  minutes of downtime, we simply paused writes and dump-restored the
  data.

* For larger databases where (near) zero downtime was important we
  used AWS DMS. The steps were intricate and were typically executed
  over multiple days.

Implementing automated workflows for different migration strategies
would have taken up a lot of our time.

While we had to repeat the same set of tasks for multiple databases,
the migration as a whole was a one time activity. Given the risks
involved, we'd have needed robust error handling and comprehensive
testing to ensure that the databases didn't go into a bad state in
between two steps. Even if such a critical activity had to be
performed more regularly, it wouldn't have been wise to automate it
until it had been manually executed successfully enough number of
times.

So we created checklist templates for each of the migration
strategies. These were nothing but pages in the same tool that we used
for documentation. When performing the migration for a particular
database, we simply cloned the relevant page and used it as a
checklist. By picking up low-risk databases first, we were able to
safely learn from our mistakes and incorporating our learning back
into the templates was much quicker and easier than having to modify
the scripts.

We did write scripts to automate individual steps, which significantly
reduced the cognitive load during the maintenance window. Due to
limited scope, it was much simpler to implement and maintain them (and
even throw them away after the job was done).

Now let’s take an example of the second case above i.e. recurring
tasks that don't have to be repeated very often. In most of my recent
side projects, I prefer checklists over scripts. A couple of them are
web apps that are deployed to cloud platforms. Some are code libraries
that are published to package repositories. Then there’s this blog
which I publish articles to every once in a while. Essentially, these
are workflows that I end up running after a gap of few days and weeks
(if not months).

If I automate them, I’d have to ensure robustness of the scripts - at
least that the common use cases are handled and tested. Otherwise
there’s a chance that when I get to deploying an app or publishing a
blog post, something fails and then I’d have debug and fix the script
first.

What if a new component gets introduced which changes the deployment
workflow? It’s much quicker to update the checklist whereas modifying
scripts may require code refactoring.

As a bonus, when I revisit a project after a time gap, going through a
checklist helps me rebuild context about the workflow as well as the
project to some extent. Personally, it inspires more confidence as
compared to trusting a script I wrote three months ago.

Here's my checklist for publishing this blog. Check my previous
article [Recurring checklists using org mode in
emacs]({filename}/recurring-checklists-org-mode.md) to understand how
it works.

```org
* TODO Publish to www.naiquev.in
  SCHEDULED: <2025-02-12 Wed .+1d>
  :PROPERTIES:
  :RESET_CHECK_BOXES: t
  :LAST_REPEAT: [2025-02-11 Tue 14:24]
  :END:
  - State "DONE"       from "TODO"       [2025-02-11 Tue 14:24]
  - [ ] Make sure that a directory ~../www.naiquev.in~ relative to
    this repository exists
    #+begin_src bash
      test -d ../www.naiquev.in
    #+end_src
  - [ ] Activate the virtual env \\
    Virtualenv is also assumed to be created inside the parent
    directory
    #+begin_src bash
      . ../.venv/bin/activate
    #+end_src
  - [ ] Generate files
    #+begin_src bash
      make publish
    #+end_src
  - [ ] Upload files to s3 bucket
    #+begin_src bash
      cd ../www.naiquev.in

      # Set credentials in environment variables
      export AWS_ACCESS_KEY_ID=******
      export AWS_SECRET_ACCESS_KEY=******

      # Run the sync command
      aws s3 sync . s3://<bucket> --exclude '.git/*' --delete
    #+end_src
```

Having said all of the above, there are indeed cases where automation
makes sense, e.g.

* If the workflow is expected to be performed too frequently, at least
  once a day or even 2-3 times a week then the time and effort spent
  in automation pays off quickly.

* If the individual steps are time critical i.e. we can’t afford to
  lose time in between steps.

* If the workflow is expected to be run by newcomers, it might be
  better to automate at least the most critical parts, so that the
  script/workflow can be made to fail fast if any pre-conditions or
  assumptions are not met.

In summary, there are advantages in choosing checklists over automated
scripts. Immediately automating a recurring task is premature
optimization. One can always start with a checklist first and then
turn it into automation later. If the steps are documented
comprehensively, it will help in future automation efforts. I’d argue
that even after the checklist is turned into automation there’s value
in maintaining the checklist for those who are curious to understand
the internals of the workflow.

Taking that thought further, just like how software is built in
layers, could automation also be imagined and built in layers? — the
lowest layer being a manual checklist, followed by a manual checklist
with individual steps automated, followed by end to end automation
that one can run with a single command or click of a button. It'd be a
considerable challenge to ensure all "layers" are in sync, but I
believe it might be well worth the effort.

And finally, this spikes my curiosity about literate programming
again. Despite being an emacs and org-mode user for over a decade,
literate programming is something I haven't explored
seriously. Perhaps it's time to give it a try.

<br/><br/> <i>Thanks to [Pranita Karekar](https://ecodhara.com/) and
[Amogh Talpallikar](https://medium.com/@amogh) for reviewing the
draft.</i>
