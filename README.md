# **Hand Gesture-Based Volume and Screen Brightness Control**

## **Description**
This program allows users to control volume or screen brightness using hand gestures, based on the distance between the index finger and thumb, depending on the selected mode. The application offers a pause function and dynamic mode switching. The user has access to a GUI displaying the camera feed, information, and buttons. Image analysis (hand shape recognition) is performed using the OpenCV library.

## **Requirements**
- Python 3.x  
- PyQt6  
- opencv-python  
- numpy  
- mediapipe  
- pycaw  
- screen-brightness-control  

## **Installation**
1. Install the required libraries:
    ```sh
    pip install -r requirements.txt
    ```

## **Usage**
1. Run the application:
    ```sh
    python main.py
    ```
2. In the application window, select a mode (volume or brightness), then use your hand to control the settings.

## **Author**
Jakub Poznański
