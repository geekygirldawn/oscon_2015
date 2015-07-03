# Copyright (C) 2015 Dawn M. Foster
# Licensed under GNU General Public License (GPL), version 3 or later: 
# http://www.gnu.org/licenses/gpl.txt

# Load the ipgraph package - you may need to install it first

library(igraph)

# Load the data into a table (comma separated with a header line)

mailing_list<-read.table("~/gitrepos/oscon_2015/data/network_output.csv", sep=',', 
                                    header=T)

# Look at table and verify that it looks good

mailing_list

# Format for use with iGraph: save it as a matrix and then an edgelist with directed
# ties between people (person a sends an email to person b has a direction).

mailing_list.mat <- as.matrix(mailing_list)

mailing_list.graph <- graph.edgelist(mailing_list.mat, directed = TRUE)

# Convert duplicate conversations to weights. Gives each exchange from person a to 
# person b the weight of one (E stands for an edge sequence, which is a way to link
# people together). Converts it into a simple graph that does not have loops or duplicate
# connections (edges) between people. Combine these edge attributes (edge.attr.comb)
# by summing the weight to give a number that represents the number of times
# person a replied to person b.

E(mailing_list.graph)$weight <- 1
mailing_list.graphw <- simplify(mailing_list.graph, edge.attr.comb=list(weight="sum"))

# Interactive graph using tkplot that uses the weights calculated above to make
# the arrows between people (edges) wider depending on how many times one person has
# replied to another. The circles (nodes) representing each person become larger the
# more connections that person has to others within the network (betweeness centrality).

tkplot(mailing_list.graphw, vertex.label.color="black", edge.color="darkslategray",
       edge.width=E(mailing_list.graphw)$weight/3, edge.arrow.size=.5, 
       vertex.size=degree(mailing_list.graph)/2)

# export a format of the data with weights that can be imported into other visualization sw

write.graph(mailing_list.graphw, "/tmp/network.dot", format=c("dot"))

# STOP here. The stuff below is just bonus material for those who want a couple other alternatives.
###################







# A second tkplot using betweenness centrality (another measure)

tkplot(mailing_list.graphw, vertex.label.color="black", edge.color="darkslategray",
       edge.width=E(mailing_list.graphw)$weight/3, edge.arrow.size=.5, 
       vertex.size=betweenness(mailing_list.graph)^.5)

# Static Plot for reference - it's hard to make these look awesome.

plot.igraph(mailing_list.graphw,vertex.label=V(mailing_list.graph)$name,
            layout=layout.fruchterman.reingold, vertex.size=20, vertex.label.color="black",
            edge.color="black",edge.width=E(mailing_list.graphw)$weight/3, edge.arrow.size=.1)
