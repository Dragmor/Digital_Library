'''
CORRECTLY WORKED IN PYTHON v3.4.3 !
'''
import time
import sqlite3
class DB():
    """docstring for DB"""
    def __init__(self):
        self.database = None

    def connect_to_db(self):
        #open/create database
        self.database = sqlite3.connect('library.db')
        self.cursor = self.database.cursor()

    def add_table(self, table_name, rows_names):
        '''for developer! Creating tables!'''
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS 
            %s (%s)''' %(table_name ,rows_names))

        self.database.commit()
#=============================================================================#
    ''' for table books '''
    def add_book(self, book_name, author_name, book_genre):
        '''add book to db in table "book_genres" and "book_authors"'''
        book_name = book_name.lower()
        author_name = author_name.lower()
        book_genre = book_genre.lower()
        
        if self.check_book(book_name) == False:
            '''checking, if book with this name not alredy in database,
            then add this book'''
            self.cursor.execute('''
                                    INSERT INTO books 
                                    VALUES ((SELECT MAX(id) FROM books)+1,?)
                                ''', (book_name, ))

            book_id = (self.cursor.execute('''
                                                SELECT MAX(id) FROM books
                                            ''').fetchone())[0]
        else:
            self.cursor.execute('''
                                    SELECT books.id FROM books 
                                    WHERE name="%s"
                                ''' %book_name)

            book_id = self.cursor.fetchone()[0]

        if self.check_author(author_name) == False:
            self.add_author(author_name)
            author_id = (self.cursor.execute('''
                                                SELECT MAX(id) FROM authors
                                            ''').fetchone())[0]
        else:
            self.cursor.execute('''SELECT authors.id FROM authors 
                WHERE name="%s"''' %author_name)
            author_id = self.cursor.fetchone()[0]

        if self.check_genre(book_genre) == False:
            self.add_genre(book_genre)
            genre_id = (self.cursor.execute('''
                                                SELECT MAX(id) FROM genres
                                            ''').fetchone())[0]
        else:
            self.cursor.execute('''
                                    SELECT genres.id FROM genres 
                                    WHERE title="%s"
                                ''' %book_genre)

            genre_id = self.cursor.fetchone()[0]

        #checking: if current data alredy in db, skip adding data
        self.cursor.execute('''
                                SELECT id FROM books_genres 
                                WHERE book_id="'''+str(book_id)+'''" 
                                AND genre_id="'''+str(genre_id)+'''"
                            ''')

        if len(self.cursor.fetchall()) > 0:
            pass
        else:
            self.cursor.execute('''SELECT * FROM books_genres''')
            b_g_id = len(self.cursor.fetchall()) + 1
            self.cursor.execute('''
                                    INSERT INTO books_genres 
                                    VALUES (?,?,?)
                                ''', (b_g_id, book_id, genre_id))

        self.cursor.execute('''
                                SELECT id FROM books_authors 
                                WHERE book_id="'''+str(book_id)+'''" 
                                AND author_id="'''+str(author_id)+'''"
                            ''')

        if len(self.cursor.fetchall()) > 0:
            pass
        else:
            self.cursor.execute('''SELECT * FROM books_authors''')
            b_a_id = len(self.cursor.fetchall()) + 1
            self.cursor.execute('''INSERT INTO books_authors 
                VALUES (?,?,?)''', (b_a_id, book_id, author_id))
        #save new data in db
        self.database.commit()

    def view_all_books(self):
        self.cursor.execute('''SELECT * FROM books''')
        #return list of all readers
        return self.cursor.fetchall()  

    def check_book(self, book_name):
        book_name = book_name.lower()
        self.cursor.execute('''
                                SELECT * FROM books 
                                WHERE name="%s"
                            ''' %book_name)
        #return book_id, if finded in db, or 0, if book not in db
        return len(self.cursor.fetchall())

    def delete_book(self, book_id, *args):
        self.cursor.execute('''
                                DELETE FROM books 
                                WHERE id=%s
                            ''' %book_id)
        self.cursor.execute('''
                                DELETE FROM books_genres 
                                WHERE book_id=%s
                            ''' %book_id)
        self.cursor.execute('''
                                DELETE FROM books_authors 
                                WHERE book_id=%s
                            ''' %book_id)
        self.cursor.execute('''
                                DELETE FROM books_readers 
                                WHERE book_id=%s
                            ''' %book_id)
        self.database.commit()

#=============================================================================#
    ''' for table genres '''
    def add_genre(self, title):

        self.cursor.execute('''
                                INSERT INTO genres VALUES 
                                ((SELECT MAX(id) FROM genres)+1,?)
                            ''', (title, ))
        self.database.commit()

    def check_genre(self, genre):
        self.cursor.execute('''
                                SELECT * FROM genres 
                                WHERE title="%s"
                            ''' %genre)

        #return book_id, if finded in db, or 0, if book not in db
        return len(self.cursor.fetchall())

    def view_all_genres(self):
        self.cursor.execute('''
                                SELECT * FROM genres 
                                ORDER BY title
                            ''')

        return self.cursor.fetchall()

#=============================================================================#
    ''' for table readers '''
    def add_reader(self, first_name, last_name, patronymic, dormitory):
        #add human to db
        if len((self.cursor.execute('''
                                        SELECT * FROM readers 
                                        WHERE first_name="'''+last_name
                                        +'''" AND last_name="'''
                                        +first_name+'''" AND patronymic="'''
                                        +patronymic+'''"
                                    ''')).fetchall()) > 0:
            return 100

        db_data = (first_name, last_name, patronymic, dormitory)
        self.cursor.execute('''
                                INSERT INTO readers VALUES 
                                ((SELECT MAX(id) FROM readers)+1,?,?,?,?)
                            ''', (db_data))
        self.database.commit() #save changes in db

    def view_all_readers(self):
        self.cursor.execute('''
                                SELECT dormitory, last_name, first_name 
                                FROM readers
                            ''')
        #return list of all readers
        return self.cursor.fetchall()

    def delete_reader(self, reader_id, *args):
        self.cursor.execute('''
                                DELETE FROM readers 
                                WHERE id=%s
                            ''' %reader_id)

        self.cursor.execute('''
                                DELETE FROM books_readers 
                                WHERE reader_id=%s
                            ''' %reader_id)

        self.database.commit()

