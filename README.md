Folders:
- BagToVideo contains Python script to convert ".bag" videos from RealSense to .avi in x264 codec.
- Calibration/Positions contains original Choregraphe list of movements to create setup calibration sequence from.
- Realpose contains the main code of the whole experiment. You can run it from that folder as "python realpose.py -h", which will give you futhure help on how to use it.

Files in Realpose:
* keyframesToMotion.py - used to extract setup sequence into movementNAO21DB.py where each keyframe is interpreted as a new move.
* cameraSettings.json - contains settings for the RealSense camera.
* calibration.txt - used to save calibration more permanently. But if start recording, it is exported as part of the setup.
* motionFromRecording.py - used to extract movement data from recorded session.
* movementNAO21.py - used for pre-loaded movements from Choregraphe.
* rigid_transform_3D.py - used to calculate the transformation matrix.
* safeMotion.py - used for robot control within updated limits from the skin. Limits are stored in folder limits.
* skinPose.py - used for robots movement and headtracking.
* videoPose.py - processes the video and outputs current zones, distances etc.
* yarpConnectorSimple.py - used for connecting and reading robots
 skin when touched.