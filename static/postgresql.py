from typing import Any

import psycopg2.extras
from psycopg2 import connect


class Conexao_postgresql(object):
    def __init__(self, mhost, db, usr, pwd):
        self.pwd = pwd
        self.usr = usr
        self.db = db
        self.mhost = mhost
        self._db = connect(host=mhost, database=db, user=usr, password=pwd)

    def manipular(self, sql, _Vars):
        try:
            if 'insert' in sql[:10]:
                # if 'RETURNING id' not in sql:
                #     sql = sql + ' RETURNING id '
                cur = self._db.cursor()
                cur.execute(sql, _Vars)
                # fk = cur.fetchone()[0]
                cur.close()
                self._db.commit()
                # return fk
            else:
                cur = self._db.cursor()
                cur.execute(sql, _Vars)
                cur.close()
                self._db.commit()
        except Exception as e:
            if self._db.closed != 0:
                self._db = connect(host=self.mhost, database=self.db, user=self.usr, password=self.pwd)
                return self.manipular(sql=sql, _Vars=_Vars)
            else:
                e = str(e)
                try:
                    cur.close()
                except:
                    pass
                raise AssertionError(e)

    def query(self, sql):
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            cur.close()
            self._db.commit()
        except Exception as e:
            if self._db.closed != 0:
                self._db = connect(host=self.mhost, database=self.db, user=self.usr, password=self.pwd)
                return self.query(sql=sql)
            else:
                e = str(e)
                try:
                    cur.close()
                except:
                    pass
                raise AssertionError(e)

    def consultar(self, sql) -> list[dict[Any, Any]]:
        try:
            rs = None
            cur = self._db.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(sql)
            rs = cur.fetchall()
            ans = []
            for row in rs:
                ans.append(dict(row))
            cur.close()
            return ans
        except Exception as e:
            if self._db.closed != 0:
                self._db = connect(host=self.mhost, database=self.db, user=self.usr, password=self.pwd)
                return self.consultar(sql=sql)
            else:
                e = str(e)
                try:
                    cur.close()
                except:
                    pass
                raise AssertionError(e)

    def fechar(self):
        self._db.close()
