import time
from tkinter import Tk, filedialog

import cv2
import mss
import numpy as np

from master_thesis_python_repo.helper.filter import Filter_With_Config
from master_thesis_python_repo.helper.import_config import FilterSettings
from master_thesis_python_repo.helper.mouse_capture import add_mouse

# from matplotlib import pyplot as plt


class Screen_Capture:
    def __init__(self, name, screen_width, screen_height):
        # Define application settings
        self.name = name
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Ask the user for the config file location,
        # import settings and setup filter
        Tk().withdraw()
        file_path = filedialog.askopenfilename()
        filter_settings = FilterSettings.import_config(file_path)
        self.filter = Filter_With_Config(filter_settings=filter_settings)

    def run(self):
        with mss.mss() as sct:
            # Define the part of the screen to capture
            monitor = {
                "top": 0,
                "left": 0,
                "width": self.screen_width,
                "height": self.screen_height,
            }
            windowName = "OpenCV/Numpy blur"

            # Create a black image in a new window
            img = np.zeros((800, 800, 3), np.uint8)
            cv2.namedWindow(windowName)

            # Create UI element
            toggleFilter = "Filter: 0=OFF, 1=ON"
            toggleMouseBlur = "Mouse blur: 0=OFF, 1=ON"
            cv2.createTrackbar(toggleFilter, windowName, 0, 1, self.nothing)
            cv2.createTrackbar(toggleMouseBlur, windowName, 0, 1, self.nothing)

            # ___________ Plots for developers - Part 1 of 2 ___________
            # Turn on interactive mode for Matplotlib
            # plt.ion()

            # # Create the plot
            # fig, ax = plt.subplots()
            # (lineR,) = ax.plot(range(self.screen_width))
            # (lineG,) = ax.plot(range(self.screen_width))
            # (lineB,) = ax.plot(range(self.screen_width))
            # ax.set_ylim(0, 255)

            while "Screen capturing":
                # Capture time for debugging
                last_time = time.time()

                # Get raw pixels from the screen, save it to a Numpy array
                img = np.array(sct.grab(monitor))

                # Get toggleFilter and toggleMouseBlur state
                s = cv2.getTrackbarPos(toggleFilter, windowName)
                toggleMouseBlur_value = cv2.getTrackbarPos(
                    toggleMouseBlur, windowName
                )

                # If toggleFilter is on use filter,
                # else show un-processed image
                if s == 1:
                    # If toggleMouseBlur is on don't blur the image in a circle
                    # around the mouse cursor, else blur everything
                    if toggleMouseBlur_value == 1:
                        img_final = self.filter.apply_to_image(
                            img=img, nonBlurRadius=100
                        )
                    else:
                        img_final = self.filter.apply_to_image(img=img)
                else:
                    img_final = img

                img_final = add_mouse(img_final)
                cv2.imshow(windowName, img_final)

                print(f"fps: {1 / (time.time() - last_time)}")

                # Press "q" to quit the application
                if cv2.waitKey(25) & 0xFF == ord("q"):
                    cv2.destroyAllWindows()
                    break

                # ___________ Plots for developers - Part 2 of 2 ___________
                # Get the 10th row of the image
                # row = img_final[round(len(img_final) / 2), :]
                # r_array = [inner[0] for inner in row]
                # g_array = [inner[1] for inner in row]
                # b_array = [inner[2] for inner in row]
                # # Update the plot
                # lineR.set_ydata(r_array)
                # lineG.set_ydata(g_array)
                # lineB.set_ydata(b_array)
                # plt.draw()
                # plt.pause(0.01)

    # Is needed for UI elements because we only want to read
    # their values and not run any fucntions
    def nothing(self, x):
        pass
