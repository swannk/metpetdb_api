"""
   SampleQuery class: keeps track of which conditions are set for 
   each query and constructs different types of queries based on the
   given conditions.

   Given q = SampleQuery()

   Facet Query: will return for each facet, the name and the count
   of values. 
   Use (for facet owner): q.owner_facet()

   Brief Where Query: will return for the current condition, a list of
   results except for the counts. These  are used to populate the map.
   Use: q.get_main_brief()

   Where Query: will return for the current condition, a list of
   results. These are used to populate the list of samples. 
   Use: q.get_main()

   Count Query: will return the total number of samples for a given
   condition. To be used to double check whether to load all of them
   to the interface. Use: q.get_count()

   Limit Query: instead of returning all the tuples in Where, we can
   limit them to a specific number, N. Use: q.get_main_limit(N)


   To do: 

   1. For queries, we can return the query string and the parameters
   separately.  We need to figure out how to use them in the code. The
   WHERE query then needs to be changed.

   2. Add the counts to the WHERE query.

"""


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
        if len (rock_type + country + owner_id + mineral_id + region_id +metamorphic_grade_id + metamorphic_region_id +publication_id) == 0:
            self.conditions_set = False
        else:
            self.conditions_set = True

    def get_view_name( self, type='full' ): 
        """ Use the simpler view if no conditions relevant to the 
            complex view are set. If type is full, then use view_name
            always.

        """
        if type == 'full':
            if len(self.clean_multi_selection_list(self.mineral_id_selections) ) == 2 :
                return self.VIEW_NAME + ' sr , ' + self.VIEW_NAME + ' sr2 ' 
            else:
                return self.VIEW_NAME + ' sr ' 
        elif not self.conditions_set:
            return self.SHORT_VIEW_NAME
        elif (len(self.mineral_id_selections) + \
                  len(self.region_id_selections) + \
                  len(self.metamorphic_grade_id_selections) + \
                  len(self.metamorphic_region_id_selections) + \
                  len(self.publication_id_selections)) == 0:
            return self.SHORT_VIEW_NAME + ' sr ' 
        elif len(self.clean_multi_selection_list(self.mineral_id_selections) ) == 2 :
            return self.VIEW_NAME + ' sr , ' + self.VIEW_NAME + ' sr2 ' 
        else:
            return self.VIEW_NAME + ' sr ' 

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

    def set_metamorphic_grade_id( self, metamorphic_grade_id_list ):
        """ Specify a list of metamorphic grade ids as input,
             -1 for null values. 

        """
        self.metamorphic_grade_id_selections = metamorphic_grade_id_list
        if len(metamorphic_grade_id_list) > 0:
            self.conditions_set = True

    def set_metamorphic_region_id( self, metamorphic_region_id_list ):
        """ Specify a list of metamorphic region_ids as input,
             -1 for null values. 

        """
        self.metamorphic_region_id_selections = metamorphic_region_id_list
        if len(metamorphic_region_id_list) > 0:
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
        (where_str, params) = self.get_where()
        str = "SELECT " + field + ", count(distinct sr.sample_id) " \
            "FROM " + self.get_view_name('full') + " " + where_str + \
            "GROUP BY " + field
        str = str %params
        return str

    def get_facet2 ( self, field ):
        """ Given the attributes needed for a facet, constructs
            the necessary query and returns the string, but
            without the count
   
        """
        (where_str, params) = self.get_where()
        str = "SELECT " + field + \
            "FROM " + self.get_view_name('full') + " " + where_str + \
            "GROUP BY " + field
        str = str %params
        return str

    def owner_facet( self ) :
        """ Return list of owners for the given query. """
        return self.get_facet( "sr.owner_id, sr.owner_name " )

    def rock_type_facet( self ) :
        """ Return list of rock types for the given query. """
        return self.get_facet( "sr.rock_type_id, sr.rock_type_name " )

    def country_facet( self ) :
        """ Return list of countries for the given query. """
        return self.get_facet( "sr.country " )

    def mineral_facet( self ) :
        """ Return list of minerals for the given query. """
        return self.get_facet( "sr.sample_mineral_id, sr.sample_mineral_name " )
    
    def mineral_facet2( self ) :
        """ Return list of minerals for the given query. """
        subquery = self.get_facet2( "sr.sample_id " )

        query = "SELECT sample_mineral_id, sample_mineral_name , " \
                "count(distinct sample_id) " \
                "FROM full_sample_results " \
                "WHERE sample_id in (" + subquery + ")" \
                "GROUP BY sample_mineral_id, sample_mineral_name "
        return query


    def region_facet( self ) :
        """ Return list of regions for the given query. """
        return self.get_facet( "sr.sample_region_id, sr.sample_region_name " )

    def metamorphic_region_facet( self ) :
        """ Return list of metamorphic regions for the given query. """
        return self.get_facet( "sr.sample_metamorphic_region_id, sr.sample_metamorphic_region" )

    def metamorphic_grade_facet( self ) :
        """ Return list of metamorphic grades for the given query. """
        return self.get_facet( "sr.sample_metamorphic_grade_id, sr.sample_metamorphic_grade" )

    def publication_facet( self ) :
        """ Return all publication info in a single facet. """
        return self.get_facet( "sr.publication_id, sr.author" )

    def clean_multi_selection_list (self, inputvalue_list) :
        value_list = []
        for item in inputvalue_list:
            if len(item) != 0:
                value_list.append(item[:])
        return value_list

    def get_multi_selection ( self, field, field2, inputvalue_list ) :
        """ Assumes the values are lists of integers corresponding to ids,
            and the field is the name of an attribute given as a string.
            Example: 'mineral_type_id' [[1,2,3],[],[4,5]]
            corresponding to statement:
                 (mineral_type_id in (1,2,3)) AND (mineral_type_id in (4,5))
        """

        where_segment = ""
        params = {}
        
        value_list = self.clean_multi_selection_list(inputvalue_list)
        if len(value_list) == 0:
            return ("", {})
        elif len(value_list) == 1: ## a single list of values
            params[field] = ""
            where_segment = " and (" + field + " in (%(" + field + ")s)) "
            for item in value_list[0]:
                params[field] += str(item) + ","
            params[field] = params[field].strip(",") 
        else: ## multiple value fields
            ## must join the view with itself
            where_segment = " and sr.sample_id = sr2.sample_id "
            ## first field
            ## now field2

            values = value_list[0]
            field_name = field + '1'
            params[field_name] = ""
            where_segment += " and (" + field + \
                             " in (%(" + field_name + ")s)) "
            for item in values:
                params[field_name] += str(item) + ","
            params[field_name] = params[field_name].strip(",") 

            values = value_list[1]
            field_name = field + '2'
            params[field_name] = ""
            where_segment += " and (" + field2 + \
                             " in (%(" + field_name + ")s)) "
            for item in values:
                params[field_name] += str(item) + ","
            params[field_name] = params[field_name].strip(",") 

        return (where_segment, params)


    def get_selection ( self, field, value_set ) :
        """ Assumes the values are integers corresponding to ids,
            and the field is the name of an attribute given as a string.
            Example: 'rock_type_id' [1,2,3]
        """

        where_segment = ""
        params = {}
        if len(value_set) == 0:
            return ("", {})
        elif len(value_set) == 1:
            params[field] = str(value_set[0])
            return (" and " + field + " = %(" + field + ")s ", \
                        params)
        else: # more than 1 value in the set
            params[field] = ""
            where_segment = " and (" + field + " in (%(" + field + ")s)) "
            for item in value_set:
                params[field] += str(item) + ","
            params[field] = params[field].strip(",") 
        return (where_segment, params)

    def merge( self, query_str, params, (q,p)):
        query_str += q
        for key in p:
            params[key] = p[key]
        return query_str
        
    def get_where ( self ) :
        """ Constructs the WHERE clause for the current query object
            containing all specified conditions.

        """
        params = {}
        query_str = "WHERE sr.public_data = 'Y' "
        if self.conditions_set:
            query_str = self.merge( \
                query_str, params,\
                    self.get_selection('sr.rock_type_id', self.rock_type_selections))
            query_str = self.merge( \
                query_str, params,\
                    self.get_selection('sr.country', self.country_selections))

            query_str = self.merge( \
                query_str, params,\
                    self.get_selection('sr.owner_id', self.owner_id_selections))

            query_str = self.merge( \
                query_str, params,\
                    self.get_multi_selection('sr.sample_mineral_id', 'sr2.sample_mineral_id', self.mineral_id_selections))

            query_str = self.merge( \
                query_str, params,\
                    self.get_selection('sr.sample_region_id', self.region_id_selections))

            query_str = self.merge( \
                query_str, params,\
                    self.get_selection('sr.sample_metamorphic_grade_id',\
                                           self.metamorphic_grade_id_selections))
            query_str = self.merge( \
                query_str, params,\
                    self.get_selection('sr.sample_metamorphic_region_id',\
                                           self.metamorphic_region_id_selections))

            query_str = self.merge( \
                query_str, params,\
                    self.get_selection('sr.publication_id',\
                                           self.publication_id_selections))

        return (query_str + " ", params)


    def __str__ ( self ) :
        return self.get_main()

    def get_main_brief ( self, limit=None ) :
        (where_str,params) = self.get_where() 
        attributes = " sr.sample_id, sr.sample_number, sr.rock_type_name, "\
            "sr.owner_name, sr.latitude, sr.longitude, sr.current_location " 
        query_str =\
            "SELECT " + attributes + \
            "FROM  " + self.get_view_name() + " " + where_str + \
            "GROUP BY" + attributes
        if limit != None:
            query_str += " LIMIT " + str(limit)
        return query_str %params

