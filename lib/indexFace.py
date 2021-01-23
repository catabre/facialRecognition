
import boto3
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="dt_proofreader"
)

mycursor = mydb.cursor()


def add_faces_to_collection(bucket,photo,collection_id, maxFaces, personName):

    client=boto3.client('rekognition')

    response=client.index_faces(CollectionId=collection_id,
                                Image={'S3Object':{'Bucket':bucket,'Name':photo}},
                                #ExternalImageId=photo,
                                MaxFaces=maxFaces,
                                QualityFilter="AUTO",
                                DetectionAttributes=['ALL'])

    print ('Results for ' + photo) 	
    print('Faces indexed:')
    faceIds = []  						
    for faceRecord in response['FaceRecords']:
         print('  Face ID: ' + faceRecord['Face']['FaceId'])
         print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))
         faceId = faceRecord['Face']['FaceId']
         #faceIds.append(faceId)
         imageId = faceRecord['Face']['ImageId']
         imageURL = photo
         left = str(faceRecord['Face']['BoundingBox']['Left'])
         top = str(faceRecord['Face']['BoundingBox']['Top'])
         height = str(faceRecord['Face']['BoundingBox']['Height'])
         width =  str(faceRecord['Face']['BoundingBox']['Width'])
         #### Save to Datastore ##### 
         sql = "INSERT INTO face (faceId, imageId, imageURL, personName, `left`, `top`, `height`, `width`) VALUES (%s, %s, %s,%s, %s,%s,%s,%s)"
         val = (faceId, imageId, imageURL, personName, left, top, height, width)
         print(val)
         #val = (faceId, imageId, imageURL, personName)
 
         try:
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
            faceIds.append(faceId)
         except (mysql.connector.IntegrityError, mysql.connector.DataError) as e:
            print(e)

    print('Faces not indexed:')
    for unindexedFace in response['UnindexedFaces']:
        print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
        print(' Reasons:')
        for reason in unindexedFace['Reasons']:
            print('   ' + reason)
    return len(response['FaceRecords']), faceIds

def search_face_in_collection(face_id,collection_id):
    threshold = 90
    max_faces=2
    client=boto3.client('rekognition')

  
    response=client.search_faces(CollectionId=collection_id,
                                FaceId=face_id,
                                FaceMatchThreshold=threshold,
                                MaxFaces=max_faces)

                        
    face_matches=response['FaceMatches']
    faceIds = [] 
    for match in face_matches:
            print ('FaceId:' + match['Face']['FaceId'])
            print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
            faceIds.append(match['Face']['FaceId'])
           
    return len(face_matches), faceIds

def IndexAndSearchFace(searchFace, maxFaces, personName, prefix):
    bucket='gktrainimage'
    collection_id='firstCollection'
    
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(bucket)
    
    for object_summary in my_bucket.objects.filter(Prefix = prefix): ##Prefix="/folderName"
        photo = object_summary.key
        print('Image URL: ' + photo)
        if not photo.lower().endswith(('.png', '.jpg', '.jpeg')):
           continue
        indexed_faces_count, faceIds = add_faces_to_collection(bucket, photo, collection_id, maxFaces, personName)
        print("Faces indexed count: " + str(indexed_faces_count))
        if searchFace: 
           for face_id in faceIds: 
                faces_count, matchingFaceIds = search_face_in_collection(face_id, collection_id)

                if matchingFaceIds == []:
                    continue
                
                for matchingFaceId in matchingFaceIds: 
                    sql = "select `personName` from `face` where faceId = '{0}' ".format(matchingFaceId)
                    mycursor.execute(sql)
                    pName = mycursor.fetchone()
                    print(pName)
                    if pName is not None and pName[0] is not None:
                       pName = pName[0]
                       print('PersonName Matched :: ' + pName)
                       if pName != 'UNKNOWN':
                           break

                sql = "UPDATE face SET personName = %s  WHERE faceId = %s "
                val = (pName , face_id )
                mycursor.execute(sql, val)
                mydb.commit()
                print(mycursor.rowcount, "record(s) affected")
       # break

