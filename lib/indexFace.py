
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
    print ('Matching faces')
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
                
                sql = "select `personName` from `face` where faceId = '{0}' ".format(matchingFaceIds[0])
                mycursor.execute(sql)
                pName = mycursor.fetchone()[0]
                print('PersonName Matched :: ' + pName)

                sql = "UPDATE face SET personName = %s  WHERE faceId = %s "
                val = (pName , face_id )
                mycursor.execute(sql, val)
                mydb.commit()
                print(mycursor.rowcount, "record(s) affected")
       # break

 
if __name__ == "__main__":
    IndexAndSearchFace( True, 5, 'UNKNOWN', 'Test/')
    #IndexAndSearchFace(False, 1, 'Dennis_Lardon', 'Dennis_Lardon/')