#comma after current_location
    def get_main ( self, limit=None ) :
        (where_str,params) = self.get_where() 
        attributes = " sr.sample_id, sr.sample_number, sr.rock_type_name, " + \
            "sr.owner_name, sr.latitude, sr.longitude, sr.current_location, " + \
            "scv.num_subsamples, scv.num_chemical_analyses, scv.num_images "

        query_str =\
            "SELECT " + attributes + \
            "FROM  " + self.get_view_name() + ", sample_counts_view scv " +  \
            where_str + " AND sr.sample_id = scv.count_sample_id "\
            "GROUP BY" + attributes
        if limit != None:
            query_str += " LIMIT " + str(limit)
        return query_str %params

    def get_count ( self ) :
        (where_str,params) = self.get_where() 
        query_str =\
            "SELECT count(DISTINCT sr.sample_id) " \
            "FROM  " + self.get_view_name() + " " + where_str 
        return query_str %params

if __name__ == '__main__':
    q = SampleQuery()

    #print str(q)

    p = SampleQuery(rock_type=[], country=['USA',], owner_id=[], \
                    mineral_id = [[],[]], region_id = [], \
                    metamorphic_grade_id = [], \
                    metamorphic_region_id = [], publication_id = [] ) 


    print
    print p.mineral_facet()
    print
    print p.mineral_facet2()
    print

    print p.owner_facet()
    print
    print p.rock_type_facet()
    print
    print p.country_facet()
    print
    print p.mineral_facet()
    print
    print p.region_facet()
    print
    print p.publication_facet()
    print


    ##print str(p)

'''

    print str(p)

    r = SampleQuery(mineral_id = [-1] ) 

    print str(r)

    
    print ""

    print q.owner_facet()


    print "********"
    print p.metamorphic_region_facet()

    print "*********"
    print p.metamorphic_grade_facet()

    print "*********"
    print p.publication_facet()

    print "@@@@@@@@@@@@@"
    q = SampleQuery()


    print q.get_count()

    print q.get_main()

    print q.get_main(10)'''

    #print q.get_main_brief()


