.. _Table_Description:


***************
Table Description
***************

.. _installing-docdir:

List of Tables
==============

Samples
-------

Stores information regarding the sample through a unique sample id, rock type id , latitude and
longitude. More information regarding the sample object and its attributes can be found at `<http://wiki.cs.rpi.edu/trac/metpetdb/wiki/SampleObject>`_

===============   ====================    ========================================================================
Attributes        Type                    Explanation     
===============   ====================    ========================================================================
sample_id         Required(PK)            Unique id for the sample for that particular owner
version           Required                It is the number of times that specific tuple has been modified(used 
                                          for concurrency issues).You read a tuple with its version info. You 
                                          read a tuple with its version info. When trying to save it, you check
                                          whether the version has not changed since you read it. If not, you 
                                          can write the new update. Otherwise, the update can fail. More 
                                          information `here <http://wiki.cs.rpi.edu/trac/metpetdb/wiki/Versioning>`_
sesar_number      Optional                Unique identifiers created by SESAR. Sample will have a sesar_number if 
                                          it is registered here (System for Earth SAmple Registration - 
                                          `<http://www.geosamples.org/>`_
public_data       Required                Y/N depending on if the sample is public / 
                                          private/project
collection_date   Optional                Must be the date when sample was collected in MM-DD-YYYY, YYYY-MM-DD 
                                          or a shortened version 
date_precision    Optional                Date could be a specific day and time (0), a specific day (1), a month  
                                          and year (31), or a year (365). Currently stored values
                                          are 0 1 31 365
number            Required                Alternate sample number. Generally the number given by the person. 
rock_type_id      Required(FK)            References the rock_type_id from the table rock_type. Every sample in the
                                          database must be one of the rock types as described `here <http://wiki.cs.rpi.edu/trac/metpetdb/wiki/RockType>`_
user_id           Required(FK)            References the users table  which stores all the user information. 
location_error    Optional                Error in meters from the actual location of the samples. 
                                          (latitude/longitude errors)  
country           Optional                Country where the sample was collected
description       Optional                Text data about the sample.
collector         Optional                Name of the person who collected the sample in the Lastname, Firstname format.
metamor
phic_region_id    Optional                Should have been a FK as the metamorphic_regions table stores the
                                          metamorphic_region_id as a required field.
collector_id      FK                      References the users for the user_id. Collector_id same as user_id?
                                                                                                                                                                                       
===============   ====================    ========================================================================



subsamples
----------

A thin subsection of the sample is called a subsample. subsamples table stores the details of the sub samples for a particular sample. Sub sample description can be found `here <http://wiki.cs.rpi.edu/trac/metpetdb/wiki/Subsample>`_

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
subsample_id           Required (PK)           Unique id for the subsample
version                Required                It is the number of times that specific tuple has been modified(used 
                                               for concurrency issues).You read a tuple with its version info. 
                                               When trying to save it, you check whether the version has not changed 
                                               since you read it. If not, you can write the new update. 
                                               Otherwise, the update can fail. More 
                                               information `here <http://wiki.cs.rpi.edu/trac/metpetdb/wiki/Versioning>`_
public_data            Required                Y/N depending on if the subsample is public / private/published
sample_id              Required (FK)           References samples table to get the corresponding sample_id.
user_id                Required                References the users table  which stores all information regarding 
                                               the users
grid_id                Optional                This information is stored if there is an image map associated 
                                               with the subsample. This information is shown depending on if the 
                                               subsample is private/public.   
name                   Required                There are 4 types of subsamples. This stores the name of the subsample.
subsample_type_id      Required                Subsample type id is stored here.                                            
=====================  ====================    ====================================================================



chemical_analyses
-----------------

Stores the chemical information for a particular subsample and associated with one sample. Hence, references subsamples and samples table through Foreign Key. The attributes can be seen in detail `here <http://wiki.cs.rpi.edu/trac/metpetdb/wiki/ChemicalAnalysisObject>`_

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
chemical_analysis_id   Required (PK)           Unique id for the chemical analysis of a subsample.
version                Required                It is the number of times that specific tuple has been modified 
                                               (used for concurrency issues). You read a tuple with its version info. 
                                               When trying to save it, you check whether the version has not changed 
                                               since you read it. If not, you can write the new update. Otherwise, 
                                               the update can fail. More information `here <http://wiki.cs.rpi.edu/trac/metpetdb/wiki/Versioning>`_
spot_id                Required                "Spot_id" is the unique identifier for a chemical analysis. 
                                               It corresponds to the point number in an electron microprobe 
                                               analytical session. t is user specified and required to be unique 
                                               for a subsample
subsample_id           Required (FK)           References the subsamples table for the subsample it is 
                                               associated with.
public_data            Required                Y/N depending on if the chemical_analysis is 
                                               public / private/project               
reference_x            Optional                The x coordinate location of the analysis on the reference image, 
                                               measured in percent of total image width (in original orientaion).
                                               The origin is assumed to be at bottom left of image.
reference_y            Optional                The y coordinate location of the analysis on the reference image,
                                               measured in percent of total image height (in original orientaion). 
                                               The origin is assumed to be at bottom left of image.
stage_x                Optional                The stage X-coordinate recorded by a microscope or microprobe.
                                               These are in microns.
stage_y                Optional                The stage Y-coordinate recorded by a microscope or microprobe. 
                                               These are in microns.
image_id               Optional (FK)           The id of the image on which the analysis location is referenced. 
analysis_method        Optional                Method of analysis from the accepted `method code <http://wiki.cs.rpi.
                                               edu/trac/metpetdb/wiki/Methods>`_
where_done             Optional                The analytical facility where analysis was performed
analyst                Optional                Name of the person who analysed the sample. Generally as Lastname,
                                               Firstname.
analysis_date          Optional                Date on which the analysis was performed.
date_precision         Optional                Date could be a specific day and time (0), a specific day (1), 
                                               a month  and year (31), or a year (365). Currently stored values are:
                                               0, 1, 31, 365
reference_id           Optional (FK)           reference_id from reference table related to this chemical analysis. 
description            Optional                Text description of the analytical strategy.
mineral_id             Optional (FK)           The id for the minerals listed for that particular sample for 
                                               which the chemical analysis is being performed. 
                                               References the minerals table.
user_id                Required (FK)           References the users table to obtain the owner of the data. 
large_rock             Required                Y/N. ‘Y’ for bulk_rock analysis, ‘N’ for spot analysis.
total                  Optional                The total weight percent of measured elements/species for this point. 
                                               This indicates the completeness of the analysis to a user.

=====================  ====================    ====================================================================



users
-----

Stores the information of the users through a unique user_id (primary key) and  email (this may be changed later on) and references the roles table for role_id as users can have many roles. 
Refer `<http://wiki.cs.rpi.edu/trac/metpetdb/wiki/UserTypes>`_ for information on roles/user types.

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
user_id                Required (PK)           Unique id for each user.
version                Required                It is the number of times that specific tuple has been modified 
                                               (used for concurrency issues). You read a tuple with its version info. 
                                               When trying to save it, you check whether the version has not changed 
                                               since you read it. If not, you can write the new update. Otherwise, 
                                               the update can fail. More information `here <http://wiki.cs.rpi.edu/trac/metpetdb/wiki/Versioning>`_
name                   Required                Name of the user
email                  Required (unique)       Email id which is used as a login
password               Required                Password chosen by users 
address                Optional                Optional information
city                   Optional                Optional information
province               Optional                Optional information
country                Optional                Optional information
postal_code            Optional                Optional information
institution            Optional                Optional information
reference_email        Optional                Optional information
confirmation_code      Optional                Not sure, may be no confirmation code for users who are just 
                                               regular users (i.e. no upload privileges) or it could  optional 
                                               due to legacy reasons.
enabled                Required                Single character for enabled/disabled status.
role_id                Required (FK)           References the roles table for the role_id of the user.

=====================  ====================    ====================================================================


roles
-----

Stores the role information for the user through the following attributes. This table may be subsumed by Drupal as a new user must be created for multiple roles for a user. The various roles of a user can be found `here <http://wiki.cs.rpi.edu/trac/metpetdb/wiki/UserTypes>`_

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
role_id                Required (PK)           Unique id for a particular role
rank                   Required (unique)       Rank of the role ; for eg: 0 -> Member, 1-> contributor etc. 
role_name              Required                Name of the role. Eg: Member, contributor, fellow etc. 

=====================  ====================    ====================================================================


sample_aliases
--------------

A sample can have multiple aliases and it is stored in the sample_aliases table with  sample_id and alias name together being unique. (i.e same sample is referred by different numbers sometimes)
(even in the presence of a unique constraint it is possible to store duplicate rows that contain a null value in at least one of the constrained columns)

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
sample_alias_id        Required(PK)            Alias id is the alternate sample number
sample_id              Required, FK(unique)    The actual sample_id whose alias is being recorded. 
alias                  Required (unique)       Name of the alias. 

=====================  ====================    ====================================================================


sample_comments
---------------

This table stores the comments associated with a sample by referencing the sample_id from the samples table. It also shows the owner of the comment by referencing the user_id from the users table. 

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
comment_id             Required (PK)           Id of the comment (integer)
sample_id              Required (FK)           Referenced from samples table
user_id                Required (FK)           Owner of the comment referenced from the users table
comment_text           Required                Comment text
date_added             Optional                Date on which the comment was added.

=====================  ====================    ====================================================================


rock_type
---------

This table stores the information regarding the rock type through the rock_type_id which is a primary key and the name of the type of rock through the attribute rock_type. 
The trac wiki `<http://wiki.cs.rpi.edu/trac/metpetdb/wiki/RockType>`_ lists the various rock types. 

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
rock_type_id           Required(PK)            Unique id of the type of rock from the above list
rock_type              Required (unique)       Name of the rock type from the above list

=====================  ====================    ====================================================================


subsample_type
--------------

This table stores the information regarding the type of subsample through subsample_type_id and subsample_type(name of subsample). The list of subsample types can be found in the subsample wiki 
`<http://wiki.cs.rpi.edu/trac/metpetdb/wiki/Subsample>`_

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
subsample_type_id      Required (PK)           Unique id of the subsample type
subsample_type         Required (unique)       Name of the subsample type

=====================  ====================    ====================================================================


chemical_analysis_elements
--------------------------

This table stores the details of the elements in the chemical analysis of a particular sample. It references the chemical_analyses and elements table to obtain the chemical_analysis_id and the element_id. It also stores the precision of the measured value through the “precision” attribute. 

(it is a correlation of chemical_analyses of a sample/subsample with the elements)
Details of chemical_analyses can be found `here <http://wiki.cs.rpi.edu/trac/metpetdb/wiki/ChemicalAnalysisObject>`_

List of elements can be found `here <http://wiki.cs.rpi.edu/trac/metpetdb/wiki/Element>`_

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
chemical_analysis_id   Required (PK, FK)       The unique id by referencing the chemical_analyses table
element_id             Required (PK, FK)       The unique id for the element by referencing the elements table. 
amount                 Required                Amount of the element present
precision              Optional                Indicates the precision of the value measured
precision_type         Optional                Type of precision in terms of absolute or relative. (‘ABS’, ‘REL’)
measurement_unit       Optional                Unit used to measure the amount of element for a particular 
                                               chemical_analyses_id. (4 characters)
min_amount             Optional                When "precision" is specified AND "precision_type"= REL, then 
                                               "min_amount"= "amount" - "precision" X "amount" and 
                                               "max_amount" = "amount" + "precision" X "amount".
max_amount             Optional                when "precision" is specified AND "precision_type"= ABS, then 
                                               "min_amount"= "amount" - "precision"  and 
                                               "max_amount" = "amount" + "precision"

=====================  ====================    ====================================================================


minerals
--------

This table stores the mineral_id and name of the mineral. It also stores the real_mineral_id which is the default for alternative minerals. 
The trac wiki lists the minerals `<http://wiki.cs.rpi.edu/trac/metpetdb/wiki/Mineral>`_

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
mineral_id             Required (PK)           Unique id for the mineral
real_mineral_id        Required (FK)           for alternative minerals this is the default id, else it is 
                                               mineral_id. References minerals table itself. 
name                   Required (unique)       Name of the mineral corresponding to 
                                               mineral_id                                               
=====================  ====================    ====================================================================


mineral_relationships
---------------------

This table stores the relationship between minerals. Parent mineral, child mineral etc. The mineral ids are stored by referencing the “minerals” table. 

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
parent_mineral_id      Required (PK, FK)       Id of the parent mineral by referencing the minerals Table
child_mineral_id       Required(PK, FK)        Id of the child mineral by referencing the minerals table.

=====================  ====================    ====================================================================


element_mineral_types
---------------------

Chemical analyses of the minerals is at the core of quantitative metamorphic geochemistry and minerals consist of elements. 
This table correlates elements and minerals.
List of elements -  `<http://wiki.cs.rpi.edu/trac/metpetdb/wiki/Element>`_ 

list of Minerals - `<http://wiki.cs.rpi.edu/trac/metpetdb/wiki/Mineral>`_

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
element_id             Required (PK, FK)       References elements table
mineral_type_id        Required (PK, FK)       References minerals table

=====================  ====================    ====================================================================


oxide_mineral_types
-------------------

This table stores the oxides for a particular mineral.  Hence both the mineral_type_id and oxide_id are Primary keys. Hence, neither of them can be NULL and they are together unique. 

The list of oxides `<http://wiki.cs.rpi.edu/trac/metpetdb/wiki/Oxide>`_

The list of Minerals `<http://wiki.cs.rpi.edu/trac/metpetdb/wiki/Mineral>`_

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
oxide_id               Required (PK, FK)       References oxides table
mineral_type_id        Required (PK, FK)       References minerals table

=====================  ====================    ====================================================================


elements
--------

This table stores the information of the elements in the chemical data of the sample. 
The list of elements can be found here in the trac wiki `<http://wiki.cs.rpi.edu/trac/metpetdb/wiki/Element>`_

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
element_id             Required (PK)           Unique id for the element in the list of elements
name                   Required (unique)       Name of the element – upto 100 characters allowed
alternate_name         Required                Alternate name – upto 100 characters
symbol                 Required (unique)       Symbol upto 4 character length
atomic_number          Required                Is an integer
weight                 Optional                Atomic weight

=====================  ====================    ====================================================================


chemical_analysis_oxides
------------------------

This table stores the oxide information for a chemical_analysis_id. i.e both oxide_id and chemical_analysis_id are together unique (Primary Keys). It references the tables chemical_analyses and oxides. (correlation of chemical_analyses of a sample/subsample with the oxide)

List of oxides can be found `here <http://wiki.cs.rpi.edu/trac/metpetdb/wiki/Oxide>`_

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
chemical_analysis_id   Required (PK, FK)       The unique id by referencing the chemical_analyses table
oxide_id               Required (PK, FK)       The unique id for the oxide by referencing the oxide table. 
amount                 Required                Amount of the oxide present
precision              Optional                Indicates the precision of the value measured
precision_type         Optional                Type of precision in terms of absolute or relative. (‘ABS’, ‘REL’)
measurement_unit       Optional                Unit used to measure the amount of oxidet for a particular 
                                               chemical_analyses_id. (4 characters)
min_amount             Optional                When "precision" is specified AND "precision_type"= REL, then 
                                               "min_amount"= "amount" - "precision" X "amount" and 
                                               "max_amount" = "amount" + "precision" X "amount".
max_amount             Optional                when "precision" is specified AND "precision_type"= ABS, then 
                                               "min_amount"= "amount" - "precision"  and 
                                               "max_amount" = "amount" + "precision"

=====================  ====================    ==================================================================== 


oxides
------

This table stores the oxide information (oxide_id) for each element_id, which is referenced from the elements table. 
The list of oxides can be found in the trac wiki `<http://wiki.cs.rpi.edu/trac/metpetdb/wiki/Oxide>`

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ==================================================================== 
oxide_id               Required (PK)           Unique id of the oxide obtained by referencing the oxides table
element_id             Required (FK)           The element_id from the list of elements corresponding to the oxide
oxidation_state        Optional                Is an integer representing the oxidation state of the atom of the oxide
species                Unique                  Group of elements are a part of a species. Species name, list:
                                               Ce2O3, Al2O3, etc..
weight                 Optional                Molecular weight
cations_per_oxide      Optional                Number of cations per oxide stored as an integer.
conversion_factor      Required                This is the factor used to convert from element atomic weight 
                                               ("weight" in the element table) to a cation unit oxide weight
                                               ("weight" in the oxide table divided by "cations_per_oxide" in 
                                               the oxide table)   

=====================  ====================    ==================================================================== 


images
------

This table stores the image details along with rock descriptions and chemical_analyses. Every image is associated with one or more samples and one or more sub samples. Hence, it references the tables samples for sample_id and subsamples for subsample_id. 
The details about the image object can be obtained from the following wiki
`<http://wiki.cs.rpi.edu/trac/metpetdb/wiki/ImageObject>`_

inorder to allow searching for images with the sample_id or subsample_id , a unique index is created on these columns. 

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ==================================================================== 
image_id               Required (PK)           Every image in the system must have an image_id (INT)
checksum               Required                Checksum for the image has a 50 character limit.
version                Required                Version of the image. 
                                               More information http://wiki.cs.rpi.edu/trac/metpetdb/wiki/Versioning
sample_alias_id        Optional (unique        References samples table to associate a unique sample with the image
                       index, FK)  
subsample_id           Optional (unique        References subsamples table to associate a unique subsample with the image
                       index, FK)
image_format_id        Optional (FK)           References image_format table which specifies the format of 
                                               image (.jpg, .png etc) 
image_type_id          Required (FK)           References image_type table. List of image formats can be seen 
                                               `here <http://wiki.cs.rpi.edu/trac/metpetdb/wiki/Image#Types>`_
width                  Required                Width of the image must be >0
height                 Required                Height of the image must be >0
collector              Optional                The name of the collector of the image
description            Optional                Text description limited to 1024 characters regarding the image
scale                  Optional                This is mm measured along the rock surface shown in the image, 
                                               corresponding to the width of the image 
user_id                Required (FK)           References users table for the owner of the image
public_data            Required                Y/N – single character depending on whether the image is public/private.
checksum_64x64         Required                Checksums are actually file addresses for each image. When an image 
                                               is loaded, it is saved on the file system in three size in three files.
                                               Mobile one is the one shown on iphone 
checksum_half          Required
checksum_mobile        Optional                Checksum for the image in the mobile app. 
filename               Required                Name of the image file.                                                                                                                                                                                
=====================  ====================    ====================================================================


image_format
------------

Stores the type of image (TIFF, GIF, JPEG, BMP, PNG,) through the image_format_id.

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
image_format_id        Required (PK)           Type of image
name                   Required (unique)       Name of the image format – mime type image/x
=====================  ====================    ====================================================================  


image_type
----------

Stores the type of image from the list of acceptable image types. The list of acceptable image types in the various image formats are specified `here <http://wiki.cs.rpi.edu/trac/metpetdb/wiki/Image>`_ (check Types)

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
image_type_id          Required (PK)           Unique id for the type of image from the list of image types
image_type             Required                Name of the image type
abbreviation           Optional (unique)       Unique abbreviation for the image type
comments               Optional                Comments for the image type 

=====================  ====================    ==================================================================== 


regions
-------

This table stores the region_id and name where samples have been found. This is referenced by sample_regions to correlate the region_id and sample_id. This is done to facilitate search of samples based on regions. More information can be found 
`here <http://wiki.cs.rpi.edu/trac/metpetdb/wiki/Region>`_

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
region_id              Required (PK)           Unique id for the region from the list of regions
name                   Required (unique)       Name of the region 

=====================  ====================    ==================================================================== 



sample_regions
--------------

This table correlates the sample_id (for the samples found in a particular region) with region_id from the regions table. There can be many samples in a particular region or the same sample could be found in different regions. 

Sample table attributes can be found `here <http://wiki.cs.rpi.edu/trac/metpetdb/wiki/SampleObject>`_

List of regions can be found `here <http://wiki.cs.rpi.edu/trac/metpetdb/wiki/Region>`_

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
region_id              Required (PK, FK)       Unique id for the region obtained by referencing the regions table
name                   Required (PK, FK)       Name of the region as in the list of regions.

=====================  ====================    ====================================================================



metamorphic_regions
-------------------

Metamorphic regions are the polygons defined by the MetPetDB team and are different from Regions. 
The same Region may be named differently by different people whereas metamorphic_regions are unique in that respect.
The id is unique to each table. 
This table also stores the shape of the gis polygon as an additional column.

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
metamorphic_region_id  Required (PK)           Unique id of the metamorphic region
name                   Required (unique)       Name of the metamorphic region
description            Optional                Textual description of the metamorphic region
shape                  Optional                Column of gis polygon is added be calling the function 
                                               AddGeometrycolumn. i.e polygon of the location.
label_location         Optional                                                
=====================  ====================    ====================================================================


sample_metamorphic_regions
--------------------------

This table correlates the samples with the metamorphic regions by referencing the samples (for sample_id) and metamorphic_regions (for metamorphic_region_id). The 2 attributes are together unique.

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
sample_id              Required (PK, FK)       Unique sample id from the samples table
metamorphic_region_id  Required (PK, FK)       Corresponding unique metamorphic region id from the 
                                               metamorphic_regions table.

=====================  ====================    ====================================================================


metamorphic_grades
------------------

Metamorphic grades are one of the sample object attributes and this table stores the metamorphic_grade_id and name from the list of metamorphic grades `<http://wiki.cs.rpi.edu/trac/metpetdb/wiki/MetamorphicGrade>`_

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
metamorphic_grade_id   Required (PK)           Unique id for the metamorphic grades from the list of metamorphic 
                                               grades
name                   Required (unique)       Name of the metamorphic grade.

=====================  ====================    ====================================================================


sample_metamorphic_grades
-------------------------

This table correlates the samples with their metamorphic grades.

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
sample_id              Required (PK, FK)       Unique sample id from the samples table
metamorphic_grade_id   Required (PK, FK)       Corresponding unique metamorphic grade id from the 
                                               metamorphic_grades table. 

=====================  ====================    ====================================================================


georeference
------------

georeference describes detailed info (author, etc.) about a reference. But does not require that the reference be already stored in the reference table.  This way, detailed reference info can be stored in the db even if no sample references it yet.
This is important because people may upload (geo)references first and then the samples, or samples first and then georeferences.

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
georef_id              Required (PK)           Unique id for the file being referred
title                  Required                Title of the file being referred to
first_author           Required                Name of the first author
second_authors         Required                Name of the second author
journal_name           Required                Name of the journal in which the reference appears
full_text              Required                I suppose this stores the entire content of the reference?
reference_number       Optional

=====================  ====================    ====================================================================


sample_georeference
-------------------

sample_georeference is a by product of a join between sample_reference, reference and georeference. Whenever the georeference table is updated, this table is repopulated.. The text files are referenced via the reference_number.

reference
---------

This table stores the reference_id of the reference and the “name” of the file referenced. 
A reference is a known unique value (also called geo-reference in outside world.)
A reference is added only when someone adds a reference for a sample.

You can have a reference even if you do not have any details about that reference in the db. You just list the info. And it is stored in reference table, and the association between reference and samples is stored in the sample_reference table (a sample can have multiple references). 

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
reference_id           Required (PK)           Unique id of the reference
name                   Required                Generally the title of the file being referenced. 

=====================  ====================    ====================================================================


sample_reference
----------------

This table correlates the sample_id from the samples table with the reference_id from the reference table which stores “name” of the referenced file. 

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
sample_id              Required (PK, FK)       References sample_id from the samples table.
reference_id           Required (PK, FK)       References the corresponding reference_id from the reference table. 

=====================  ====================    ====================================================================


projects
--------

Users can share private data by starting projects, inviting members etc and to organize suites of public, private and published data. This table stores information about all the projects along with version.

More information about the Projects table can be found `here <http://wiki.cs.rpi.edu/trac/metpetdb/wiki/Projects>`_

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
project_id             Required (PK)           Unique id of the project
version                Required                It is the number of times that specific tuple has been modified 
                                               (used for concurrency issues). You read a tuple with its version info. 
                                               When trying to save it, you check whether the version has not changed 
                                               since you read it. If not, you can write the new update. Otherwise, 
                                               the update can fail. More information `here <http://wiki.cs.rpi.edu/trac/metpetdb/wiki/Versioning>`_
user_id                Required(FK, unique)    References the users table for the owner of the 
                                               project                 
name                   Required (unique)       Name of the project
description            Required                A textual description of the project. (upto 300 characters)                             
=====================  ====================    ====================================================================


project_members
---------------

This table correlates the user_id and the project. (i.e project_id)
A user can be part of many projects.

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
project_id             Required (PK, FK)       Referenced from the projects table.
user_id                Required (PK, FK)       Corresponding user_id referenced from the users table. 

=====================  ====================    ====================================================================


project_invites
---------------

This table stores the invites(invite_id, I suppose this gives the number of users associated with a project) for a particular project. 

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
invite_id              Required (PK)           Unique id of the invite to be a part of the project
project_id             Required (FK)           Id of the project referenced from the projects table
user_id                Required (FK)           ID of the project owner
action_timestamp       Required 
status                 Optional
=====================  ====================    ====================================================================


project_samples
---------------

This table correlates the project a sample is associated with by referencing the samples (sample_id) and the projects( project_id) tables. (no primary key)

=====================  ====================    ====================================================================
Attributes             Type                    Explanation     
=====================  ====================    ====================================================================
project_id             Required (FK)           Referenced from the projects table
sample_id              Required (FK)           Referenced from the samples table

=====================  ====================    ====================================================================