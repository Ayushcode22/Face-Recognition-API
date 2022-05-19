
from fastapi import FastAPI, File, UploadFile, Form
from fastapi import Path
import psycopg2
import sys
from zipfile import ZipFile
import face_recognition
from PIL import Image
from PIL.ExifTags import TAGS
from io import BytesIO
import numpy

app = FastAPI()



@app.post("/add_face/")
async def add_face(file: UploadFile = File(..., description="An image file having a single human face.")):
   # TODO: Implement the logic for saving the face details in DB
   
	con = psycopg2.connect(
		host ="127.0.0.1",
		database="postgres",
		user="admin",
		password = "admin"
	)
	
	cur = con.cursor()
	
	cur.execute("CREATE TABLE IF NOT EXISTS images(id SERIAL PRIMARY KEY, photo BYTEA,metadata VARCHAR);")
	File = open(file.filename,"rb")	
	BinaryData=File.read();
	binary = psycopg2.Binary(BinaryData)
	File.close;
	s = ""
	im = Image.open(file.filename)
	if im._getexif() is not None:
		for tag, value in im._getexif().items():
			if tag in TAGS:
				s = s + str(TAGS[tag]) + ": " + str(value) + " "
	
	j = file.filename.find(".")
	print(j)
	file.filename = file.filename[0:j]
	metadata = "Name: " + file.filename + "; " + s
	cur.execute("INSERT INTO images(photo,metadata) VALUES (%s,%s)",(binary,metadata));


	con.commit();
	cur.close()
	con.close()
	   
	   
	return {"file_name":file.filename}
	
	
	
@app.post("/add_faces_in_bulk/")
async def add_faces_in_bulk(file: UploadFile = File(..., description="A ZIP file containing multiple face images.")):
# TODO: Implement the logic for saving the face details in DB
    con = psycopg2.connect(
        host ="127.0.0.1",
        database="postgres",
        user="admin",
        password = "admin"
    )
    cur = con.cursor()
    zipObj = ZipFile(file.filename)
    file_objects = [zipObj.read(item) for item in zipObj.namelist()]


    files = zipObj.namelist();

    for l in range(1,len(files)):
        i = files[l].find("/")
        j = files[l].find(".")
        files[l] = files[l][i+1:j]

    length_fo = len(file_objects)
    print(length_fo)


    for i in range(1,length_fo):
        st=''
        binary = psycopg2.Binary(file_objects[i])
        dataEnc = BytesIO(file_objects[i])
        img = Image.open(dataEnc)
        if(img.getexif() is not None):
            for tagname,value in img.getexif().items():
                if(tagname in TAGS):
                    st = st + str(TAGS[tagname])+ ": "+ str(value)+" "
    metadata = "Name: " + files[i] + "; "+st
    cur.execute("INSERT INTO images(photo,metadata) VALUES (%s,%s)",(binary,metadata));

    con.commit();
    cur.close()
    con.close()
    return {"file": file.filename}

	
	
	
@app.post("/get_face_info/")
async def get_face_info(face_id: int):
	# TODO: Implement the logic for retrieving the details of a face record from DB.
	con = psycopg2.connect(
		host ="127.0.0.1",
		database="postgres",
		user="admin",
		password = "admin"
	)
	
	cur = con.cursor()
	
	cur.execute("SELECT metadata FROM images WHERE id=%s",[face_id])
	name =cur.fetchone() 
	
	print(name);
	
	con.commit();
	cur.close()
	con.close()
	
	return {"name": name}
	
	
	
@app.post("/search_faces/")
async def search_faces(kk: str,file: UploadFile =File(..., description="An image file, possible containing multiple human faces.")):
	
	img_test = face_recognition.load_image_file(file.filename)
	test_img_encoding = face_recognition.face_encodings(img_test)
	
	k = int(kk)
	print(k)
	con = psycopg2.connect(
		host ="127.0.0.1",
		database="postgres",
		user="admin",
		password = "admin"
	)
	cur = con.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS images(id SERIAL PRIMARY KEY, photo BYTEA,metadata VARCHAR);")
	postgreSQL_select_Query = "select * from images"
	cur.execute(postgreSQL_select_Query)
	Images = cur.fetchall()
	
	Dict = {}
	
	for row in Images:
		binarydata = row[1]
		fout = open('img.jpg','wb')
		fout.write(binarydata)
		known_image = face_recognition.load_image_file("img.jpg")
		known_image_encoding = face_recognition.face_encodings(known_image)
		
		for img in test_img_encoding :
			face_distance = face_recognition.face_distance(known_image_encoding,img);
			for i, face_distance in enumerate(face_distance):
				if(face_distance<=0.6):
					Dict[row[0]]=face_distance
	#print(Dict)
	
	imgID=[]
	
	d=sorted(Dict.items(), key = lambda kv:(kv[1], kv[0]))
	print(d)
	for i in range(0,k):
		if(d[i][0] in imgID):
			continue
		else:
			imgID.append(d[i][0])
		
	print(imgID)	
	con.commit();
	cur.close()
	con.close()
	
	return {"ImageIdMatched":imgID}
