import sys
import time
from datetime import datetime
import cv2
import re
import requests
import subprocess
import random
import os
import dotenv
import logging

from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
from sense_hat import SenseHat, ACTION_PRESSED
from store import update_realtime, update_bird_sightings, update_cat_sightings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("twitchr")
IMAGES_DIR = 'images/'


def _make_twitchr_request(data) -> None:
    logger.info("making api request...")
    requests.post(
        os.environ['TWITCHR_APP_URL'] + "api/send-update/",
        headers={'x-api-key': os.environ["TWITCHR_API_KEY"]},
        data=data
    )


def make_play_sound_request() -> None:
    logger.info("making request to play sound...")
    _make_twitchr_request(data={
        "type": "play_sound",
        "sound": random.choice(["birds", "insect", "water"])
    })


def pushed_middle(event):
  # play sound if middle button pressed
    if event.action == ACTION_PRESSED:
        logger.info("button pressed")
        make_play_sound_request()


def get_device_data(sensehat: SenseHat) -> dict:
    celcius = round(sensehat.temperature, 1)
    # calibrate the temperature
    # following https://github.com/initialstate/wunderground-sensehat/wiki/Part-3.-Sense-HAT-Temperature-Correction
    cpu_temp = subprocess.check_output(
        "vcgencmd measure_temp", shell=True).decode('utf-8')
    cpu_temp = float(re.findall(r'\d+', cpu_temp)[0])
    temp_calibrated = round(celcius - ((cpu_temp - celcius) / 2), 1)
    fahrenheit = round(1.8 * temp_calibrated + 32, 1)
    humidity = round(sensehat.humidity)
    pressure = round(sensehat.pressure)
    return {
        "celcius": temp_calibrated,
        "fahrenheit": fahrenheit,
        "humidity": humidity,
        "pressure": pressure,
    }


def run() -> None:
    dotenv.load_dotenv()
    bird_timer = datetime.now()

    # setup sensehat
    sense = SenseHat()
    sense.clear()
    sense.stick.direction_middle = pushed_middle

    # set up the camera
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # create the detector
    base_options = core.BaseOptions(file_name='lite-model-detection.tflite')
    detection_options = processor.DetectionOptions(max_results=2)
    options = vision.ObjectDetectorOptions(
        base_options=base_options, detection_options=detection_options)
    base_detector = vision.ObjectDetector.create_from_options(options)

    # create the classifier
    base_options = core.BaseOptions(file_name='lite-model-birds.tflite')
    classification_options = processor.ClassificationOptions(max_results=2)
    options = vision.ImageClassifierOptions(
        base_options=base_options, classification_options=classification_options)
    classifier = vision.ImageClassifier.create_from_options(options)

    # Capture Image on a loop
    while camera.isOpened():
        # take photo and save locally
        logger.info("taking snapshot...")
        ran_successful, image = camera.read()
        current_time = datetime.now()
        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
        snapshot_str = 'snapshot{}.jpg'.format(timestamp)
        status = 'Nothing Spotted'
        cv2.imwrite(IMAGES_DIR + snapshot_str, image)

        if not ran_successful:
            sys.exit(
                'Image could not be captured.'
            )

        # create a TensorImage object from captured image
        current_image_ref = snapshot_str
        input_tensor = vision.TensorImage.create_from_file(
            IMAGES_DIR + current_image_ref)

        # get the object detection results
        detection_result = base_detector.detect(input_tensor)

        # logic to decide what to do based on result
        for detection in detection_result.detections:
            # get category with the highest score
            category = detection.categories[0]
            for c in detection.categories:
                category = c if c.score > category.score else category

            # if the score's threshold is greater than .5 then continue analysing the image
            if category.score >= .5:
                if category.category_name == 'bird':
                    # get bird species from picture
                    bird_species_result = classifier.classify(input_tensor)
                    # check if there are any matches for bird species
                    if bird_species_result.classifications[0].categories:
                        bird_species = bird_species_result.classifications[0].categories[0].display_name
                        if (bird_species == "None"):
                            bird_species = "Unknown"
                        status = "Bird Spotted"
                        logger.info("bird spotted, sending update...")
                        # update bird sightings on firebase
                        update_bird_sightings(current_image_ref, bird_species)
                        # send update
                        _make_twitchr_request(
                            data={"type": "bird", "species": bird_species})
                        bird_timer = current_time
                        break
                elif category.category_name == 'cat':
                    status = "CAT SPOTTED"
                    logger.info("cat spotted, sending update...")
                    # update cat sightings on firebase
                    update_cat_sightings(current_image_ref)
                    _make_twitchr_request(data={"type": "cat"})
                    break

        # if a bird has not been seen in 30 mins or more, play a sound to try to attract them
        difference = current_time - bird_timer
        if difference.total_seconds() >= 1800:
            logger.info("no bird spotted for 30 minutes")
            make_play_sound_request()
            # reset the timer
            bird_timer = current_time

        # send update to firebase realtime db
        device_data = get_device_data(sense)
        logger.info("updating realitime db...")
        update_realtime(status, device_data, current_image_ref)

        # delete temp image
        os.remove(IMAGES_DIR + snapshot_str)
        logger.info("deleted snapshot")

        # go to sleep for 30 seconds
        logger.info("going to sleep")
        time.sleep(30)
        logger.info("waking up")


if __name__ == '__main__':
    run()
