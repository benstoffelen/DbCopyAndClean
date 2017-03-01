import mysql.connector as mariadb
from config.config import local_host, local_user, local_password
from utilities import utilities

try:
    # initialise utilities class
    utilities = utilities.Utilities()

    # connect to db's
    mariadb_connection_read = mariadb.connect(host=local_host, port=3306, user=local_user, password=local_password,
                                              database="db_ampel", charset='utf8')
    mariadb_connection_write = mariadb.connect(host=local_host, port=3306, user=local_user, password=local_password,
                                               database="comment_sentiment", charset='utf8')

    cursor_read = mariadb_connection_read.cursor(buffered=True)
    cursor_write = mariadb_connection_write.cursor(buffered=True)
    print "Copy comments to table."

    query_stmt = "SELECT id,text FROM db_ampel.comment c LIMIT 100"
    cursor_read.execute(query_stmt)

    print "Total comments in database: " + str(cursor_read.rowcount)

    if cursor_read.rowcount == 0:
        print("No values to be copied. Terminating update process.")
    else:
        rows = cursor_read.fetchall()
        for row in rows:
            # create variables
            id = row[0]
            text = row[1]

            # clean text
            text = utilities.clean_text(text)

            # try to parse the language
            lang = utilities.check_language_langid(text)

            # if the language is german do some further parsing
            if lang == 'de':
                # split into sentences
                for idx, sentence in enumerate(utilities.split_into_sentences(text)):
                    # if the sentence is larger than three char (too avoid random jitter)
                    if len(sentence) > 3:
                        print sentence
                        #stmt = 'INSERT IGNORE INTO comment_sentiment.comments(`id`, `comment_text`) VALUES("' + row[
                        #    0] + "_" + str(idx) + '","' + sentence + '")'
                        #cursor_write.execute(stmt)
                        #mariadb_connection_write.commit()
                #print("Added to DB. Text: " + text + " Language detected: " + lang)
            else:
                # if the comment is not in the german language, reject and move on
                #print "Lang not DE. Skipped: " + text + " Lang: " + lang
                pass

    mariadb_connection_write.close()
    mariadb_connection_read.close()
except mariadb.Error as error:
    print "Error: {}".format(error)