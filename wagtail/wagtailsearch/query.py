from __future__ import absolute_import, unicode_literals


class SearchQuery:
    def __and__(self, other):
        return And([self, other])

    def __or__(self, other):
        return Or([self, other])

    def __invert__(self):
        return Not(self)


class SearchQueryOperator(SearchQuery):
    pass


class And(SearchQueryOperator):
    def __init__(self, subqueries):
        self.subqueries = subqueries


class Or(SearchQueryOperator):
    def __init__(self, subqueries):
        self.subqueries = subqueries


class Not(SearchQueryOperator):
    def __init__(self, subquery: SearchQuery):
        self.subquery = subquery


class MatchAll(SearchQuery):
    pass


class PlainText(SearchQuery):
    def __init__(self, query_string: str, operator: str = None,
                 boost: float = 1.0):
        self.query_string = query_string
        self.operator = operator
        self.boost = boost


class Term(SearchQuery):
    def __init__(self, term: str, boost: float = 1.0):
        self.term = term
        self.boost = boost


class Prefix(SearchQuery):
    def __init__(self, prefix: str, boost: float = 1.0):
        self.prefix = prefix
        self.boost = boost


class Fuzzy(SearchQuery):
    def __init__(self, term: str, max_distance: float = 3, boost: float = 1.0):
        self.term = term
        self.max_distance = max_distance
        self.boost = boost


class Boost(SearchQuery):
    def __init__(self, query: SearchQuery, boost: float):
        self.query = query
        self.boost = boost


class Filter(SearchQuery):
    def __init__(self, query: SearchQuery,
                 include: SearchQuery = None, exclude: SearchQuery = None):
        self.query = query
        self.include = include
        self.exclude = exclude


MATCH_ALL = MatchAll()
