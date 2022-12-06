import os
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression




from django.contrib import messages
import pandas as pd
import numpy as np
import plotly.express as px

# Create your views here.



def home(request):
    
    if request.method == 'POST':
        uploaded_file = request.FILES['data_file']

        if uploaded_file.name.endswith('.csv'):
            #save the file in media
            #     
            savefile = FileSystemStorage()

            name = savefile.save(uploaded_file.name, uploaded_file)

            d = os.getcwd() #gets current directory
            file_dir = d+'\media\\'+name
            readfile(file_dir)
            
            


        else: 
            messages.warning(request, 'file was not uploaded')

        return redirect(results)
    
    return render(request, 'home.html')

def readfile(filename):
    
    global rows, cols, dat1, dat2, a, b, model

    my_file = pd.read_csv(filename, sep='[,]', engine='python')

    data = pd.DataFrame(data=my_file)

    data_array = np.array(data)

    rows = len(data_array[:,0])
    cols = len(data_array[1,:])

    dat1 = data_array[:,0].reshape(-1, 1)#[np.newaxis]
    dat2 = data_array[:,1].reshape(-1, 1)#[np.newaxis]
    
    a = data_array[:,0]
    b = data_array[:,1]

    model = LinearRegression()
    model.fit(dat1,dat2)
    

def results(request):
    global username, eval

    df = pd.DataFrame(dict(
    x = a,
    y = b))

    fig = px.scatter_matrix(df) 

    #fig = px.line(a,b)
    Chart_fig = fig.to_html()

    hi = Chart_fig
    
    if request.method == 'POST':
        
        username = request.POST.get('number')
        eval = model.predict(np.array(username, dtype=float).reshape(-1, 1))
        return redirect(results1)

    #name = request.POST['number']

    return render(request, 'results.html', {'tru':hi})

def results1(request):

    return render(request, 'results1.html', {'yes': eval})