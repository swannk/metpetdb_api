
class SampleQuery(object):
    """ Query object for sample searches. Queries the view given by
        VIEW_NAME (current full sample results)
        Holds all query conditions in lists with names _selections
        and constructs queries for the given conditions.

    """

    def __init__ ( self , \
                       rock_type=[], \
                       country=[], \
                       owner_id=[], \
                       mineral_id = [], \
                       region_id = [], \
                       metamorphic_grade_id = [], \
                       metamorphic_region_id = [],\
                       publication_id = []
                       ) :
        self.rock_type_selections = rock_type
        self.country_selections = country
        self.owner_id_selections = owner_id
        self.mineral_id_selections = mineral_id
        self.region_id_selections = region_id
        self.metamorphic_grade_id_selections = metamorphic_grade_id
        self.metamorphic_region_id_selections = metamorphic_region_id
        self.publication_id_selections = publication_id
        self.VIEW_NAME = 'full_sample_results'
        self.SHORT_VIEW_NAME = 'basic_sample_results'
        if len (rock_type + country + owner_id + mineral_id + region_id) == 0:
            self.conditions_set = False
        else:
            self.conditions_set = True

    def get_view_name( self ):
        if not self.conditions_set:
            return self.SHORT_VIEW_NAME
        elif (len(self.mineral_id_selections) + \
                  len(self.region_id_selections) + \
                  len(self.metamorphic_grade_id_selections) + \
                  len(self.metamorphic_region_id_selections) + \
                  len(self.publication_id_selections)) == 0:
            return self.SHORT_VIEW_NAME
        else:
            return self.VIEW_NAME

    def set_rock_type( self, rock_type_list ):
        """ Specify a list of rock_type_ids as input, -1 for null values. """
        self.rock_type_selections = rock_type_list
        if len(rock_type_list) > 0:
            self.conditions_set = True

    def set_country( self, country_list ):
        """ Specify a list of countries as input, -1 for null values. """
        self.country_selections = country_list
        if len(country_list) > 0:
            self.conditions_set = True

    def set_owner_id( self, owner_id_list ):
        """ Specify a list of owner_ids as input, -1 for null values. """
        self.owner_id_selections = owner_id_list
        if len(owner_id_list) > 0:
            self.conditions_set = True

    def set_mineral_id( self, mineral_id_list ):
        """ Specify a list of mineral_ids as input, -1 for null values. """
        self.mineral_id_selections = mineral_id_list
        if len(mineral_id_list) > 0:
            self.conditions_set = True

    def set_region_id( self, region_id_list ):
        """ Specify a list of region_ids as input, -1 for null values. """
        self.region_id_selections = region_id_list
        if len(region_id_list) > 0:
            self.conditions_set = True

    def set_metamorphic_grade_id( self, id_list ):
        """ Specify a list of metamorphic grade ids as input,
             -1 for null values. 

        """
        self.metamorphic_grade_id_selections = id_list
        if len(id_list) > 0:
            self.conditions_set = True

    def set_metamorphic_region_id( self, id_list ):
        """ Specify a list of metamorphic region_ids as input,
             -1 for null values. 

        """
        self.metamorphic_region_id_selections = id_list
        if len(id_list) > 0:
            self.conditions_set = True

    def set_publication_id( self, publication_id_list ):
        """ Specify a list of publication_ids as input, -1 for null values. """
        self.publications_id_selections = publication_id_list
        if len(publication_id_list) > 0:
            self.conditions_set = True
    
    def get_facet ( self, field ):
        """ Given the attributes needed for a facet, constructs
            the necessary query and returns the string.
   
        """
        where_str = self.get_where()
        return "SELECT " + field + ", count(distinct sample_id) " \
            "FROM " + self.VIEW_NAME + " " + where_str + \
            "GROUP BY " + field

    def owner_facet( self ) :
        """ Return list of owners for the given query. """
        return self.get_facet( "owner_id, owner_name " )

    def rock_type_facet( self ) :
        """ Return list of rock types for the given query. """
        return self.get_facet( "rock_type_id, rock_type_name " )

    def country_facet( self ) :
        """ Return list of countries for the given query. """
        return self.get_facet( "country " )

    def mineral_facet( self ) :
        """ Return list of minerals for the given query. """
        return self.get_facet( "sample_mineral_id, sample_mineral_name " )

    def region_facet( self ) :
        """ Return list of regions for the given query. """
        return self.get_facet( "sample_region_id, sample_region_name " )

    def metamorphic_region_facet( self ) :
        """ Return list of metamorphic regions for the given query. """
        return self.get_facet( "sample_metamorphic_region_id, sample_metamorphic_region" )

    def metamorphic_grade_facet( self ) :
        """ Return list of metamorphic grades for the given query. """
        return self.get_facet( "sample_metamorphic_grade_id, sample_metamorphic_grade" )

    def publication_facet( self ) :
        """ Return all publication info in a single facet. """
        return self.get_facet( "publication_id, author" )


    def get_selection ( self, field, value_set ) :
        """ Assumes the values are integers corresponding to ids,
            and the field is the name of an attribute given as a string.
            Example: 'rock_type_id' [1,2,3]
        """

        where_segment = ""
        if len(value_set) == 0:
            return ""
        elif len(value_set) == 1:
            return " and " + field + " = " + str(value_set[0])
        else: # more than 1 value in the set
            where_segment = " and (" + field + " in ("
            for item in value_set:
                where_segment += str(item) + ","
            where_segment = where_segment.strip(",")  + "))"
        return where_segment

    def get_where ( self ) :
        """ Constructs the WHERE clause for the current query object
            containing all specified conditions.

        """

        query_str = "WHERE public_data = 'Y' "
        if self.conditions_set:
            query_str += self.get_selection('rock_type_id', self.rock_type_selections)
            query_str += self.get_selection('country', self.country_selections)
            query_str += self.get_selection('owner_id', self.owner_id_selections)
            query_str += self.get_selection('sample_mineral_id', self.mineral_id_selections)
            query_str += self.get_selection('sample_region_id', self.region_id_selections)
            query_str += self.get_selection('sample_metamorphic_grade_id',\
                                                self.metamorphic_grade_id_selections)
            query_str += self.get_selection('sample_metamorphic_region_id',\
                                                self.metamorphic_region_id_selections)

            query_str += self.get_selection('publication_id',\
                                                self.publication_id_selections)

        return query_str + " "


    def __str__ ( self ) :
        query_str =\
            "SELECT DISTINCT sample_id, sample_number " \
            ", rock_type_name, owner_name, mineral_info "\
            ", latitude, longitude " \
            "FROM  " + self.get_view_name() + " " + self.get_where() + \
            "ORDER BY sample_id, sample_number, rock_type_name, owner_name "
        return query_str



if __name__ == '__main__':
    q = SampleQuery()

    print str(q)

    p = SampleQuery(rock_type=[3,], owner_id=[139], mineral_id=[3,], region_id=[52,], metamorphic_grade_id=[17,])

    print str(p)

    '''p = SampleQuery(rock_type=[1,2], country=["'United States'"], owner_id=[4,5,-1], \
                       mineral_id = [-1], region_id = [], publication_id = [1,2,3] ) 

    print str(p)

    r = SampleQuery(mineral_id = [-1] ) 

    print str(r)

    
    print ""

    print q.owner_facet()

    print p.owner_facet()
    print p.rock_type_facet()
    print p.country_facet()
    print p.mineral_facet()
    print p.region_facet()
    print p.publication_facet()

    print "********"
    print p.metamorphic_region_facet()

    print "*********"
    print p.metamorphic_grade_facet()

    print "*********"
    print p.publication_facet()'''
   

  
