from webservices.db import _DbObject, _DbGetQuery

# http://127.0.0.1:8000/api/subsample/1216/
class SampleObject(_DbObject):
    def __init__(self, id = None):
        self.getQuery = _SampleGetQuery();
        
        if id:
            self._get({"sample_id": id})
            
    def get(self, id):
        return self._get({"sample_id": id})
            
    def exists(self):
        return "id" in self.attributes

class _SamplePermissionsQuery(_DbGetQuery):
    def __init__(self):
        self.oneQuery = ()

        
class _SampleGetQuery(_DbGetQuery):
    def __init__(self):
        self.oneQuery = (
            "SELECT "
                "samples.sample_id AS id, "
                "samples.number, "
                "samples.collection_date, "    
                "CASE WHEN samples.public_data = 'Y' THEN TRUE ELSE FALSE END AS public_data, "
                "samples.country, "
                "samples.description, "
                "samples.location_text, "
                "st_y(samples.location) AS latitude, "
                "st_x(samples.location) AS longitude, "
                "owner.name AS owner_name, "
                "collector.name AS collector_name, "
                "rock_type.rock_type AS rock_type_name, "
                "metamorphic_grades.name AS metamorphic_grade_name, "
                "COUNT(subsamples.subsample_id) AS subsamples_count "
            "FROM (((((( "
                "samples "
                "LEFT OUTER JOIN subsamples "
                "ON samples.sample_id = subsamples.sample_id ) "
                "LEFT OUTER JOIN users owner "
                "ON samples.user_id = owner.user_id ) "
                "LEFT OUTER JOIN users collector "
                "ON samples.collector_id = collector.user_id ) "
                "LEFT OUTER JOIN rock_type "
                "ON samples.rock_type_id = rock_type.rock_type_id ) "
                "LEFT OUTER JOIN sample_metamorphic_grades "
                "ON samples.sample_id = sample_metamorphic_grades.sample_id ) "
                "LEFT OUTER JOIN metamorphic_grades "
                "ON sample_metamorphic_grades.metamorphic_grade_id = metamorphic_grades.metamorphic_grade_id ) "
            "WHERE "
                "samples.sample_id = %(sample_id)s "
            "GROUP BY "
                "samples.sample_id, "
                "samples.number, "
                "samples.collection_date, "
                "samples.public_data, "
                "samples.country, "
                "samples.description, "
                "samples.location_text, "
                "st_y(samples.location), "
                "st_x(samples.location), "
                "owner.name, "
                "collector.name, "
                "rock_type.rock_type, "
                "metamorphic_grades.name"
            )
                        
        self.manyQueries = {
            "aliases": (
                "SELECT "
                    "alias AS name "
                "FROM "
                    "sample_aliases "
                "WHERE "
                    "sample_aliases.sample_id = %(sample_id)s"
                ),
            "minerals": (
                "SELECT "
                    "name "
                "FROM "
                    "minerals, "
                    "sample_minerals "
                "WHERE "
                    "minerals.mineral_id = sample_minerals.mineral_id AND "
                    "sample_minerals.sample_id = %(sample_id)s"
                ),
            "regions": (
                "SELECT "
                    "name "
                "FROM "
                    "regions, "
                    "sample_regions "
                "WHERE "
                    "regions.region_id = sample_regions.region_id AND "
                    "sample_regions.sample_id = %(sample_id)s"
                ),
            "metamorphic_regions": (
                "SELECT "
                    "name "
                "FROM "
                    "metamorphic_regions, "
                    "sample_metamorphic_regions "
                "WHERE "
                    "metamorphic_regions.metamorphic_region_id = sample_metamorphic_regions.metamorphic_region_id AND "
                    "sample_metamorphic_regions.sample_id = %(sample_id)s"
                ),
            "references": (
                "SELECT "
                    "name "
                "FROM "
                    "reference, "
                    "sample_reference "
                "WHERE "
                    "reference.reference_id = sample_reference.reference_id AND "
                    "sample_id = %(sample_id)s"
                ),
            "images": (
                "SELECT "
                    "images.checksum_64x64, "
                    "images.height, "
                    "images.width, "
                    "image_type.image_type "
                "FROM images, "
                    "image_type "
                "WHERE "
                    "images.image_type_id = image_type.image_type_id AND "
                    "sample_id = %(sample_id)s"
                )
            }

