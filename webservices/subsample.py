from webservices.db import _DbObject, _DbGetQuery

# http://127.0.0.1:8000/api/subsample/1216/
class SubsampleObject(_DbObject):
    def __init__(self, id = None):
        self.getQuery = _SubsampleGetQuery();
        
        if id:
            self._get({"subsample_id": id})
            
    def get(self, id):
        return self._get({"subsample_id": id})
            
    def exists(self):
        return "id" in self.attributes
        
class _SubsampleGetQuery(_DbGetQuery):
    def __init__(self):
        self.oneQuery = (
            "SELECT "
                "subsamples.subsample_id AS id, "
                "subsamples.public_data AS public, "
                "subsamples.name, "
                "subsample_type.subsample_type AS type, "
                "users.name AS owner, "
                "("
                    "SELECT "
                        "COUNT(*) " 
                    "FROM "
                        "subsamples, "
                        "images "
                    "WHERE "
                        "subsamples.subsample_id = %(subsample_id)s AND "
                        "images.subsample_id = subsamples.subsample_id"
                ") AS image_count, "
                "("
                    "SELECT "
                        "COUNT(*) "
                    "FROM "
                        "subsamples, "
                        "chemical_analyses "
                    "WHERE "
                        "subsamples.subsample_id = %(subsample_id)s AND "
                        "chemical_analyses.subsample_id = subsamples.subsample_id"
                ") AS chemical_analysis_count "
            "FROM "
                "users, "
                "subsamples, "
                "subsample_type "
            "WHERE "
                "subsamples.subsample_type_id = subsample_type.subsample_type_id AND "
                "users.user_id = subsamples.user_id AND "
                "subsamples.subsample_id = %(subsample_id)s"
            )
            
# This is displayed on bottom of samples page view
class SubsampleTableObject(_DbObject):
    def __init__(self, sample_id = None):
        self.getQuery = _SubsampleTableGetQuery();
        
        if id:
            self._get({"sample_id": sample_id})
            
    def get(self, id):
        return self._get({"sample_id": sample_id})

    def exists(self):
        return "*" in self.attributes and len(self.attributes["*"]) > 0

        
class _SubsampleTableGetQuery(_DbGetQuery):
    def __init__(self):
        self.manyQueries = {
            "*": (
                "SELECT "
                    "subsamples.subsample_id AS id, "
                    "subsamples.name, "
                    "subsamples.public_data AS public, "
                    "subsample_type.subsample_type AS type, "
                    "("
                        "SELECT "
                            "COUNT(*) " 
                        "FROM "
                            "subsamples, "
                            "images "
                        "WHERE "
                            "subsamples.sample_id = %(sample_id)s AND "
                            "images.subsample_id = subsamples.subsample_id"
                    ") AS image_count, "
                    "("
                        "SELECT "
                            "COUNT(*) "
                        "FROM "
                            "subsamples, "
                            "chemical_analyses "
                        "WHERE "
                            "chemical_analyses.subsample_id = subsamples.subsample_id AND "
                            "subsamples.sample_id = %(sample_id)s"
                    ") AS chemical_analysis_count, "
                    "users.name AS owner_name "
                "FROM "
                    "users, "
                    "subsamples, "
                    "subsample_type "
                "WHERE "
                    "subsamples.subsample_type_id = subsample_type.subsample_type_id AND "
                    "users.user_id = subsamples.user_id AND "
                    "subsamples.sample_id = %(sample_id)s"
                )
            }
