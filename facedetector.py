import cv2
import dlib

def detectFaces(name):
    detector = dlib.get_frontal_face_detector()
    suitable_frames = list()
    # Create an object to read
    # from camera
    video = cv2.VideoCapture("resized_" + name)

    # We need to check if camera
    # is opened previously or not
    if (video.isOpened() == False):
        print("Error reading video file")

    # We need to set resolutions.
    # so, convert them from float to integer.
    frame_width = int(video.get(3))
    frame_height = int(video.get(4))

    # Below VideoWriter object will create
    # a frame of above defined The output
    # is stored in 'filename.avi' file.
    frame_num=0
    while (True):
        ret, frame = video.read()
        frame_num += 1
        if ret == True:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = detector(gray)
            print("length ", len(faces))

            if len(faces) == 1:            
                for rect in faces:
                        x, y, width, height = rect.left(), rect.top(), rect.width(), rect.height()
                        cv2.rectangle(frame, (x, y), (x+width, y+height), (255, 0, 0), 2)  # Blue color, 2px rectangle thickness
                        
                        # calculate percentage of width available for vertical video:
                        width_percentage = ((9 / 16) * frame_height ) / frame_width
                        
                        # if the face takes up more than 60% of the vertical frame its good
                        if width_percentage * 0.4 < (width) / (frame_width) < width_percentage:
                            suitable_frames.append(frame_num)
            
            cv2.imshow('Face Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break


    video.release()

    # Closes all the frames
    cv2.destroyAllWindows()

    return suitable_frames

def verifyFaces():
    backend = 'retinaface'
    video = cv2.VideoCapture('./output/output_0')

    obj = DeepFace.verify(img1_path = "img1.jpg", img2_path = "img2.jpg", detector_backend = backends[4])

    return

if __name__ == "__main__":
    verifyFaces()