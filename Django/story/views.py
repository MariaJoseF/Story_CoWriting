from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect,requires_csrf_token
from django.core import serializers
from .post import *

from .models import *

################################# ROS
import rospy
from std_msgs.msg import String, Empty, Header
pub_child_choice = rospy.Publisher('child_choice', String, queue_size=1)
#################################

class IndexView(generic.ListView):
	template_name = 'index.html'
	context_object_name = 'all_stories'

	def get_queryset(self):
		return Story.objects.all()

class HeaderView():
	template_name = 'header.html'

class FooterView():
	template_name = 'footer.html'

class StoryView(TemplateView):
	template_name = 'add_story.html'

class Story2View():
	template_name = 'add_story2.html'

class StoryCreate  (CreateView):
	model = Story
	fields = ['namest', 'script','idty','idsc']

# Lists all stories or create a new one
class StoryList(APIView):

	# def get(self, request):
	# 	story = Story.objects.all()
	# 	serializers = StorySerializer(story, many=True)
	# 	return Response(serializers.data)

	def post(self,request):
		template_name = 'add_story2.html'
		serializer = StorySerializer(data=request.data)
		if serializer.is_valid():
			#serializers.save()
			response = render(request, template_name, request.data)
    		return response

######old version
			#return Response(serializers.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FullStoryList(APIView):
	# def get(self, request):
	# 	story = Story.objects.all()
	# 	serializers = StorySerializer(story, many=True)
	# 	return Response(serializers.data)

	def post(self,request):
		#template_name = 'story.html'
		template_name = 'gendermch.html'
		serializer = FullStSerializer(data=request.data)
		gender = ""
		template_name_previous = template_name
		item = ""
		namevar = ""

		if request.method  == 'POST':
			if request.POST.get("Opt",None) is None:
				print("serializer.is_valid")

				if serializer.is_valid():
					#serializers.save()
					getPost = GetPostData()
					getPost.object_decoder(request.data)
					#print request.data
					response = render(request, template_name, request.data)
				return response

			else:
				try:
					dt = {}

					print ("---------------------------------")

					print ("items")
					for key, value in request.POST.items():
						print ("%s %s" % (key, value))


						v = value.replace("[", "")
						#print ("v %s" %v)
						value = v
						v = value.replace("]", "")
						#print ("v %s" %v)
						value = v

						v = value.replace("u'", "")
						#print ("v %s" %v)
						value = v
						
						v = value.replace("'", "")
						#print ("v %s" %v)
						value = v

						if key == 'gender':
							gender = value

						v = value.split(",")
						#print ("v %s" %v)
						value = v

 						strip_list = map(lambda it: it.strip(), value)
 						#print (strip_list)

						dt.update([(key, strip_list)])
						print (dt)

					emoti = request.POST.get("emotion",None)
					print ("receiveid emotion = %s" % emoti) 

					print ("OPT = ")
					print (request.POST.get("Opt"))
					print (request.POST.get("Opt") == 'Opt1')
		
					if request.POST.get("Opt") == 'Opt2':
						template_name_previous = 'mainch.html'
						item = request.POST.get("C_MC")
						print ("receiveid item = %s" % item) 
						namevar = "C_MC"
						if gender == "man":
							template_name = 'jobmc_man.html'
						elif gender == "robot":
							template_name = 'jobmc_robot.html'
						elif gender == "woman":
							template_name = 'jobmc_woman.html'
						

					elif request.POST.get("Opt") == 'Opt1':
						template_name_previous = 'gendermch.html'

						item = request.POST.get("C_MCg")
						print ("receiveid item = %s" % item) 
						namevar = "C_MCg"
						template_name = 'mainch.html'

					elif request.POST.get("Opt") == 'Opt3': 
						template_name_previous = 'jobmc_man.html'
						item = request.POST.get("C_MCj_man")
						print ("receiveid item = %s" % item) 
						namevar = "C_MCj_man"
						template_name = 'drinkmc.html'
						

					elif request.POST.get("Opt") == 'Opt4':
						template_name_previous = 'jobmc_woman.html'
						item = request.POST.get("C_MCj_woman")
						print ("receiveid item = %s" % item) 
						namevar = "C_MCj_woman"
						template_name = 'drinkmc.html'
						

					elif request.POST.get("Opt") == 'Opt5':
						template_name_previous = 'jobmc_robot.html'
						item = request.POST.get("C_MCj_robot")
						print ("receiveid item = %s" % item) 
						namevar = "C_MCj_robot"
						template_name = 'drinkmc.html'
						

					elif request.POST.get("Opt") == 'Opt6':
						template_name_previous = 'drinkmc.html'
						item = request.POST.get("C_MCd")
						print ("receiveid item = %s" % item) 
						namevar = "C_MCd"
						template_name = 'weapons.html'
						

					elif request.POST.get("Opt") == 'Opt7':
						template_name_previous = 'weapons.html'
						item = request.POST.get("C_MCw")
						print ("receiveid item = %s" % item) 
						namevar = "C_MCw"
						template_name = 'place.html'
						

					elif request.POST.get("Opt") == 'Opt8':
						template_name_previous = 'place.html'
						item = request.POST.get("C_P")
						print ("receiveid item = %s" % item) 
						namevar = "C_P"
						template_name = 'gendersc.html'
						

					elif request.POST.get("Opt") == 'Opt10':
						template_name_previous = 'secondarych.html'
						item = request.POST.get("C_SC")
						print ("receiveid item = %s" % item) 
						namevar = "C_SC"
						if gender == "man" or gender == "woman":
							template_name = 'speciesschuman.html'
						elif gender == "robot":
							template_name = 'speciesscrobot.html'
						

					elif request.POST.get("Opt") == 'Opt9':
						template_name_previous = 'gendersc.html'
						item = request.POST.get("C_SCg")
						print ("receiveid item = %s" % item) 
						namevar = "C_SCg"
						template_name = 'secondarych.html'
						

					elif request.POST.get("Opt") == 'Opt11':
						template_name_previous = 'speciesschuman.html'
						item = request.POST.get("C_SCs_human")
						print ("receiveid item = %s" % item) 
						namevar = "C_SCs_human"
						template_name = 'dancesch.html'
						

					elif request.POST.get("Opt") == 'Opt12':
						template_name_previous = 'speciesscrobot.html'
						item = request.POST.get("C_SCs_robot")
						print ("receiveid item = %s" % item) 
						namevar = "C_SCs_robot"
						template_name = 'dancesch.html'
						

					elif request.POST.get("Opt") == 'Opt13':
						template_name_previous = 'dancesch.html'
						item = request.POST.get("C_SC_dance")
						print ("receiveid item = %s" % item) 
						namevar = "C_SC_dance"
						template_name = 'genderbgc.html'
						

					elif request.POST.get("Opt") == 'Opt15':
						template_name_previous = 'badch.html'
						item = request.POST.get("C_BG")
						print ("receiveid item = %s" % item) 
						namevar = "C_BG"
						if gender == "man":
							template_name = 'jobbgc_man.html'
							gender = "man"
						elif gender == "robot":
							template_name = 'jobbgc_robot.html'
						elif gender == "woman":
							template_name = 'jobbgc_woman.html'
						

					elif request.POST.get("Opt") == 'Opt14':
						template_name_previous = 'genderbgc.html'
						item = request.POST.get("C_BGg")
						print ("receiveid item = %s" % item) 
						namevar = "C_BGg"
						template_name = 'badch.html'
						

					elif request.POST.get("Opt") == 'Opt16':
						template_name_previous = 'jobbgc_man.html'
						item = request.POST.get("C_BGj_man")
						print ("receiveid item = %s" % item) 
						namevar = "C_BGj_man"
						template_name = 'drinkbgc.html'
						

					elif request.POST.get("Opt") == 'Opt17':
						template_name_previous = 'jobbgc_woman.html'
						item = request.POST.get("C_BGj_woman")
						print ("receiveid item = %s" % item) 
						namevar = "C_BGj_woman"
						template_name = 'drinkbgc.html'
						

					elif request.POST.get("Opt") == 'Opt18':
						template_name_previous = 'jobbgc_robot.html'
						item = request.POST.get("C_BGj_robot")
						print ("receiveid item = %s" % item) 
						namevar = "C_BGj_robot"
						template_name = 'drinkbgc.html'
						

					elif request.POST.get("Opt") == 'Opt20':
						template_name_previous = 'badactions.html'
						item = request.POST.get("C_Ba")
						print ("receiveid item = %s" % item) 
						namevar = "C_Ba"
						template_name = 'placebg.html'
						

					elif request.POST.get("Opt") == 'Opt21':
						template_name_previous = 'placebg.html'
						item = request.POST.get("C_BGp")
						print ("receiveid item = %s" % item) 
						namevar = "C_BGp"
						template_name = 'story.html'
						

					elif request.POST.get("Opt") == 'Opt19':
						template_name_previous = 'drinkbgc.html'
						item = request.POST.get("C_BGd")
						print ("receiveid item = %s" % item) 
						namevar = "C_BGd"
						template_name = 'badactions.html'
						

					if item and emoti is not None:
						text = '{\''+namevar+'\': \' '+ item + '\', \'emotion\': \'' +emoti + '\'} \n'
						f = open('text.txt', 'a')
						f.write(text)
						f.close()
					else:
						raise Exception()
				except Exception as e:
					print ("errors???")
					print (e)

					dt.update([('error_message', 'Nothing Selected')])
					
					print (dt)
					return render(request,template_name_previous, context = dt, content_type="json")
				else:
					print ("Everything went well")
					return render(request,template_name,context = dt, content_type="json")	

		return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

#def storyteste(request):
	def storyteste(request):
		print ("story teste")
		if True:

		#if request.method  == 'POST':
			try:
				item = request.POST.get("C_MC",None)
				dt = request.POST.get("C_MCg")
				print ("receiveid item =") 
				print (item)
				option = request.POST.get("emotion",None)
				print ("receiveid option =") 
				print (option)
				if item is not None:
					text = {'selection':item, 'emotion':option}
					f = open('text.txt', 'w+')
					f.write(str(text))
					#json.dump(text,f)
					f.close()
					msg = String()
					msg.data = text
					pub_child_choice.publish(msg)

			except Exception as e:
				print ("errors???")
				return render(request,'add_story.html',{'error_message':'Nothing Selected'})
			else:
				print ("Everything went well")
				return render(request,'add_story.html',dt)
