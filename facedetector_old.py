import cv2
import dlib

def detectFaces(name):
    detector = dlib.get_frontal_face_detector()
    suitable_frames = list()
    # Create an object to read
    # from camera
    video = cv2.VideoCapture(name)

    # We need to check if camera
    # is opened previously or not
    if (video.isOpened() == False):
        print("Error reading video file")

    # We need to set resolutions.
    # so, convert them from float to integer.
    frame_width = int(video.get(3))
    frame_height = int(video.get(4))

    size = (frame_width, frame_height)
    print(size)

    # Below VideoWriter object will create
    # a frame of above defined The output
    # is stored in 'filename.avi' file.
    frame_num=0
    while (True):
        ret, frame = video.read()
        frame_num += 1
        print(frame_num)
        if ret == True:

            location = detector.detect_faces(frame)
            if len(location) == 1:
                for face in location:
                    x, y, width, height = face['box']
                    print(width, height)
                    print((width*height) / (frame_width*frame_height))
                    if (width*height) / (frame_width*frame_height) > 0.08:
                        suitable_frames.append(frame_num)
                        print("frame:" + str(frame_num))
                        
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break


    video.release()

    # Closes all the frames
    cv2.destroyAllWindows()

    return suitable_frames