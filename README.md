# OSCON and FLOSS Community Metrics
## Network Analysis and Community Visualizations

By: [Dawn M. Foster](http://fastwonderblog.com). PhD student at the 
[University of Greenwich, Centre for Business Network Analysis](http://www2.gre.ac.uk/about/faculty/business/research/centres/cbna/home)

### OSCON: Network analysis: People and open source communities

* OSCON 2015 - [Session link](http://www.oscon.com/open-source-2015/public/schedule/detail/41617)
* Slides: [Presentation Material](http://www.slideshare.net/geekygirldawn/network-analysis-people-and-open-source-communities)
is on SlideShare
* Video: [Uploaded on YouTube](https://www.youtube.com/watch?v=YoLnV5snX_Q&feature=youtu.be)
* When: 10:40am–11:20am Thursday, July 23, 2015
* Room: E147/148 
* Tags: Linux, Tools and techniques

### FLOSS Community Metrics: Gource Custom Data: Visualizations

* [FLOSS Community Metrics](http://flosscommunitymetrics.org/) - Portland 2015
* Slides: [Presentation Material](http://www.slideshare.net/geekygirldawn/floss-community-metrics-gource-custom-log-formats)
is on SlideShare
* When: 1:40 - 2:00 Sunday, July 18, 2015
* At: Community Leadership Summit
* Uses: [Data Gathering](https://github.com/geekygirldawn/oscon_2015#data-gathering) and
[Gource](https://github.com/geekygirldawn/oscon_2015#gource) sections of this README.

Additional Info
---------------

My slides will be available on [slideshare](http://www.slideshare.net/geekygirldawn)
shortly after the presentations.

This github repo contains all of the scripts, data, instructions, and other 
technical materials that you can use to reproduce what I did in the sessions.
If I do this well, you'll be able to use these tools to gather data and 
perform similar analysis using your own community data. 

This README file is where you can find most of the instructions for replicating the
data and analysis from the presentations along with some extra material.

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

This is the "do it yourself" method and requires a bit manual / scripting work on your part. See Step 2 (alternative) below for a Python script that does this for you.

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

**Step 2 (alternative): Use a Python script to easily run the database query and re-format the data a bit.**

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
be installed with your OS, or you can download a more [current version](http://www.r-project.org/).

See the [r-files directory](https://github.com/geekygirldawn/oscon_2015/tree/master/r-files)
for plot_network.r script, which has all of the
r commands required to create the network from a file, plot it, 
and export it into a better format for Visone.

The comments in the script file should do a fair job of explaining what
the code does and why.

The purpose of this section is to show you what RStudio / R can do for basic
graph generation and to generate a file with additional network data that can
be used with Visone below.

Visone
------

The instructions for this section are quite long. Since it's a GUI-based application,
there are no script files, just a long list of things to click on to get the desired results.

[Visone](http://visone.info/) is a free app (sadly not open source) that can be 
[downloaded](http://visone.info/html/download.html) and runs as a Java app. There are some
other open source tools, including the above R example, for this type of visualization, 
but I haven't found one that works quite as well as Visone and runs across all major OSs.

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

**Use weighted data to adjust line color**

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

**Export image**

* File -> export
* Select an option (PNG, PDF, SVG, and many more)
* Click save
* The next pop-up, you can take the defaults (complete graph, original size) or customize the size.

Gource
-------

More info about [Gource](https://github.com/acaudwell/Gource), 
including downloads and information about installation. You can 
also look at the presentation I did about Gource at the
[FLOSS Community Metrics Meeting](http://www.slideshare.net/geekygirldawn/floss-community-metrics-gource-custom-log-formats)

Using the Gource [custom log format](https://code.google.com/p/gource/wiki/CustomLogFormat)
option.

I also added a few other options to make it look a bit nicer:

* -i : Time files remain idle (default 0). This allows people being replied to 
       to disappear after 10 seconds to clean up a bit and make it more readable.
* --max-user-speed : Speed users can travel per second (default: 500). I slowed 
       this down to 100 to make it easier to see the users.
* -a 1 : Auto skip to next entry if nothing happens for a number of seconds (default: 3)
         sped this up a bit.
* --highlight-users : keeps the usernames for the people sending emails from
                      disappearing. I would have liked to have the same for filenames
                      which are the people being replied to, but can't seem to find
                      at option for that
* -s 30 : seconds per day. Not used here, but when you run these yourself, you might
          want to slow things down a bit so you can better see what's going on.

    $ gource -i 5 --max-user-speed 100 -a 1 --highlight-users gource_output.log

If you've never run Gource on your code repositories, you should!

    $ gource </path/to/repo> 

I recommend playing around with the different controls to speed things up / slow down or show / hide
things to get something that looks good with your data. Most of this information can be found
using gource -H, but the [control page](https://github.com/acaudwell/Gource/wiki/Controls)
on the wiki has more details about the controls. You might also check out these [templates]
(https://github.com/FOSSRIT/gourciferous/tree/develop/Templates) with recommended configurations
for different types of data (large projects, long-lived projects, etc.)

You can also check out [Gourciferous](https://github.com/FOSSRIT/gourciferous) for visualizing multiple
repos in a single visualization using the custom log format.

Data and Examples
-----------------

The data used in the examples comes from the Linux kernel 
[IOMMU list](http://lists.linuxfoundation.org/pipermail/iommu/) for January 2015.
[IOMMU](https://en.wikipedia.org/wiki/IOMMU) (Input/Output Memory Management Unit) is used in 
the Linux kernel to map the virtual memory accessible by devices to physical memory for security
and other reasons. I selected this list for a few reasons:

* I'm studying the Linux kernel community at the University of Greenwich, so I wanted to pick something 
from the Linux kernel, but there are [over 150 mailing lists](http://vger.kernel.org/vger-lists.html)
documented for the Linux kernel (and not all of them are listed at that link).  
* The IOMMU list is lower volume than many of the kernel lists (651 posts for January), so it's more
manageable as an example.
* It is a mailman list, which has nicely formatted, clean logs that import well using mlstats.
Many of the kernel lists have other ways of logging (Gmane, etc.) that aren't quite as clean
when imported. 

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
