from django.shortcuts import render, redirect
from django.http import JsonResponse
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from django.contrib import auth
from django.contrib.auth.models import User


gemini_api_key = '......'
os.environ["GOOGLE_API_KEY"] = gemini_api_key


def ask_gemini(message):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest",
                                 max_tokens=512,
                                 temperature=0.7)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful chatbot that answers the queries of users in helpful manner. Always answer in increasing order of complexity. Do not anser the question if you do not know the answer.",
            ),
            ("human", "{input}"),
        ]
    )

    chain = prompt | llm
    response = chain.invoke(
        {
            "input": message,
        }
    )
    # print(response.content)
    return response.content



# Create your views here.
def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_gemini(message)
        return JsonResponse({'message':message,'response':response})

    return render(request,'chatbot.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password!!!!!'
            return render(request,'login.html',{'error_message':error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username,email,password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Error creating account'
                return render(request,'register.html',{'error_message':error_message})
        else:
            error_message = "Password don't match!!"
            return render(request,'register.html',{'error_message':error_message})

    return render(request,'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')
