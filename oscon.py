#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Copyright (C) 2015 Dawn M. Foster
# Licensed under GNU General Public License (GPL), version 3 or later: http://www.gnu.org/licenses/gpl.txt

# OSCON 2015 Presentation: Portland, OR                  
# Network analysis: People and open source communities
# Thursday, July 23, 2015 

import fileinput        # used for file operations
import os		# used to merge dir and filename
import sys, getopt      # used to read options 
import MySQLdb		# for mysql

def usage():
    print ""
    print "oscon.py"
    print "Copyright (C) 2015 Dawn M. Foster"
    print "Licensed under GNU General Public License (GPL), version 3 or later:"
    print "http://www.gnu.org/licenses/gpl.txt"
    print ""
    print "Assumes you are using a MySQL database on localhost."
    print "The month and year are hardcoded into the query for this OSCON example to make data manageable,"
    print "but you can remove that part of the query if you want to use it for all data."
    print """
-h, --help
-o, --outputfiledir   OUTFILEDIR: Set the directory for the output files where
                      you want to store them. If these files exist, the 
                      originals will OVERWRITTEN.
-d, --database	      DATABASE: the database name to query.
-u, --user-mysql      USER: the MySQL username. 
-p, --password-mysql  PASS: Not ideal, but you need to pass it a cleartext password.
"""

def main(argv):
    output_file_dir=''
    user=''
    password=''

    try: 
        opts, args = getopt.getopt(argv, "ho:d:u:p:", ["help","outputfiledir=","database=","user-mysql=","password-mysql="])
    except getopt.GetoptError:
        print 'Usage: oscon.py -o <outputfiledir> -d <database> -u <user-mysql> -p <password-mysql>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif opt in ("-o", "--outputfiledir"):
            output_file_dir = arg
        elif opt in ("-d", "--database"):
            database = arg
        elif opt in ("-u", "--user-mysql"):
            user = arg
        elif opt in ("-p", "--password-mysql"):
            password = arg

    # Prepare output files

    output_file_network = os.path.join(output_file_dir, 'network_output.csv')
    output_file_gource  = os.path.join(output_file_dir, 'gource_output.log')
    network = open(output_file_network, 'w')
    network.write('sender_email,response_of_email\n') # Add header line to csv
    gource = open(output_file_gource, 'w')

    # Output messages to make sure user has the correct details

    print 'Writing output files as:'
    print 'Network: ', output_file_network
    print 'Gource: ', output_file_gource
    print 'Database:', database

    # Prepare database

    db = MySQLdb.connect('localhost', user, password, database);
    cursor = db.cursor()

    # Run query
    try: 
        cursor.execute("select mp.email_address, m.message_id, m.subject, unix_timestamp(date_add(m.first_date, interval m.first_date_tz second)) as unix_date, m.is_response_of, (select mp2.email_address from messages m2, messages_people mp2 where m2.is_response_of=m.is_response_of AND mp2.message_id=m2.is_response_of limit 1) from messages_people mp, messages m where YEAR(m.first_date)=2015 AND MONTH(m.first_date)=1 AND mp.message_id=m.message_id;")
    except:
        print 'Error: Unable to retreive data'

    posts = cursor.fetchall()

    for row in posts:
            email = row[0]
            message_id = row[1]
            subject = row[2]
            unix_date = row[3]
            response_of = row[4]
            response_of_email = row [5]
            username = email.split("@")[0]
            if response_of_email is None: # new threads
                gource.write("%s|%s|A|new\n" % (unix_date, username))
            elif email == response_of_email: # self-replies
                pass
            else:
                username_response_of = response_of_email.split("@")[0]
                gource.write("%s|%s|M|%s\n" % (unix_date, username, username_response_of))
                network.write("%s,%s\n" % (username, username_response_of))

    # disconnect from database and close files
    db.close()
    gource.close()
    network.close()

    # Sort Gource file by timestamp
    try:
        gource = open(output_file_gource, 'r')
        try: 
            lines = gource.readlines()
            lines.sort()
            gource.close()
            gource = open(output_file_gource, 'w')
            gource.writelines(lines)
        finally:
            gource.close()
    except:
        print 'Cannot open Gource file for sorting'

if __name__ == "__main__":
   main(sys.argv[1:])


