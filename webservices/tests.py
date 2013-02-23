from django_nose import FastFixtureTestCase


class UtilTest(FastFixtureTestCase):
    def __init__(self, arg):
        import webservices.util as util
        self.CustomJSONEncoder = util.CustomJSONEncoder
        self.dictfetchall = util.dictfetchall
        self.dictfetchone = util.dictfetchone

        super(UtilTest, self).__init__(arg)


    # testing functions

    def test_CustomJSONEncoder(self):
        import json

        expected_string = '[{"a": "QQQ"}, {"b": 777}, {"1": "ZZZ"}]'

        data = [
            {"a": "QQQ"},
            {"b": 777},
            {1: "ZZZ"}
        ]

        self.assertEquals(expected_string, json.dumps(data, cls=self.CustomJSONEncoder))
        
    def test_CustomJSONEncoder_datetime(self):
        import json
        import datetime

        expected_string = '"2010-12-25T00:00:00"'

        data = datetime.datetime(2010, 12, 25)

        self.assertEquals(expected_string, json.dumps(data, cls=self.CustomJSONEncoder))


    def test_dictfetchall_regions_dne(self):
        expected_regions = []

        cursor = self._query_regions({"sample_id": -1})
        self.assertEqual(cursor.rowcount, 0)

        regions = self.dictfetchall(cursor)

        self.assertEqual(expected_regions, regions)


    def test_dictfetchall_regions_3805(self):
        expected_regions = [
            {"name": "New Mexico"},
            {"name": "Sangre De Cristo Mts"},
            {"name": "Trampas Ridge"}
        ]

        cursor = self._query_regions({"sample_id": 3805})
        self.assertEqual(cursor.rowcount, 3)

        regions = self.dictfetchall(cursor)

        self.assertEqual(expected_regions, regions)


    def test_dictfetchone_regions_dne(self):
        expected_region = {"error": "DNE"}

        cursor = self._query_regions({"sample_id": -1})
        self.assertEqual(cursor.rowcount, 0)

        region = self.dictfetchone(cursor)

        self.assertEqual(expected_region, region)

    def test_dictfetchone_regions_3805(self):
        expected_regions = [
            {"name": "New Mexico"},
            {"name": "Sangre De Cristo Mts"},
            {"name": "Trampas Ridge"}
        ]

        cursor = self._query_regions({"sample_id": 3805})
        self.assertEqual(cursor.rowcount, 3)

        for i in range(cursor.rowcount):
            region = self.dictfetchone(cursor)
            self.assertIn(region, expected_regions)
            expected_regions = [expected_region for expected_region in expected_regions if expected_region != region]


    # helper functions

    def _query_regions(self, conditions):
        from django.db import connection as con

        query = (
            "SELECT "
                "name "
            "FROM "
                "regions, "
                "sample_regions "
            "WHERE "
                "regions.region_id = sample_regions.region_id AND "
                "sample_regions.sample_id = %(sample_id)s"
            "ORDER BY "
                "name"
        )

        cursor = con.cursor()
        cursor.execute(query, conditions)

        return cursor


class SampleTest(FastFixtureTestCase):
    def __init__(self, arg):
        from webservices.sample import SampleObject
        self.SampleObject = SampleObject

        super(SampleTest, self).__init__(arg)

    def test_sample_exists(self):
        sample = self.SampleObject()
        self.assertFalse(sample.exists())

        sample = self.SampleObject(-1)
        self.assertFalse(sample.exists())

        sample = self.SampleObject()
        sample.get(-1)
        self.assertFalse(sample.exists())

        sample.get("3805")
        self.assertTrue(sample.exists())

    def test_sample_attributes_3805(self):
        sample = self.SampleObject()

        self.assertTrue(sample.get("3805"))

        expected_sample_attributes = {
            "id":3805,
            "number":"test001",
            "owner_name":"Sibel Adali",
            "collector_name":null,
            "collection_date":"2006-08-01T19:00:00",
            "location_text":"RPI",
            "longitude":-105.643730163574,
            "latitude":36.002140045166,
            "country":"USA",
            "public_data":false,
            "subsamples_count":1,
            "description":"Ortega Quartzite",
            "metamorphic_grade_name":"Amphibolite facies",
            "rock_type_name":"Quartzite",
            "minerals":[
                {"name":"Amphibole"},
                {"name":"Oxides"},
                {"name":"Quartz"},
                {"name":"Biotite"},
                {"name":"Garnet"}
            ],
            "images":[
            {
                "image_type":"Back-Scattered Electron Image",
                "width":983,
                "checksum_64x64":"0408bbc03ba29b52e3eecb9c703455d7fd4abdea1b60208b04",
                "height":654
            },
            {
                "image_type":"Back-Scattered Electron Image",
                "width":64,
                "checksum_64x64":"04e70ea8dcb19107b04a9343b77f2e3f758416749e356dd6c3",
                "height":55
            }
            ],
            "metamorphic_regions":[
                {"name":"Southern Sangre De Cristo Range"},
                {"name":"Santa Fe Range"},
                {"name":"Proterozoic New Mexico"}
            ],
            "regions":[
                {"name":"Sangre De Cristo Mts"},
                {"name":"New Mexico"},
                {"name":"Trampas Ridge"}
            ],
            "references":[],
            "aliases":[]
        }

        self.assertEquals(expected_sample_attributes, sample.attributes)


