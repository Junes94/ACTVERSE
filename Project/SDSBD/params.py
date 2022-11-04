# Parameters for analysis of SDSBD AVATAR project.

# General SDSBD
# ['nose', 'head', 'anus', 'torso', 'LH', 'RH', 'LF', 'RF', 'tail']
fps = 30
start = round(fps * 5)  # start frame to be analyzed
end = round(fps * 400 - fps * 5)  # end frame to be analyzed

# Center SDSBD
joint1 = [3, 4, 5]  # Set head-torso middle point as a body center point
joint2 = [9, 10, 11]
radius = 3

# Walk SDSBD
vel_thres = 0.1
angle_thres = 90
dist_thres = 5
