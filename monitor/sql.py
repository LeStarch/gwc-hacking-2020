""" Service monitoring the DOSable endpoint

This service will report DOS status as it is monitored. Should the service go down, this will report that the service is
down. Fantastic!
"""
import os
import sqlite3
from flask import Flask, request, send_from_directory, jsonify
import requests
import shutil
from monitor.base import Monitor, Health


KNOWN = [('saran', 'maga2020!'), ('michaels', '2!cool4you'), ('land', 'IamTheVeryModel8'), ('vivianb', 'zoomersBlikeTHAT'), ('carlosm', 'python4ever')]
SINGLETON = None

class SQLMon(Monitor):
    """ Monitors the DOS service """
    def __init__(self, app):
        """ App initialization"""
        global SINGLETON
        self.last_query = ""
        self.health = Health.HEALTHY
        self.message = "No issue"
        app.route('/sql', endpoint="sql", methods=['POST'])(self.sql_service)
        super().__init__(app)
        SINGLETON = self

    def status(self):
        """ Reports the status of the request """
        try:
            conn = sqlite3.connect("./gwc.sql")
            self.corruption(conn)
            conn.close()
        finally:
            return self.message, self.health

    def restart(self):
        shutil.copy("./gwc.sql.bak", "./gwc.sql")
        self.health = Health.HEALTHY
        self.message = "No issues"
        super().restart()

    def execute_all_templated(self, conn, query, *values, system=False):
        """ Execute templated query anf get results """
        query_filled = query.format(*values)
        self.last_query=query_filled if not system else self.last_query
        queries = [item for item in query_filled.split(";") if item != ""]
        results = []
        if len(queries) > 1 and not system:
            self.health = Health.SICK
            self.message = "SQL injection detected"
        for query in queries:
            response = conn.execute(query + ";")
            results.extend([item for item in response])
        return results

    def corruption(self, conn):
        """ Detect corruption """
        try:
            results = self.execute_all_templated(conn, "SELECT * FROM PASSWORDS;", system=True)
            if results != KNOWN:
                self.health = Health.DEAD
                self.message = "Password corruption detected"
                return

            results = self.execute_all_templated(conn, "SELECT * FROM USERS;", system=True)
            if results != [(known[0], ) for known in KNOWN]:
                self.health = Health.DEAD
                self.message = "User corruption detected"
                return
            results = self.execute_all_templated(conn, "SELECT * FROM MESSAGES;", system=True)
        except Exception as exc:
            if "no such table:" in str(exc):
                self.health = Health.DEAD
                self.message = "Data loss detected"
            else:
                self.health = Health.DEAD
                self.message = str(exc)
        return

    def login(self, conn, user_string, pass_string):
        """ Login code """

        results = self.execute_all_templated(conn, "SELECT name FROM USERS WHERE name='{}';", user_string)
        if not results:
            raise Exception("No such user {}".format(user_string))
        elif len(results) > 1:
            raise Exception("Conflicting users: {}. Please contact administrator.".format(results))

        # Check password
        results = self.execute_all_templated(conn, "SELECT password FROM PASSWORDS WHERE name='{}';", user_string)
        if not results:
            raise Exception("No such user {}".format(user_string))
        elif results[0][0] != pass_string:
            raise Exception("Bad password, try again.")
        # Bad, login detected
        self.health = Health.DIEING
        self.message ="User account breach: {}".format(user_string)



    @staticmethod
    def sql_service():
        """ SQL service, poorly implemented"""
        global SINGLETON
        conn = None
        try:
            if SINGLETON is None:
                raise Exception("Somehow not setup????")
            conn = sqlite3.connect("./gwc.sql")
            user_string = request.form.get("user", "anonymous")
            pass_string = request.form.get("password", "")
            SINGLETON.login(conn, user_string, pass_string)
            results = SINGLETON.execute_all_templated(conn, "SELECT message FROM MESSAGES WHERE name='{}';", user_string)
            message = "Your messages: {}".format("".join(["{}".format(item) for item in results]))
        except sqlite3.Error as exc:
            message = "Database reported error: {}".format(exc)
        except Exception as err:
            message = "Other Error: {}".format(err)
        # Failsafe commit before request exist
        if conn is not None:
            conn.commit()
            conn.close()
        return message + "-hint-{}".format(SINGLETON.last_query)
