from django.db import connection as con
from webservices.util import dictfetchone, dictfetchall, CustomJSONEncoder
import json

class _DbObject(object):
    attributes = {}

    getQuery = None
    
    def _get(self, conditions):
        self.attributes = self.getQuery.execute(conditions)
        return self.exists()
    
    def exists(self):
        raise NotImplementedError("Should have implemented this")
        
    def json(self):
        return json.dumps(self.attributes, cls=CustomJSONEncoder)

class _DbGetQuery(object):
    oneQuery = None
    manyQueries = None

    def __init__(self):
        raise NotImplementedError("Should have implemented this")

    def execute(self, conditions):
        data = {}
        cursor = con.cursor()

        if self.oneQuery:
            print self.oneQuery
            print conditions
            cursor.execute(self.oneQuery, conditions)
            data = dictfetchone(cursor)
        
        if (self.oneQuery and "error" not in data and self.manyQueries) or (self.oneQuery is None and self.manyQueries):
            for item, query in self.manyQueries.iteritems():
                cursor.execute(query, conditions)
                data[item] = dictfetchall(cursor)
        
        return data
