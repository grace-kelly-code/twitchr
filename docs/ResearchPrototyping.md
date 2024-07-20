# Research and Prototyping

## Intro

The purpose of this document is to have a record and reference point while I am at the research and prototyping phase. My project - Twitchr is a bird feeder monitor.

## Camera

The first thing I want to look into is how I am going to take a picture. I am going to use my USB web camera because it is 1080p, there is a long wire on it and it has a clamp so I have more options on where to place it, and because I want to use the sense hat to display information, the rpi will remain inside the house while the camera could be either inside or outside.

[How to capture a single photo with webcam using OpenCV in Python (educative.io)](https://www.educative.io/answers/how-to-capture-a-single-photo-with-webcam-using-opencv-in-python)

In the above guide it mentions the library OpenCV, so i will try and install that

```sql
pip3 install opencv-python
```

```python
import cv2
camera = cv2.VideoCapture(0)
# webcam is 1080p
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# take photo
ran_successful, image = camera.read()
# save photo
cv2.imwrite('current_image.jpg', image)
```

I am going to connect the webcam and try this above code


![cam_pik](https://github.com/user-attachments/assets/7b3d745f-c0f7-4df1-b724-687b778da04d)


The camera works!! 📸 So I can use opencv to take pictures, i think i might have it do it every X number of seconds instead of continuously especially if i am going to be storing these images in firebase, i don’t want to fill up the space too quickly…

## Image Detection and Classification

Now that I have my camera setup, I am now going to look at how to detect birds and cats via [TensorFlow](https://www.tensorflow.org/). 

I‘ve read the following on how TensorFlow works and how models are trained:

[What is TensorFlow, and how does it work? – Towards AI](https://towardsai.net/p/l/what-is-tensorflow-and-how-does-it-work)

[Is Your Dog an Elephant? Building an Animal Classifier with TensorFlow | by Peter Chau | Tensorpad | Medium](https://medium.com/tensorpad/building-an-animal-classifier-with-tensorflow-ad5931b04946)

[Using TensorFlow to recognize Cats and Dogs | by Patrick Kalkman | Towards Data Science](https://towardsdatascience.com/recognizing-cats-and-dogs-with-tensorflow-105eb56da35f)

I’ve decided for this project I could use some models that are freely available on tensor’s website instead of training my own. I am also going to use TensorFlow Lite as it’s much faster and the type of detection I want to do is not very complex.

I found the python library `tflite_support` which is mentioned in the Tensorflow docs so i will import that and try it out

[Module: tflite_support  |  TensorFlow Lite](https://www.tensorflow.org/lite/api_docs/python/tflite_support)

Base Detection Model → [https://tfhub.dev/tensorflow/lite-model/efficientdet/lite0/detection/metadata/1](https://tfhub.dev/tensorflow/lite-model/efficientdet/lite0/detection/metadata/1)

```python
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision

# this should detect if it is a bird or a cat
base_options = core.BaseOptions(file_name='lite-model-detection.tflite')
detection_options = processor.DetectionOptions(max_results=2)
options = vision.ObjectDetectorOptions(base_options=base_options, detection_options=detection_options)
base_detector = vision.ObjectDetector.create_from_options(options)

input_tensor = vision.TensorImage.create_from_file('goldfinch.jpg')
# see if it sees a cat or bird
detection_result = base_detector.detect(input_tensor)

print(detection_result)
```

I will supply it a couple of images to see what happens

Bird


![bird1](https://github.com/user-attachments/assets/985c4bf9-deb2-4d4c-81b4-0cb3283ea733)


```bash
Category(index=15, score=0.7578125, display_name='', category_name='bird')
```

Cat

![cat](https://github.com/user-attachments/assets/48b6ccb0-58fc-4e66-aa48-b8ee3398f6db)



```bash
Category(index=16, score=0.87109375, display_name='', category_name='cat')
```

Dog


![dog](https://github.com/user-attachments/assets/0d09bcb5-91c9-480e-ac2a-e8772c375644)


```bash
Category(index=17, score=0.81640625, display_name='', category_name='dog')
```

Now to test the classification model, I want to determine what type of bird is present

[Integrate object detectors  |  TensorFlow Lite](https://www.tensorflow.org/lite/inference_with_metadata/task_library/object_detector) this was used to use the tflite-support package

bird classification model - [TensorFlow Hub (tfhub.dev)](https://tfhub.dev/google/lite-model/aiy/vision/classifier/birds_V1/3) 

```python
# this should tell me what type of bird is spotted
base_options = core.BaseOptions(file_name='lite-model-birds.tflite')
classification_options = processor.ClassificationOptions(max_results=2)
options = vision.ImageClassifierOptions(base_options=base_options, classification_options=classification_options)
classifier = vision.ImageClassifier.create_from_options(options)

input_tensor = vision.TensorImage.create_from_file('goldfinch.jpg')
classification_result = classifier.classify(input_tensor)

print(classification_result)
```

I’ve supplied it a sample image and it works!!


![bird2](https://github.com/user-attachments/assets/562fb7da-823c-4446-9064-7e8546462bbf)


```sql
Category(index=556, score=0.578125, display_name='Carduelis carduelis', category_name='/m/0fq15')
```

Another Example


![bird3](https://github.com/user-attachments/assets/ff8680d6-eb58-4084-9ef5-a980e5ccf79c)


```bash
Category(index=665, score=0.9765625, display_name='Cyanistes caeruleus', category_name='/m/01kvvt')
```

It seems to be working pretty good!!

## Sending Comms

I want to send a message when a bird is spotted - I’m going to use Twilio for this. I remember signing up for the GitHub Developer pack and there is a $50 credit to use


![twilio](https://github.com/user-attachments/assets/0d5935d0-840b-4e4a-bedc-c58812b76bd9)



The docs are very nice to use and there are docs for both python and node which will be useful if I want to send the SMS messages through the glitch web application or via the rpi

For the purposes of research I’ll try the python client

```sql
from twilio.rest import Client as TwilioClient
twilio_client = TwilioClient(ACCOUNT_SID, AUTH_TOKEN)

def send_sms(client: TwilioClient, phone_number: str, msg_body: str):
  """Sends a sms to a provided phone number"""
  client.messages.create(
                  to=phone_number, 
                  from_="<twilio_number>",
                  body=msg_body)

bird_breed = 'penguin'
bird_url = 'https://en.wikipedia.org/wiki/penguin'
msg_body = "\n\n🐦 Bird Spotted!! 🐦\n\nSpotted a {}\n\nRead about it here: {}".format(bird_breed, bird_url)
send_sms(twilio_client, "<phone_number>", msg_body)
```

and it works, I received an SMS on my phone


![sms](https://github.com/user-attachments/assets/47eae46e-1bb7-4b6e-9265-ccbac2eea53b)


I also want to be able to send an email to a user ✉️ After taking a look at a few options like Sendgrid and Mailchimp I’ve decided to go with Mailgun for this as the documentation looked good, it has an SMTP option and there is a free plan [SMTP | Mailgun](https://www.mailgun.com/products/send/smtp/)

Testing out the library by following the guide provided, but I haven’t received any email…

After 10 minutes I still haven’t received an email…

Investigating further it looks like I need to add my email as an authorized recipient: [Authorized Recipients – Mailgun Help Center](https://help.mailgun.com/hc/en-us/articles/217531258-Authorized-Recipients) 

Adding it now and trying again...

I still haven’t received the email in my inbox.

Looking in my spam folder and the email is there!!

![email](https://github.com/user-attachments/assets/9d29bbfd-c6fb-4a62-9c7a-ff0ceb8e6a19)

It looks like as this is a sandbox account the email will always be in the spam folder which for the purposes of this project is fine.

## Playing Sounds

Now I know the pi can spot a cat, I want to be able to raise an alarm if a cat is spotted at the bird feeder, so I want to connect a bluetooth speaker. 

This is a nice guide to connect my speaker: [Connecting bluetooth audio device to Raspberry Pi - Wiretuts](https://wiretuts.com/connecting-bluetooth-audio-device-to-raspberry-pi)

I found some mp3s of dogs barking and downloading one from here [Dog Sounds - Listen or Free Download MP3 | Orange Free Sounds](https://orangefreesounds.com/sound-effects/animal-sounds/dog-sounds/)

This sound effect sound plays for too long so I went with this shorter one

[Download Free Dog Sound Effects | Mixkit](https://mixkit.co/free-sound-effects/dog/)

```python
pulseaudio --start
sudo bluetoothctl
default-agent
scan on
trust MAC:ADDRESS
pair MAC:ADDRESS
connect MAC:ADDRESS
```

I’ve managed to connect my headphones to the raspberry pi for testing purposes with the mac address of them - I had some issues initially but following the troubleshooting guide in the link above solved these issues for me.

Next I need to figure out how to actually play the sound doing a search I found this article:

[Python | Playing audio file in Pygame - GeeksforGeeks](https://www.geeksforgeeks.org/python-playing-audio-file-in-pygame/)

so I’ll give the `pygame` module a try

```python
import pygame

pygame.mixer.init()
pygame.mixer.music.load("dog-bark.mp3")
pygame.mixer.music.play()
```

Success! I’ve gotten the sound effect to play 🎵 So I can use this to play a dog barking, I think I might also implement it to play a sound if a bird hasn’t been spotted in X number of minutes to see if it would attract one to the feeder.

## Displaying Messages

I want to show a message on the sense hat when something is spotted, I know I can do this via the `sense` library but I would also like to display a pixel image as well as a string.

Raspberry Pi have a guide on how to do that: [Projects | Computer coding for kids and teens | Raspberry Pi](https://projects.raspberrypi.org/en/projects/getting-started-with-the-sense-hat/5)

I drew a couple of simple pixel images on a 8x8 grid so I could calculate the colors and co-ordinates

Bird:


![pixl1](https://github.com/user-attachments/assets/ce3857bf-e6fb-4f14-b97f-f2ed36337f85)


Cat:

![pixl2](https://github.com/user-attachments/assets/ae267202-ced1-4966-a6f2-6f23042f24e1)


```python
from sense_hat import SenseHat

sense = SenseHat()

r = (255, 0, 0)
blu = (90, 250, 250)
w = (213, 214, 219)
blk = (26, 32, 48)
o = (255, 169, 65)

BIRD = [
    blk, blk, blu, blu, blk, blk, blk, blk,
    blk, blu, blu, blu, blu, blk, blk, blk,
    o, blu, w, blu, blu, blk, blk, w,
    blk, blu, blu, blu, w, w, w, w,
    blk, blu, blu, blu, w, w, w, w,
    blk, blk, blu, blu, blu, blu, blu, blk,
    blk, blk, blu, blu, blu, blk, blk, blk,
    blk, blk, o, blk, o, blk, blk, blk
]

CAT = [
    blk, blk, blk, blk, blk, blk, blk, blk,
    blk, blk, blk, o, blk, blk, o, blk,
    blk, blk, blk, o, o, o, o, blk,
    o, o, blk, o, r, o, r, blk,
    o, blk, blk, o, o, o, o, blk,
    o, o, o, o, o, o, blk, blk,
    blk, o, o, o, o, o, blk, blk,
    blk, o, o, blk, o, o, blk, blk
]

sense.set_pixels(BIRD)
time.sleep(10)
sense.clear()
sense.set_pixels(CAT)
time.sleep(10)
```


Using the 8x8 grid makes things a lot easier to work out the co-ordinates

## Message Queueing

I want the sound to be played automatically when a cat is spotted and I want the messages to appear on the sense hat so I think having a MQTT queue would be a good way of achieving this. For example I can publish a message to the queue when the cat is spotted and then have a listener on the pi that will trigger the alarm and displays an image when it receives the message

I am going to try [HiveMq](https://www.hivemq.com/?utm_source=adwords&utm_campaign=&utm_term=hive%20mqtt&utm_medium=ppc&hsa_tgt=kwd-1211385496493&hsa_cam=14220703563&hsa_src=g&hsa_net=adwords&hsa_kw=hive%20mqtt&hsa_ad=625076184875&hsa_grp=143284499233&hsa_ver=3&hsa_acc=3585854406&hsa_mt=p&gclid=CjwKCAiAv9ucBhBXEiwA6N8nYOKmkTdsgI4x3f4CrZegjxuwcJsEmh08Iwgqj1Ij2asGswJOsNPUDRoCIRsQAvD_BwE), there is a nice web client that is in beta so it looks like it would be good for testing purposes


![mqtt](https://github.com/user-attachments/assets/d8aaf982-4251-4b94-8d45-8b80fe3390c0)


There is also docs for Python and Node, I am thinking of using the Twitchr Web App as a middle man to make these requests so Node will be the way to go for that, and I will set up the listener on the rpi using Python so it can then play sounds/display messages

```bash
const options = {
  host: *******,
  port: *******,
  protocol: "mqtts",
  username: *******,
  password: *******,
};

const client = mqtt.connect(options);
client.publish("test", "Hello World!", { qos: 2, retain: false }
```

It works!! 🎉


![msg](https://github.com/user-attachments/assets/10d6b970-efb9-4649-b209-8b231849ea0d)


## Storage

I want to display the latest image on the twitchr website and keep the data fresh, to do this i am going to use Firebase

[IoT Using Raspberry Pi and Firebase and Android - Hackster.io](https://www.hackster.io/ahmedibrrahim/iot-using-raspberry-pi-and-firebase-and-android-dbe61d)

Trying to install `firebase-admin` is throwing up the following error:

```sql
This package requires Rust >=1.48.0.
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for cryptography
Failed to build cryptography
ERROR: Could not build wheels for cryptography, which is required to install pyproject.toml-based projects
```

I tried installing cryptography separately and that fails aswell so I am going to try installing an earlier version of cryptography

```sql
pip3 install cryptography==3.4.2
```

that installed, and now i can install firebase-admin and try it out

```python
pip3 install firebase-admin
```

```bash
file = os.path.basename('pine-grosbeak.jpg')
blob = bucket.blob(file)
outfile = 'pine-grosbeak.jpg'
blob.upload_from_filename(outfile)
```

success with uploading the image to the storage bucket


![firebase](https://github.com/user-attachments/assets/c05347d2-5bde-4526-9437-c3c60d2e94b3)


I have a fair idea how firebase works for when it comes to using it on my glitch web app. I think I am going to use [Chartjs](https://www.chartjs.org/) to display some nice graphs using the data like how many sightings throughout the week and a breakdown of each species of bird spotter.

I am also going to have users for the Twitchr website where they can set their email and phone number for the notifications, and set whether they want alerts sent to them. For this kind of data I think I will use [lowdb](https://github.com/typicode/lowdb).

Also for the website I would like to use a components framework like Semantic UI, I think for this project I will use [Bootstrap](https://getbootstrap.com/) because it has some nice components like tables and toast messages which I think will be useful

## Security

Speaking of users, I will need to make sure whatever API I create will have to be secure as I don’t want anyone making requests to it and abusing the app and publish messages to the MQTT queue or sending comms out 🔒

I found this guide on API Authentication : [API Keys: API Authentication Methods & Examples (stoplight.io)](https://blog.stoplight.io/api-keys-best-practices-to-authenticate-apis) I think I will assign each user on the app an API key (store it in the db) and provide this key whenever making a request and have the application check to make sure it is valid before allowing the request

```bash
GET / HTTP/1.1
Host: example.com
X-API-KEY:  abcdef12345
```

## Weather Updates

I also want to get weather updates and send comms based on the type of reading so I will use OpenWeatherMap API to get these readings. I want to make a call once an hour to see if the sun will be setting soon. I think I might create a cron job to do this for me

[Cron Jobs in Glitch? Easy. A much cleaner setup for creating Cron… | by Joshua Tabansi | Medium](https://medium.com/@joshuatabansi/cron-jobs-in-glitch-easy-e6068b14e474)

On second thoughts, it looks like Glitch doesn’t allow cron tasks to be performed if you are using the free tier: [Glitch banning use of pinging services | Botwiki](https://botwiki.org/blog/glitch-banning-use-of-pinging-services/)

I will probably use Thingspeak then instead - I can create a Thingspeak Htpp and then a TimeControl to let it make a request to open weather map once an hour. Maybe I might use the twitchr web app to act as a middle man for this and let the user set the rpi’s co-ordinates (stored in the lowdb database) to get accurate weather results.


![thingspeak](https://github.com/user-attachments/assets/4d04db8e-9703-4e34-96b1-41ab61107187)


I can then send comms out for situations like the sun is setting soon so time to bring in the bird feeder and maybe display a weather icon on the sense hat (the MQTT queue would come in handy for that)

## Bird Feeders

I need to have subject matter to test the twitchr project on so I am going to need to get some bird feeders.

This post mentions some types of bird feeders: [https://www.woodlandtrust.org.uk/blog/2020/07/attract-birds-to-your-garden/](https://www.woodlandtrust.org.uk/blog/2020/07/attract-birds-to-your-garden/)

I decided to get a few different ones and try them out, I got a peanut feeder, a seed feeder and a mealworm feeder.  My idea is to place the hanging feeders in a couple of different spots to start attracting birds and when they are comfortable with the feeders they will hopefully come to the window feeder on the house so I can capture some photos with the web cam.

![birdfeeder](https://github.com/user-attachments/assets/c77ae57b-0531-423d-b7c9-dd35e02ddd76)


After a couple of days of nothing, I looked out the window and saw this guy!!


![bird_on_feeder](https://github.com/user-attachments/assets/a270e19a-bbdf-4919-bff7-22d50b7c176b)

## End

From the above research and prototyping, I think I have an idea of how I am going to approach this project. I will next work on my flow diagrams and then start implementing all of the components and work on piecing everything together.
