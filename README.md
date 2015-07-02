# Network analysis: People and open source communities

* By Dawn M. Foster
* For OSCON 2015
* When: 10:40am–11:20am Thursday, 07/23/2015
* Room: F 147/148
* Tags: Linux, Tools and techniques

My slides will be available on [slideshare](http://www.slideshare.net/geekygirldawn)
shortly after the presentation. 

This github repo contains all of the scripts, data, instructions, and other 
technical materials that you can use to reproduce what I did in the session.
If I do this well, you'll be able to use these tools to gather data and 
perform similar analysis using your own community data. 

Data Gathering
--------------

If you are gathing data from open source communities, your best friend is
the [MetricsGrimoire](https://github.com/MetricsGrimoire) suite of tools,
especially [mlstats](https://github.com/MetricsGrimoire/MailingListStats) for mailing lists
and [CVSAnaly](https://github.com/MetricsGrimoire/CVSAnalY) for code repos.

**Step 1: Get your mailing list data into a database using mlstats.**

a) Install [mlstats](https://github.com/MetricsGrimoire/MailingListStats)

    $ python setup.py install

b) Log into mysql and create the database

    mysql> create database mlstats;

c) Import your mailing list data by running mlstats

    $ mlstats --db-user=USERNAME --db-password=PASS http://URLOFYOURLIST

Note: this can take a long time depending on how long your mailing list 
has been around and the number of messages.

**Step 2: Run database queries to extract your data**

A good list of starter queries can be found on the 
[mlstats wiki](https://github.com/MetricsGrimoire/MailingListStats/wiki/Queries) and
you'll want to look at the [database schema](https://github.com/MetricsGrimoire/MailingListStats/wiki/Database-Schema) as well

To get the data to run network analysis, I'm using this query to extract
a list of people and who they are replying to on the mailing list.

    SELECT mp.email_address AS sender, (SELECT mp2.email_address FROM 
    messages m2, messages_people mp2 WHERE m2.is_response_of=m.is_response_of 
    AND mp2.message_id=m2.is_response_of limit 1) AS receiver 
    FROM messages_people mp, messages m WHERE YEAR(m.first_date)=2015 AND 
    MONTH(m.first_date)=1 AND mp.message_id=m.message_id;

In short, this query finds everyone who has sent a message to the mailing list within 
the specified month. I limited it to a month only to make the data more manageable for
the examples. It then looks at every message and determines the person that it was
in response of. If there it was not a reply, then it is a new thread and response of
has a NULL value.

To get the data for the Gource custom log, you would need something more like this,
but you would need to re-format it into a pipe-separated file that Gource can read 
(see Python script alternative below):

    SELECT unix_timestamp(DATE_ADD(m.first_date, interval m.first_date_tz second)) 
    AS unix_date, mp.email_address AS sender, (SELECT mp2.email_address FROM 
    messages m2, messages_people mp2 WHERE m2.is_response_of=m.is_response_of AND 
    mp2.message_id=m2.is_response_of limit 1) AS receiver FROM messages_people mp, 
    messages m WHERE YEAR(m.first_date)=2015 AND MONTH(m.first_date)=1 AND 
    mp.message_id=m.message_id; 

**Step 2(alternative): Use a Python script to easily run the database query and re-format the data a bit.**

Run oscon.py:

    $ oscon.py -o <outputfiledir> -d <database> -u <user-mysql> -p <password-mysql>

What oscon.py does:

* Gathers information about where to put output files and the database being used.
* Runs the query.
* Strips the email down to the username (everything before @example.com) to have a 
shorter identifier for the users (looks much better on graphs).
* Formats the output into a nice, clean CSV file called network_output.csv excluding
new threads and self-replies.
* Formats the output into a nice Gource custom log format sorted by time
as gource_output.log

CAVEAT: I am not a real programmer; the code is ugly; and it may or may not work for 
you without some tweaking. However, I will be doing more Python programming, and I 
appreciate **helpful** suggestions about how to improve :)

RStudio
-------

If you are going to be using R for anything much, I recommend installing
[RStudio](http://www.rstudio.com/). It's an open source tool that provides a
nice interface into R. However, the script and all of the commands in it will 
run just fine if you are using the command line version of R, which may already
be installed with your OS, or you can download a more [current version](http://www.r-project.org/)

See r-files directory for plot_network.r script, which has all of the
r commands required to create the network from a file, plot it, 
and export it into a better format for Visone.

The comments in the script file should do a fair job of explaining what
the code does and why.

The purpose of this section is to show you what RStudio / r can do for basic
graph generation, and generate a file with additional network data that can
be used with Visone below.

Visone
------

**Open network file: r-files/network.dot**

* files of type: DOT files

**Network map zooming**

* Click triangle button in top right corner to optimize layout
* Use magnifying glass with plus sign to zoom in
* Use magnifying glass with 1:1 to zoom to 100%
* Use magnifying glass with square to fit to screen

**Add Labels with people's names in each circle (aka node)**

* visualization tab
* category: mapping
* type: label
* property: node lable
* attribute: v_name
* click visualize

**People who interact more should have bigger nodes**

This is based on a concept called [degree centrality](https://en.wikipedia.org/wiki/Centrality#Degree_centrality),
 which is the number of connections that someone has within the network. In this
case, it is calculated based on the interactions with other people within the network.
More interactions with other people = bigger nodes.

* analysis tab
* task: indexing
* class: node centrality
* index: degree
* click analyze
* Won't look like it's done anything until the next step to visualize it.
* visualize tab
* category: mapping
* type: size
* property: node area
* attribute: degree(%)
* click visualize

**Use weighted data to adjust line size**

* visualize tab
* category: mapping
* type: color
* property: link color
* attribute: v_weight
* method: interpolation
* scheme: click and pick a color scheme
* minimum: click, click scheme, click sequential, select a slightly darker shade
* click visualize

This gives you a feel for who talks to each other the most. Light lines = few
replies and dark lines = more replies.

**Add node colors**

* visualize tab
* category: mapping
* type: color
* property: node color
* attribute: degree (%)
* method: interpolation
* scheme: click and pick a color scheme
* maximum: click, click scheme, click sequential, select a slightly lighter shade
* click visualize

Gource
-------

Using the Gource [custom log format](https://code.google.com/p/gource/wiki/CustomLogFormat)
option.

    $ gource --highlight-users data/gource_output.log

More info about [Gource](https://github.com/acaudwell/Gource).

License and Copyright
---------------------

Code is licensed under [GNU General Public License (GPL), version 3 or later](http://www.gnu.org/licenses/gpl.txt).

Other content, including the tutorial materials in this README and data files are licensed under a 
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).

Copyright (C) 2015 Dawn M. Foster

END HERE
--------

Visone - Alternative
------

Use this alternative method if you don't want to use r to clean up the data
and do some pre-analysis. What get won't be as nice, but it will still likely 
be useful.

Open network file: network_output.csv

* files of type: CSV
* data_format: link list
* Header: checked
* network type: one mode
* directed edges: checked
* cell delimiter: ,

Network map zooming:

* Click triangle button in top right corner to optimize layout
* Use magnifying glass with plus sign to zoom in
* Use magnifying glass with 1:1 to zoom to 100%
* Use magnifying glass with square to fit to screen

Add Labels for people:

* visualization tab
* category: mapping
* type: label
* property: node lable
* attribute: sender
* click visualize

Make people who interact more have bigger nodes

* analysis tab
* task: indexing
* class: node centrality
* index: degree
* click analyze
* Won't look like it's done anything until the next step to visualize it.
* visualize tab
* category: mapping
* type: size
* property: node area
* attribute: degree(%)
* click visualize

Merge multiple links:

* drag a node with a lot of connections around to see multiple links
* transformation tab
* level: links
* operation: merge
* merge: same direction

Combine two usernames into one person

* edit menu -> deselect all (just in case you have something selected)
* control to select the two nodes
* transformation tab
* level: nodes
* operation: merge
* operation: contract nodes
* click transform
* edit menu -> deselect all (just in case you have something selected)
* control to select the two circles referencing that person (if the person responded to self)
* links menu -> delete links