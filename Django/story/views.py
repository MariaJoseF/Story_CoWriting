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
		serializers = StorySerializer(data=request.data)
		if serializers.is_valid():
			#serializers.save()
			response = render(request, template_name, request.data)
    		return response

######old version
			#return Response(serializers.data, status=status.HTTP_201_CREATED)
		return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class FullStoryList(APIView):

	# def get(self, request):
	# 	story = Story.objects.all()
	# 	serializers = StorySerializer(story, many=True)
	# 	return Response(serializers.data)

	def post(self,request):
		#template_name = 'story.html'
		template_name = 'add_story.html'
		serializers = FullStSerializer(data=request.data)

		if request.method  == 'POST':
			if request.POST.get("Opt",None) is None:
				print("serializers.is_valid")

				if serializers.is_valid():
					#serializers.save()
					getPost = GetPostData()
					getPost.object_decoder(request.data)
					#print request.data
					response = render(request, template_name, request.data)
				return response

			else:
				try:
					#print (request.POST)
					item = request.POST.get("C_MC",None)
					dt = request.POST.get("received_dt")
					print ("dt = %s" % dt)
					#print (dt)
					print ("receiveid item = %s" % item) 
					#print (item)
					emoti = request.POST.get("emotion",None)
					print ("receiveid emotion = %s" % emoti) 
					#print (emoti)


					if item and emoti is not None:
						text = '{\'C_MC\': \' '+ item + '\', \'emotion\': \'' +emoti + '\'} \n'
						f = open('text.txt', 'a')
						f.write(text)
						# json.dump(text,f)
						f.close()
					else:
						raise Exception()
				except Exception as e:
					print ("errors???")
					print (e)
					return render(request,'add_story.html',{'request.data':request.data,'error_message':'Nothing Selected'})
				else:
					print ("Everything went well")
					data = {'received_dt':dt}
					print (data)
					return render(request,'add_story.html',data)	
######old version
			#return Response(serializers.data, status=status.HTTP_201_CREATED)
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
