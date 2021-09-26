import cv2

from OCR_client import upload_image, visualize_boxes
import os

path = "samples"
dir_list = os.listdir(path)
print("Files in '", path, "' :")
print(dir_list)

for file in dir_list:
    print("file = ", file)
    fn = os.path.join(path, file)
    data = upload_image(fn)
    image = cv2.imread(fn)
    print("Time taken: ", data["elapsed_time"])

    if data["code"] == 0:
        #     # print(data["data"].keys())
        for info in data["data"]["words_info"]:
            print(info)

        boxes = []  # list of all boxes
        for winfo in data["data"]["chars_info"]:
            #print(winfo)
            #print(winfo)
            boxes.append(winfo["box"])
        visualize_boxes(image.copy(), boxes, os.path.join("/", "tmp", "words_" + file))

        # boxes = []  # list of all boxes
        # for info in data["data"]["words_info"]:
        #     print(winfo)
        #     boxes.append(info["box"])
        # visualize_boxes(image.copy(), boxes, os.path.join("/", "tmp", "chars_" + file))

    else:
        print("Some error, message = ", data["msg"])
