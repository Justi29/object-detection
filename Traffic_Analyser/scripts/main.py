import cv2
import numpy as np
import csv
import os
import datetime
import random
from pathlib import Path


class Traffic_Analyser:

    def __init__(self, video_path):  # constructor takes path to the video as an argument
        self.FONT = cv2.FONT_HERSHEY_SIMPLEX
        self.COLOUR = (50, 200, 0)
        self.max_frames = 10  # for testing
        self.video_path = video_path
        self.dir_path = os.path.dirname(self.video_path)  # directory path of the video
        self.output_video_file = ""
        self.output_csv_file = ""
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.parent_directory = str(Path(self.current_directory).parent)
        self.yolo_weights = self.current_directory + "/yolov3_custom_best.weights"  # path to the custom YOLO weights
        self.yolo_cfg = self.current_directory + "/yolov3_custom.cfg"  # path to the custom YOLO config
        self.class_names = self.current_directory + "/obj.names"  # path to the possible classes/object names

    def video_analyse(self):

        # creating filename of output video
        t = datetime.datetime.now()  # current time for unique file names
        self.current_time = t.strftime("%H-%M_%d-%b")
        self.random = random.randint(10, 99)
        self.output_video_file = self.parent_directory + "/" + self.current_time + "_" + os.path.split(self.video_path)[1].split(".")[0] + ".avi"

        # loading the Deep Learning network
        net = cv2.dnn.readNet(self.yolo_weights, self.yolo_cfg)
        # getting all possible classes
        with open(self.class_names, "r") as f:
            classes = [line.strip() for line in f.readlines()]

        layers_names = net.getLayerNames()
        layers_output = [layers_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        video = cv2.VideoCapture(self.video_path)

        vid_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))  # getting video source width and height
        vid_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        result = cv2.VideoWriter(self.output_video_file,
                                 cv2.VideoWriter_fourcc(*'MJPG'),
                                 10, (vid_width, vid_height))

        # instantiate lists for each class
        self.total_objects = []
        self.total_people = []
        self.total_two_wheelers = []
        self.total_trams = []
        self.total_trucks = []
        self.total_cars = []
        # self.total_traffic_lights = []
        # self.total_traffic_signs = []

        self.frame = 0
        success, img = video.read()
        while success:
            self.frame += 1
            # no. of objects of each category in one frame
            objects_number = 0
            people_number = 0
            trams_number = 0
            trucks_number = 0
            two_wheelers_number = 0
            cars_number = 0
            # trlights_number = 0
            # trsigns_number = 0

            # analysing only one of two consecutive frames to improve performance
            if self.frame % 2 == 1 and self.frame != 1:
                success, img = video.read()
            if self.frame % 2 == 1 and success:
# -------------------------------------------------------------------------------------------------------------
                blob_results = cv2.dnn.blobFromImage(img, 0.00392, (320, 320), (0, 0, 0), True, False)
                img_height, img_width, img_channels = img.shape
                net.setInput(blob_results)
                outs = net.forward(layers_output)

                class_ids = []
                confidences = []
                boxes = []

                # detecting through network layers
                for out in outs:
                    for detection in out:
                        scores = detection[5:]
                        class_id = np.argmax(scores)
                        confidence = scores[class_id]
                        # passing objects only if the confidence level is higher then 50%
                        if confidence > 0.5:
                            # Detected object dimensions
                            center_x = int(detection[0] * img_width)
                            center_y = int(detection[1] * img_height)
                            width = int(detection[2] * img_width)
                            height = int(detection[3] * img_height)

                            #  Rectangle
                            x = int(center_x - width / 2)
                            y = int(center_y - height / 2)

                            boxes.append([x, y, width, height])
                            confidences.append(float(confidence))
                            class_ids.append(class_id)

                indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.6, 0.4)
# ------------------------------------------------------------------------------------------------------
            else:
                success, img = video.read()

            if success:
                for i in indexes:
                    i = int(i)

                    # drawing boxes and counting objects based on the previous frame analysis
                    if class_ids[i] in [0, 1, 2, 3, 4]:  # ids of analysed classes (person,two-wheeler,
                                                         # train or tram, bus or truck)

                        objects_number += 1
                        x, y, width, height = boxes[i]
                        label = classes[class_ids[i]].upper()
                        conf = str(round(confidences[i] * 100, 1)) + "%"
                        cv2.rectangle(img, (x, y), (x + width, y + height), self.COLOUR, 2)
                        cv2.putText(img, label, (x + 5, y + 15), self.FONT, 0.5, self.COLOUR, 1)
                        cv2.putText(img, conf, (x + 5, y + height - 5), self.FONT, 0.5, self.COLOUR, 1)

                    # counting objects per category
                    if class_ids[i] == 0:  # person
                        people_number += 1
                    if class_ids[i] == 1:  # two-wheeler
                        two_wheelers_number += 1
                    if class_ids == 2:  # train or tram
                        trams_number += 1
                    if class_ids == 3:  # bus or truck
                        trucks_number += 1
                    if class_ids[i] == 4:  # car
                        cars_number += 1

                self.total_objects.append(objects_number)
                self.total_people.append(people_number)
                self.total_two_wheelers.append(two_wheelers_number)
                self.total_trams.append(trams_number)
                self.total_trucks.append(trucks_number)
                self.total_cars.append(cars_number)

                cv2.putText(img, str(self.frame), (20, 20), self.FONT, 0.5, self.COLOUR, 2)
                result.write(img)
                print(".", end='')

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        video.release()
        result.release()
        cv2.destroyAllWindows()

    # Function responsible for timestamp counting and saving the results to CSV file
    def write_timestamps(self):

        # creating filename for analysis results
        self.output_csv_file =self.current_time + "_" + os.path.split(self.video_path)[1].split(".")[
            0] + ".csv"
        cameraCapture = cv2.VideoCapture(self.video_path)

        success, frame = cameraCapture.read()
        fps = cameraCapture.get(cv2.CAP_PROP_FPS)

        total_timestamp = []

        count = 0
        # counting all timestamps
        while success:
            success, frame = cameraCapture.read()
            count += 1
            time_stamp = count / fps
            total_timestamp.append(time_stamp)

        cv2.destroyAllWindows()
        cameraCapture.release()

        # saving the results
        with open(self.parent_directory + "/" + self.output_csv_file, 'w', newline='') as file:
            print(len(total_timestamp))
            print(len(self.total_objects))
            print(len(self.total_people))
            print(len(self.total_two_wheelers))
            print(len(self.total_trams))
            print(len(self.total_trucks))
            print(len(self.total_cars))
            writer = csv.writer(file)
            writer.writerow(["timestamp", "detected objects", "people", "two-wheelers",
                             "trains or trams", "buses or trucks", "cars"])
            for i in range(len(self.total_objects)):
                writer = csv.writer(file)
                writer.writerow([total_timestamp[i], self.total_objects[i], self.total_people[i],
                                 self.total_two_wheelers[i], self.total_trams[i], self.total_trucks[i], self.total_cars[i]])
