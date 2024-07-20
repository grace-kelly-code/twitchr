# Twitchr

<img width="384" alt="top" src="https://github.com/user-attachments/assets/113b9bef-2744-4531-8a86-724aa18aa7d5">



## About

Twitchr is a bird feeder monitoring system for the RPI. This application has the following purposes:

1. Take snapshots of the bird feeder every 30 seconds and see if a cat or bird is spotted using a Tensorflow Lite Detection and Classification models.
    1. If a bird is spotted, update bird sightings on Firebase and send a request to the Twitchr Web Application to send comms to subscribed users.
    2. If a cat is spotted, send a request to the Twitchr Web Application to send notifications and play a barking sound through the Bluetooth speaker (via MQTT Queue). Also update cat sightings in Firebase.
    3. Send up to date snapshot of bird feeder along with the status (Nothing/Bird/Cat Spotted) and sense hat readings (temperature, humidity, pressure) to Firebase

2. If no bird has been spotted for 30 minutes, make a request to the Twitchr Web Application to play a sound to try and attract a bird to visit the feeder e.g. insects, water running (via MQTT Queue). This can also be achieved manually by pressing the button on the sense hat.

3. Run a MQTT client that listens for messages on the `twitchr` topic (posted to it via the Twitchr Web App).
   
   1. If the payload contains `bird` - display alert on the sense hat
   


    https://github.com/user-attachments/assets/ac726010-4298-4a9e-be45-c5475837400b


    2. If the payload contains `cat` - display alert on the sense hat and play alarm through the bluetooth speaker



    https://github.com/user-attachments/assets/84576998-668a-4624-bade-2f39df1d0de7



    3. If the payload contains `weather` - display alert on the sense hat



     https://github.com/user-attachments/assets/bd8f8aad-960e-47c8-ad79-f8baa80365df



    4. If the payload contains `play_sound` - play selected sound via the Bluetooth speaker



    https://github.com/user-attachments/assets/6d01deb9-381f-45ce-bbcf-d02d4e8856d7



This application should be used in conjunction with the [Twitchr Web Application](https://github.com/gracielilykelly/twitchr-app/)

## Flow Diagram

<img width="1223" alt="Screenshot 2022-12-13 164245" src="https://user-images.githubusercontent.com/97189399/207392677-72eacdda-30b2-4258-b9ef-cf9718c456d0.png">



## Project Setup

Plugged in RPI with USB Camera and Bluetooth Speaker:

![setup](https://github.com/user-attachments/assets/941323a3-e692-438f-a7e6-343e1fef13f8)

Placed Webacam and Speaker Outside in view of the Feeder:

![bird_outside](https://github.com/user-attachments/assets/20abd43f-6a53-484b-bad7-d3e08523f3a3)


## Installation Guide

The Installation Guide for this application can be found [here](https://github.com/gracielilykelly/twitchr/blob/main/docs/Installation%20Guide.md)


## Documentation

You can find documentation related to this project [here](https://github.com/gracielilykelly/twitchr/tree/main/docs)
