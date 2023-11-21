import cv2
import serial

def main():
    # Search for camera in usb ports
    camera_port = 0
    camera = cv2.VideoCapture(camera_port)
    if not camera.isOpened():
        print("Failed to open camera.")
        return
    
    # Show camera feed
    while True:
        ret, frame = camera.read()
        cv2.imshow('Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()