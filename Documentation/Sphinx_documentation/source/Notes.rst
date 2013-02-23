.. _Notes:


***************
End Notes
***************

Details of the possible up gradations to the schema can be found `here <https://github.com/metpetdb/metpetdb-py/blob/master/database/MetPetDBSchemav1.0.pdf>`_

The current `schema <https://github.com/metpetdb/metpetdb/tree/master/mpdb-server/schema>`_ may be slightly outdated and will be updated shortly. 

Some of the tables not discussed in this report but are there in the schema:
Table Name: xray_image
Probably like a subclass of images. For each image created, an xray_image is created referencing the actual image. Not sure about what each attribute holds. 

Table Name: grids, image_on_grid, geometry_columns, sample_ref_sys (not sure about their use)

**Empty tables:**

* Admin_users
* Role_changes
* Users_roles
* Image_comments (may be used later)
* Image_reference (may be used later)