def indexAllPersons():
 IndexAndSearchFace(False, 1, 'Anand', 'TrainImages/Anand')
 IndexAndSearchFace(False, 1, 'Bedore', 'TrainImages/Bedore')
 IndexAndSearchFace(False, 1, 'Bjarke', 'TrainImages/Bjarke')
 IndexAndSearchFace(False, 1, 'Dennis_Lardon', 'TrainImages/Dennis_Lardon')
 IndexAndSearchFace(False, 1, 'Eichinger', 'TrainImages/Eichinger')
 IndexAndSearchFace(False, 1, 'Evans', 'TrainImages/Evans')
 IndexAndSearchFace(False, 1, 'Fay', 'TrainImages/Fay')
 IndexAndSearchFace(False, 1, 'Gary_Kelly', 'TrainImages/Gary_Kelly')
 IndexAndSearchFace(False, 1, 'Gaurav', 'TrainImages/Gaurav')
 IndexAndSearchFace(False, 1, 'Grenier', 'TrainImages/Grenier')
 IndexAndSearchFace(False, 1, 'Harbin', 'TrainImages/Harbin')
 IndexAndSearchFace(False, 1, 'Harding', 'TrainImages/Harding')
 IndexAndSearchFace(False, 1, 'Hargrove', 'TrainImages/Hargrove')
 IndexAndSearchFace(False, 1, 'Harler', 'TrainImages/Harler')
 IndexAndSearchFace(False, 1, 'Jones', 'TrainImages/Jones')
 IndexAndSearchFace(False, 1, 'King', 'TrainImages/King')
 IndexAndSearchFace(False, 1, 'Labrie', 'TrainImages/Labrie')
 IndexAndSearchFace(False, 1, 'Mark_Wolfe', 'TrainImages/Mark_Wolfe')
 IndexAndSearchFace(False, 1, 'Martin', 'TrainImages/Martin')
 IndexAndSearchFace(False, 1, 'McMrtry', 'TrainImages/McMrtry')
 IndexAndSearchFace(False, 1, 'Mike_Kapsa', 'TrainImages/Mike_Kapsa')
 IndexAndSearchFace(False, 1, 'Montgomery', 'TrainImages/Montgomery')
 IndexAndSearchFace(False, 1, 'Mossuto', 'TrainImages/Mossuto')
 IndexAndSearchFace(False, 1, 'NoName2', 'TrainImages/NoName2')
 IndexAndSearchFace(False, 1, 'Perez', 'TrainImages/Perez')
 IndexAndSearchFace(False, 1, 'Perrino', 'TrainImages/Perrino')
 IndexAndSearchFace(False, 1, 'Peters', 'TrainImages/Peters')
 IndexAndSearchFace(False, 1, 'Phillips', 'TrainImages/Phillips')
 IndexAndSearchFace(False, 1, 'Rabinowitz', 'TrainImages/Rabinowitz')
 IndexAndSearchFace(False, 1, 'Reid', 'TrainImages/Reid')
 IndexAndSearchFace(False, 1, 'Richardson', 'TrainImages/Richardson')
 IndexAndSearchFace(False, 1, 'RIOS', 'TrainImages/RIOS')
 IndexAndSearchFace(False, 1, 'Romano', 'TrainImages/Romano')
 IndexAndSearchFace(False, 1, 'Ronny_Moon', 'TrainImages/Ronny_Moon')
 IndexAndSearchFace(False, 1, 'Ross', 'TrainImages/Ross')
 IndexAndSearchFace(False, 1, 'Rupprecht', 'TrainImages/Rupprecht')
 IndexAndSearchFace(False, 1, 'Rutherford', 'TrainImages/Rutherford')
 IndexAndSearchFace(False, 1, 'Sam_Iannuzzi', 'TrainImages/Sam_Iannuzzi')
 IndexAndSearchFace(False, 1, 'Sarah_Schulte', 'TrainImages/Sarah_Schulte')
 IndexAndSearchFace(False, 1, 'Schumacher', 'TrainImages/Schumacher')
 IndexAndSearchFace(False, 1, 'Singh', 'TrainImages/Singh')
 IndexAndSearchFace(False, 1, 'Stank', 'TrainImages/Stank')
 IndexAndSearchFace(False, 1, 'Stewart', 'TrainImages/Stewart')
 IndexAndSearchFace(False, 1, 'Swati', 'TrainImages/Swati')
 IndexAndSearchFace(False, 1, 'Tonda_Montague', 'TrainImages/Tonda_Montague')
 IndexAndSearchFace(False, 1, 'Toombs', 'TrainImages/Toombs')
 IndexAndSearchFace(False, 1, 'Turneabe_Connelly', 'TrainImages/Turneabe_Connelly')
 IndexAndSearchFace(False, 1, 'Turner', 'TrainImages/Turner')
 IndexAndSearchFace(False, 1, 'Vargo', 'TrainImages/Vargo')
 IndexAndSearchFace(False, 1, 'Weight', 'TrainImages/Weight')
 IndexAndSearchFace(False, 1, 'Whitfield', 'TrainImages/Whitfield')


 
if __name__ == "__main__":
    #indexAllPersons()   
    IndexAndSearchFace( True, 7, 'UNKNOWN', 'TestImages/')
    #IndexAndSearchFace(False, 1, 'Anand_Kishore', 'TrainImages/Anand')