#=============================================================================#
    ''' for authors '''
    def add_author(self, name):
        self.cursor.execute('''
                                INSERT INTO authors VALUES 
                                ((SELECT MAX(id) FROM authors)+1,?)
                            ''', (name, ))
        self.database.commit()

    def check_author(self, author_name):
        self.cursor.execute('''
                                SELECT * 
                                FROM authors 
                                WHERE name="%s"
                            ''' %author_name)
        #
        return len(self.cursor.fetchall())

#=============================================================================#
    def add_dormitory(self, name):
        self.cursor.execute('''
                                INSERT INTO dormitorys VALUES 
                                ((SELECT MAX(id) FROM dormitorys)+1,?)
                            ''', (name, ))
        self.database.commit()

    def check_dormitory(self, name):
        self.cursor.execute('''
                                SELECT * 
                                FROM dormitorys 
                                WHERE name="%s"
                            ''' %name)
        #
        return len(self.cursor.fetchall())

    def view_all_dormitorys(self):
        self.cursor.execute('''
                                SELECT * 
                                FROM dormitorys 
                                ORDER BY name
                            ''')
        #
        return self.cursor.fetchall()

#=============================================================================#
    '''for get/give books in books_readers'''
    def book_get_give(self, book_id, reader_id, extradition):
        try:
            #get datetime in format dd-mm-yyyy hh:mm
            datetime = str(time.localtime().tm_mday)+'-'
            datetime += str(time.localtime().tm_mon)+'-'
            datetime += str(time.localtime().tm_year)+' '
            datetime += str(time.localtime().tm_hour)+':'
            datetime += str(time.localtime().tm_min)
    
            db_data = (book_id, reader_id, datetime, extradition)
    
            self.cursor.execute('''
                                    INSERT INTO books_readers VALUES 
                                    ((SELECT MAX(id) FROM books_readers)+1,?,?,?,?)
                                ''', (db_data))
            #save changes in DataBase
            self.database.commit()
        except:
            return 707
