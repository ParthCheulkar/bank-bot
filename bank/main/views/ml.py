def verification(username):
    import face_recognition
    import numpy
    import cv2
    import time
    import os
    import glob
    import os
    

    print(f'ml->{username}')

    if not os.path.isdir(f"../bank/main/vid_ss/{username}/"):
        os.mkdir(f"../bank/main/vid_ss/{username}/")
    

    # list_of_files = glob.glob(f'media/ids/{username}_id.*') # * means all if need specific format then *.csv
    # latest_file_document = max(list_of_files, key=os.path.getctime)
    # print(latest_file_document)
    # print(list_of_files)
    list_of_files_1 = glob.glob(f'media/images/{username}.*') # * means all if need specific format then *.csv
    latest_fileimages = max(list_of_files_1, key=os.path.getctime)
    # print(f"1->{list_of_files_1}")
    # print(f"1->{latest_fileimages}")
    list_of_files_2 = glob.glob(f'media/videos/{username}_video.mp4') # * means all if need specific format then *.csv
    latest_file_videos = max(list_of_files_2, key=os.path.getctime)
    
    print(f"lisoffiles2->{list_of_files_2}")

    flag = 0
    print(f"flag->{flag}")
    path = 'media/videos/video.mp4'

    cap = cv2.VideoCapture(latest_file_videos)
    width = 1280
    heigh = 720

    i= 0
    while True:

        success, img = cap.read()

        if i == 10:
            break

        try:


            cv2.resize(img,(width,heigh))
            # cv2.imwrite('../ekyc/main/vid_ss/' + str(i) + '.jpeg', img)
            cv2.imwrite(f"../bank/main/vid_ss/{username}/" + str(i) + '.jpeg', img)
            i += 1


        except Exception as e:
            break



        cv2.waitKey(1)


    # imgtest = face_recognition.load_image_file(latest_file_document)

    # imgtest = cv2.cvtColor(imgtest , cv2.COLOR_BGR2RGB)
    # imgtest = cv2.resize(imgtest , (512,512))
    # face_loc_test = face_recognition.face_locations(imgtest)
    # encodingtest = face_recognition.face_encodings(imgtest)
    # print(flag)
    # if not len(face_loc_test):
    #     flag = 1

    # print(flag)

    img = face_recognition.load_image_file(latest_fileimages)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img , (512,512))
    face_loc = face_recognition.face_locations(img)
    encoding1 = face_recognition.face_encodings(img)
    if not len(face_loc):
        flag = 1
    # print(flag)




    if flag == 0:
            path = f"../bank/main/vid_ss/{username}/"

            n = (len(os.listdir(path)))
            # print(n)
            values = []
            values1 = []
            for i in range(n):
                img = face_recognition.load_image_file(f"../bank/main/vid_ss/{username}/"+str(i)+'.jpeg')
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                face_loc = face_recognition.face_locations(img)
                if not len(face_loc):
                    print("Not reading")
                    continue
                encoding= face_recognition.face_encodings(img)
                # results = face_recognition.compare_faces([encoding[0]],encodingtest[0])

                results1 = face_recognition.compare_faces([encoding[0]],encoding1[0])
                # print(results)
                # values.append(results)
                values1.append(results1)
                # print(values)
                # print(values1)


            # c=0
            # ctc=0
            # cfc=0
            # if len(values)>3:
            #     for v in values:
            #         a = v[0]

            #         if a == True:
            #             ctc+=1
            #             c+=1
            #         else:
            #             cfc+=1


            #     if ctc>cfc:
            #         flag =0
            #     else:
            #         flag=1



            # else:
            #     flag = 1

            d=0
            dtd=0
            dfd=0
            if len(values1)>3:
                for v in values1:
                    a = v[0]

                    if a == True:
                        dtd+=1
                        d+=1
                    else:
                        dfd+=1


                if dtd>dfd:
                    flag =0
                else:
                    flag=1



            else:
                flag = 1


    else:
        pass
    print(values)
    print(values1)
    print(f"finalFlag->{flag}")
    return flag