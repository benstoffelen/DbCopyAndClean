import re

import langdetect as langdetect
import mysql.connector as mariadb
import nltk.tokenize as nlp
from langdetect.lang_detect_exception import LangDetectException

from cleaner import urlmarker
from cleaner.cleaners import check_language
from config.config import local_host, local_user, local_password

try:
    # connect to db
    mariadb_connection_read = mariadb.connect(host=local_host, port=3306, user=local_user, password=local_password,
                                              database="db_ampel", charset='utf8')
    mariadb_connection_write = mariadb.connect(host=local_host, port=3306, user=local_user, password=local_password,
                                               database="comment_sentiment", charset='utf8')

    cursor_read = mariadb_connection_read.cursor(buffered=True)
    cursor_write = mariadb_connection_write.cursor(buffered=True)
    print "Copy comments to table."

    query_stmt = "SELECT id,text FROM db_ampel.comment c"
    cursor_read.execute(query_stmt)

    print "Total comments in database: " + str(cursor_read.rowcount)

    added = 0
    not_de = 0
    not_recognised = 0
    with_url = 0
    if cursor_read.rowcount == 0:
        print("No values to be copied. Terminating update process.")
    else:
        rows = cursor_read.fetchall()
        for row in rows:
            # give info
            print "added: " + str(added) + "not_de: " + str(not_de) + "not recognised: " + str(
                not_recognised) + "with url: " + str(with_url)

            # try to parse the language
            lang = check_language()

            # if the language is german do some further parsing
            if language == 'de':
                # dismiss all posts that have urls in them
                matches = re.findall(urlmarker.WEB_URL_REGEX, row[1])
                if len(matches) > 0:
                    with_url += 1
                    continue

                # clean comment of apostrophes
                text = row[1].replace('"', "")

                # split into sentences
                for idx, sentence in enumerate(nlp.sent_tokenize(text, language='german')):
                    # if the sentence is larger than three char (too avoid random jitter)
                    if len(sentence) > 3:
                        stmt = 'INSERT IGNORE INTO comment_sentiment.comments(`id`, `comment_text`) VALUES("' + row[
                            0] + "_" + str(idx) + '","' + sentence + '")'
                        cursor_write.execute(stmt)
                        mariadb_connection_write.commit()

                added += 1
                print("Added to DB. Text: " + row[1] + " Language detected: " + langdetect.detect(row[1]))
            else:
                # if the comment is not in the german language, reject and move on
                not_de += 1
                print "Lang not DE. Skipped: " + row[1] + language

    mariadb_connection_write.close()
    mariadb_connection_read.close()

    print "Added to Database: " + str(added)
    print "Not recognised: " + str(not_recognised)
    print "Not German: " + str(not_de)

except mariadb.Error as error:
    print "Error: {}".format(error)
