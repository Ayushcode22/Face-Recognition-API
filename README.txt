Submitter name: Ayush Tirpude

Roll No.: 2019csb1078

Course: CS305

=================================

1. What does this program do

 We can use this program to add images to Postgresql database. We can add a single image or compress and create a zip file containing images and pass 
 that zip file to store images inside. We can find metadata for each image in database and also we can search a particular image in the database, 
 which will give k(through user input) images which have similarity with the image being searched. 


2. A description of how this program works (i.e. its logic)

 This program is made using python language. Database used is Postgreql.I have created connection to the postgresql database using psycopg2. For 
 inserting a single image into the database we need to run add_face() which will take input file as an image and will add this image as binary data 
 in database with an image ID and metadata(if present). For inserting images in bulk we need to run add_face_in_bulk().This will use zipfile library 
 of python to read files inside zip.After reading we then store all images stored in zip to database. Each photo having unique ID.
 
 To search faces in database we need to use search_face(). This will take a test image as input. This image is encoded using python library : 
 face_recognition. After encoding this test image we iterate through the database row by row. The image present in that row is encoded again and 
 distance is calculated between the test image and the input image. If it is less than confidenceValue then its image id with its distance is added 
 to a dictionary. The dictionary is sorted according to values of distance from test image and then top-k imageId are appended in a list and 
 returned. 

 To get info of image we need to use get_face_info(). In this function we give ImageID as input. this id is searched in the database and 
 corresponding metadata is returned using select querry.


3. How to compile and run this program

for unit-testing use the file test_index.py. and write the command :  coverage run -m pytest test_index.py
for testing on fastapi, first run : uvicorn index:app --reload
Then open : http://127.0.0.1:8000/docs#/  to open swagger UI.
You can use all the functions there.
