#!/usr/bin/env python3
import psycopg2
from psycopg2.extras import RealDictCursor

# ---------------------------
# Master Interface (Context Manager)
# ---------------------------
class PostgresMaster:
    def __init__(self, host, port, user, password, database):
        self.host     = host
        self.port     = port
        self.user     = user
        self.password = password
        self.database = database
        self.conn     = None

    def __enter__(self):
        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
        # Enable autocommit to simplify DDL/DML operations.
        self.conn.autocommit = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn is not None:
            self.conn.close()

    def execute(self, query, params=None):
        """
        Execute an SQL command using a RealDictCursor so that rows are returned as dictionaries.
        """
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params)
            try:
                result = cur.fetchall()
            except psycopg2.ProgrammingError:
                result = None
        return result
