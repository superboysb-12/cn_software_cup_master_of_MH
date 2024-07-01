import sqlite3
import pandas as pd

db = sqlite3.connect("allow_deny.db")
cu=db.cursor()

cu.execute('''
create table if not exists 白名单(
ip varchar(30) primary key
);
'''
)


cu.execute('''
create table if not exists 黑名单(
ip varchar(30) primary key
);
'''
)

db.commit()

cu.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables=cu.fetchall()
tables=[item[0] for item in tables]


def add_list(IP,option):
    if option not in tables:
        return -1
    db = sqlite3.connect("allow_deny.db")
    cu.execute(f"insert into {option} (ip) values (?)",(IP,))
    db.commit()
    return 1

def get_allow_list():
    cu.execute("select * from 白名单;")
    allowlist=pd.DataFrame(cu.fetchall(), columns=['ip'])
    return allowlist

def get_deny_list():
    cu.execute("select * from 黑名单;")
    denylist=pd.DataFrame(cu.fetchall(), columns=['ip'])
    return denylist

def show_tables():
    return tables

def add_tables():
    pass