import os
import time
# import logging
import requests
import json
import cv2

size_limit = 4*1024*1024
resolution_limit = 3072*2400


# ----------------  GLOBALS: configuration - change these for your environment -------------------------
LOCAL_URL = "http://localhost:8000"
SERVER_URL = "http://jnresearch.com"  # LOCAL_URL
PREDICT_ONE_URL = SERVER_URL + '/do_ocr'
# ----------------------------------------------------------------------------------------------------------


def test():
    response = requests.get(SERVER_URL)
    print(response.text)
    return


def validate_size(fn):
    file_size = os.path.getsize(fn)
    if file_size >= size_limit:
        code = -1
        msg = "Size limit exceeded, limit = %d, given size = %d" % (size_limit, file_size)
    else:
        code = 0
        msg = "Success"
    return code, msg


def validate_resolution(fn):
    img = cv2.imread(fn)
    h = img.shape[0]
    w = img.shape[1]

    if h*w >= resolution_limit:
        code = -1
        msg = "Unsupported Resolution"
    else:
        code = 0
        msg = "Success"

    return code, msg


def validate_input(fn):
    code, msg = validate_size(fn)
    if code == 0:
        code, msg = validate_resolution(fn)
    return code, msg


def upload_image(img_file):
    """ post image and return the response """
    t1 = time.time()
    code, msg = validate_input(img_file)

    if code == -1:
        t2 = time.time()
        result = {
            "code": code,
            "msg": msg,
            "data": None,
            "elapsed_time": t2 - t1,
        }
        return result

    content_type = 'image/png'
    img = open(img_file, 'rb')  # .read()
    fn = os.path.split(img_file)[-1]
    files = {'file': (fn, img, content_type)}
    response = requests.post(PREDICT_ONE_URL, files=files)
    result = json.loads(response.text)
    result["elapsed_time"] = time.time() - t1
    return result


def write_to_json(data, json_name):
    """
    Writes the data to json file
    :param data: data to be written to json file
    :param json_name: json file name
    :return: None
    """
    with open(json_name, "w") as f:
        json.dump(data, f)
        msg = "JSON output saved at: %s" % json_name
        print(msg)
        # logging.info(msg)
    return


def visualize_boxes(image, boxes, fn=None, thick=1, color=(255, 0, 0)):
    # print("boxes = ", boxes)
    for i, box in enumerate(boxes):
        coord1 = (int(box[0]), int(box[1]))
        coord2 = (int(box[2]), int(box[3]))
        image = cv2.rectangle(image, coord1, coord2, color, thick)
    if fn is not None:
        print("Writing file to: ", fn)
        cv2.imwrite(fn, image)
    return image
