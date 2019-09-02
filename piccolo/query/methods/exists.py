from __future__ import annotations

from piccolo.custom_types import Combinable
from piccolo.query.base import Query
from piccolo.query.mixins import WhereDelegate
from piccolo.querystring import QueryString

from .select import Select


class Exists(Query):
    def setup_delegates(self):
        self.where_delegate = WhereDelegate()

    def where(self, where: Combinable) -> Exists:
        self.where_delegate.where(where)
        return self

    def response_handler(self, response) -> bool:
        return response[0]["exists"]

    @property
    def querystring(self) -> QueryString:
        select = Select(
            self.table,
            QueryString(f"SELECT * FROM {self.table.Meta.tablename}"),
        )
        select.where_delegate._where = self.where_delegate._where
        return QueryString('SELECT EXISTS({}) AS "exists"', select.querystring)

    def __str__(self) -> str:
        return self.querystring.__str__()
