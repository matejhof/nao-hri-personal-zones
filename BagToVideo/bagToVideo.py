#####################################################
##               Read bag from file                ##
#####################################################


# First import library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
# Import argparse for command-line options
import argparse
# Import os.path for file path manipulation
import os.path
import json

# Create object for parsing command-line options
parser = argparse.ArgumentParser(description="Read recorded bag file and display depth stream in jet colormap.\
                                Remember to change the stream resolution, fps and format to match the recorded.")
# Add argument which takes path to a bag file as an input
parser.add_argument("-i", "--input", type=str, help="Path to the bag file")
# Parse the command line arguments to an object
args = parser.parse_args()
# Safety if no parameter have been given
if not args.input:
    print("No input paramater have been given.")
    print("For help type --help")
    exit()
# Check if the given file have bag extension
if os.path.splitext(args.input)[1] != ".bag":
    print("The given file is not of correct file format.")
    print("Only .bag files are accepted")
    exit()

fourcc = cv2.VideoWriter_fourcc(*'x264')
videoFPS = 15.
videoFrames = 0
videoColored = cv2.VideoWriter(args.input[:-4] + '-raw.avi',fourcc, videoFPS, (1280,720))

try:
   # Load camera advanced settings
   ctx = rs.context()
   devices = ctx.query_devices()
   dev = devices[0]
   advnc_mode = rs.rs400_advanced_mode(dev)

   while not advnc_mode.is_enabled():
      print("Activating advanced mode")
      advnc_mode.toggle_advanced_mode(True)
      time.sleep(5)

   with open('cameraSettings.json', 'r') as json_file:
     as_json_object = json.load(json_file)

   # For Python 2, the values in 'as_json_object' dict need to be converted from unicode object to utf-8
   if type(next(iter(as_json_object))) != str:
      as_json_object = {k.encode('utf-8'): v.encode("utf-8") for k, v in as_json_object.items()}
   # The C++ JSON parser requires double-quotes for the json object so we need
   # to replace the single quote of the pythonic json to double-quotes
   json_string = str(as_json_object).replace("'", '\"')
   advnc_mode.load_json(json_string)

   #Create a config and configure the pipeline to stream
   # color and depth streams - should be kept same, otherwise projection won't work
   config = rs.config()

   # Tell config that we will use a recorded device from filem to be used by the pipeline through playback.
   rs.config.enable_device_from_file(config, args.input, repeat_playback=False)
   # Configure the pipeline to stream the depth stream
   config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, int(videoFPS))

   # Create pipeline
   pipeline = rs.pipeline()

   # Start streaming from file
   profile = pipeline.start(config)

   playback = profile.get_device().as_playback()
   playback.set_real_time(False)


   # Create opencv window to render image in
   cv2.namedWindow("RealSense", cv2.WINDOW_NORMAL)
   
   while True:
      frames = pipeline.wait_for_frames()
      color_frame = frames.get_color_frame()
      color_image = np.asanyarray(color_frame.get_data())
      videoColored.write(color_image)
finally:
   videoColored.release()