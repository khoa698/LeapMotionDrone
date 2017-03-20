import ps_drone
import os, sys, inspect, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
import Leap
import math


drone = ps_drone.Drone()
drone.startup()
#delay to stabilise
time.sleep(1)

print 'Initialized...'

#initialise stored var and new vars
storedPitch = 0
storedYaw = 0
storedRoll = 0
storedVertical =160

pitch = storedPitch
yaw =storedYaw
roll =storedRoll
vertical =storedVertical


drone.takeoff()

#enable the Leap Motion Sensor
controller = Leap.Controller()
#enable gestures from the Leap Motion Sensor
controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
#configure the necessary gesture criteria to notice by the sensor
controller.config.set("Gesture.Swipe.MinLength", 30.0)
controller.config.set("Gesture.Swipe.MinVelocity", 150)
controller.config.save()
oldframe = controller.frame()
time.sleep(0.025)

while (True):
	frame = controller.frame()
	if (frame.hands.is_empty == False):
		all_hands = frame.hands
		if (len(all_hands) < 2):
			hand = all_hands.rightmost
			lefthand = None
		else:
			hand = all_hands.rightmost
			lefthand = all_hands.leftmost

		for gesture in frame.gestures(oldframe):
			if gesture.state is Leap.Gesture.STATE_START:
				pass
			elif gesture.state is Leap.Gesture.STATE_UPDATE:
				pass
			elif gesture.state is Leap.Gesture.STATE_STOP:
				if (gesture.type == Leap.Gesture.TYPE_SWIPE):
					drone.land()
					break


		#retrieve the normal of the palm
		normal = hand.palm_normal
		#retrieve the direction of the palm
		direction = hand.direction
		#retrieve the altitude of the palm
		vertical = hand.palm_position.y


			
		if ((math.degrees(direction.pitch) > storedPitch + 15) or (math.degrees(direction.pitch)<storedPitch -15)):
			#update pitch in degrees
			pitch = math.degrees(direction.pitch)
			#update the stored variable pitch
			storedPitch = pitch
		else:
			pitch = storedPitch

		if ((math.degrees(normal.roll) > storedRoll + 10) or (math.degrees(normal.roll)<storedRoll-10)):
			#update roll in degrees
			roll = math.degrees(normal.roll)
			storedRoll = roll
		else:
			roll = storedRoll
		if ((math.degrees(direction.yaw)> storedYaw +10) or (math.degrees(direction.yaw)<storedYaw-10)):
			yaw = math.degrees(direction.yaw)
			storedYaw=yaw
		else:
			yaw = storedYaw


        #normalise values of pitch/roll to fit -45 to 45
        #and yaw to fit -90 to 90
        #as sensors return only values from -90 to 90 degrees
        #and we don't want the drone to tilt to any degrees higher than 45
        #considering normal wind condition
		if (pitch > 45):
			pitch = 45
		elif (pitch < -45):
			pitch = -45
		if (roll > 45):
			roll = 45
		elif ( roll < -45):
			roll = -45
		if (yaw > 90):
			yaw = 90
		elif (yaw < -90):
			yaw = -90


        #As the values of speed taken by the drone is percentages
        #from -1 to 1, we need to take into account the percentage of speed
        #that is not too sensitive/high as hand motion has never been stable
		pitch = pitch / 90
		roll = roll / 50
		yaw = yaw / 80

		if ((vertical >= 400) or (vertical < 50)):
			vertical = 0
		else:
			vertical = (vertical - 150)/250


        #initialise left hand to control video capturing of the drone
		if (lefthand != None):
			drone.startVideo()
			drone.showVideo()
			if not (lefthand.fingers.is_empty):
				for finger in lefthand.fingers:
					if (finger.is_extended == True):
						if (finger.type == Finger.TYPE_INDEX):
							drone.frontCam()
						elif (finger.type == Finger.TYPE_THUMB):
							drone.groundCam()

        #trace old frame to capture any motion of the hand
		oldframe = frame
        #move the drone following the 4 criteria roll pitch yaw, height
		drone.move(-roll, -pitch, vertical, yaw)
        #sleeps for 25ms, refresh every 25ms
		time.sleep(0.025)
	else:
		drone.land()
		break
drone.shutdown()
print 'Completed trip.'





