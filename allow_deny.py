import sqlite3
import pandas as pd
class namelist:
    def __init__(self):
        self.db = sqlite3.connect("allow_deny.db")
        self.cu=self.db.cursor()
        self.cu = self.db.cursor()
        self.cu.execute('''
        create table if not exists 白名单(
        ip varchar(30) primary key
        );
        '''
        )

        self.cu.execute('''
        create table if not exists 白名单(
        ip varchar(30) primary key
        );
        '''
        )

        self.db.commit()

        self.cu.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.tables = self.cu.fetchall()
        self.tables = [item[0] for item in self.tables]

    def add_list(self,IP, option):
        if option not in self.tables:
            return -1
        self.cu.execute(f"insert into {option} (ip) values (?)", (IP,))
        self.db.commit()
        return 1

    def get_allow_list(self):
        self.cu.execute("select * from 白名单;")
        allowlist = pd.DataFrame(self.cu.fetchall(), columns=['ip'])
        return allowlist

    def get_deny_list(self):
        self.cu.execute("select * from 黑名单;")
        denylist = pd.DataFrame(self.cu.fetchall(), columns=['ip'])
        return denylist

    def show_tables(self):
        return self.tables

    def add_tables(self):
        pass














