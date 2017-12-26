import sys
import sqlite3
import json

def dbtojsonfunction(name):

    try:

        conn = sqlite3.connect('EBL.db')

    # This enables column access by name: row['column_name']
        conn.row_factory = sqlite3.Row

        curs = conn.cursor()       

    # Commit the inserted rows.
        conn.commit()

    # Now fetch back the inserted data and write it to JSON.
        


        #curs.execute("SELECT date, ltp, maximum FROM "+ name) use this for the case of stock market analysis

        curs.execute("SELECT * FROM {} ".format(name))        
        recs = curs.fetchall()

        #print ("DB data as a list with a dict per DB record:")
        rows = [ dict(rec) for rec in recs ]
        #print (rows)

    

       # print ("DB data as a single JSON string:")
        rows_json = json.dumps(rows)
        #print (rows_json)

    except (Exception, e):
        print ("ERROR: Caught exception: " + repr(e))
        raise e
        sys.exit(1)

    return (rows_json)