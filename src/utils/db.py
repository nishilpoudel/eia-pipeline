import psycopg2
import os
import logging
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

def get_connection():
    """ 
    Return psycopg2 connection
    Doesn't require password because of peer authentication
    """

    return psycopg2.connect(

        dbname = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        host = os.getenv("DB_HOST"),
        port = os.getenv("DB_PORT")
    )

def get_cursor(conn):
    """
    Returns a RealDictCursor so returned rows are dicts keyed by column name rather by index

    """
    return conn.cursor(cursor_factory= RealDictCursor)

