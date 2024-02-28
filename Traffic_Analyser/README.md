# Traffic Analyser

In the scripts folder there are two scripts with the extension .py that create this application.
The executable folder contains all the necessary files to easily run Traffic Analyser, including gui.exe, yolov3_custom_best.weights and yolov3_custom.cfg.
Besides, three example videos in .mp4 format that can be used for analysis are provided. Please note that depending on the length of the video, its analysis may take much more time.

- NYStreets.mp4    14s 
- cityRoad.mp4     16s
- bigTraffic.mp4   1:25m


## Usage
### Quickstart
Navigate to ./executable/gui and double-click on the 'gui' executable file to open it or if using a command line also go to the same folder and run `./gui start` command.

From the graphical interface level: 
- Select the video to be analysed in mp4 or avi format - 'Search files' button
- Start the analysis of the selected recording - 'Start analysis' button. 
Please note that video analysis can take up to a few minutes.
  
  After the video processing is finished, information about the end of the analysis will be displayed. The new analysed video is saved with .avi extension to /executable folder.
  
- Generate a .csv file containing timestamps along with the number of counted objects - 'Save CSV' button. The results are saved to /executable folder.
- Play the last processed video in a separate window - 'Play' button

### Analyse new video
To analyse a new video just click the 'Search files' button and follow the previous instructions

### Stop the program
To close the analyser, simply click the X button.

