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
            return ans
        except Exception as e:
            if self._db.closed != 0:
                self._db = connect(host=self.mhost, database=self.db, user=self.usr, password=self.pwd)
                return self.consultar(sql=sql)
            else:
                e = str(e)
                raise AssertionError(e)

    def proximaPK(self, tabela, chave):
        sql = 'select max(' + chave + ') from ' + tabela
        rs = self.consultar(sql)
        pk = rs[0][0]
        if pk is None:
            return 0
        else:
            return pk + 1

    def fechar(self):
        self._db.close()
