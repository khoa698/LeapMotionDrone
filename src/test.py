import os, sys, inspect, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
import math

storedPitch = -1.503539253670133
storedYaw = -14.89836891011053
storedRoll = 26.59556988266136
storedVertical =150
pitch = storedPitch
yaw =storedYaw
roll =storedRoll
vertical =storedVertical

controller = Leap.Controller()
controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
controller.config.set("Gesture.Swipe.MinLength", 30.0)
controller.config.set("Gesture.Swipe.MinVelocity", 150)
controller.config.save()
oldframe = controller.frame()
while (True):
	frame = controller.frame()
	if (frame.hands.is_empty == False):
		all_hands = frame.hands
		if (len(all_hands) < 2):
			righthand = all_hands.rightmost
			twohand = False
			print '1 hand'
		else:
			righthand = all_hands.rightmost
			lefthand = all_hands.leftmost
			twohand = True
			print '2 hands'

		for gesture in righthand.frame.gestures(oldframe):
			if gesture.state is Leap.Gesture.STATE_START:
				pass
			elif gesture.state is Leap.Gesture.STATE_UPDATE:
				pass
			elif gesture.state is Leap.Gesture.STATE_STOP:
				if (gesture.type == Leap.Gesture.TYPE_SWIPE):
					swipe = Leap.SwipeGesture(gesture)
					print swipe.speed

			else:
				print 'nothing much...'
		print '\n\n'

		if (twohand == True):
			print 'there is a left hand!'
			if not (lefthand.fingers.is_empty):
				for finger in lefthand.fingers:
					if (finger.is_extended == True):
						if (finger.type == Leap.Finger.TYPE_INDEX):
							print 'index uppppp'
						elif (finger.type == Leap.Finger.TYPE_THUMB):
							print 'thumbs uppppppp'
		oldframe = frame
		time.sleep(0.025)
		print '\n\n'


