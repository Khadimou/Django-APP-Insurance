from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


# Create your views here.
from .forms import InscriptionForm, User
from pyspark.sql import functions as F
from .utils import prime_assurance
from pyspark.sql import SparkSession
import tempfile
import os
import csv
from django.http import HttpResponse
from assurance.forms import VehicleForm, InfoForm

def success_recommendation(request):
    return render(request, 'successreco.html')

def recommendation(request):
    if request.method == 'POST':
        form = InfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('successreco.html')
    else:
        form = InfoForm()
    
    return render(request, 'recommendation.html', {'form': form})


def create_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('successcreation.html')
    else:
        form = VehicleForm()
    
    return render(request, 'create_vehicle.html', {'form': form})


import os
import csv
import tempfile
from django.shortcuts import render, redirect
from django.http import HttpResponse
from pyspark.sql import SparkSession

def import_data(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file_path = temp_file.name
        temp_file.close()

        with open(temp_file_path, 'wb+') as destination:
            for chunk in csv_file.chunks():
                destination.write(chunk)

        # Vérification de l'existence du fichier temporaire
        if os.path.exists(temp_file_path):
            spark = SparkSession.builder.appName('prime_assurance').getOrCreate()
            spark_df = spark.read.csv(temp_file_path, header=True, inferSchema=True)
            # Traitement des données avec PySpark
            processed_data = prime_assurance(spark_df)

            csv_rows = []
            header_row = ['Risk Coefficient', 'Insurance Premium','Base Premium']

            # Récupérer les données
            for row in processed_data.collect():
                csv_row = list(row)
                csv_rows.append(csv_row)

            # inserer l'en-tête dans la première ligne de csv_rows
            csv_rows.insert(0, header_row)

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="processed_data.csv"'

            csv_writer = csv.writer(response)
            csv_writer.writerows(csv_rows)

            os.remove(temp_file_path)

            return response
        else:
            return HttpResponse('Erreur lors de la création du fichier temporaire.')

    return render(request, 'import_data.html')


def import_success(request):
    return render(request, 'import_success.html')


def inscription_view(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            # Récupérer les données du formulaire
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            telephone = form.cleaned_data['telephone']

            # Créer un nouvel utilisateur dans la base de données
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )

            # Enregistrer le numéro de téléphone de l'utilisateur
            user.profile.telephone = telephone
            user.profile.save()

            # Effectuer d'autres opérations ou rediriger vers une page de succès
            return redirect('accueil')  # Rediriger vers la page d'accueil après l'inscription
    else:
        form = InscriptionForm()
    return render(request, 'inscription.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accueil')  # Remplacez 'accueil' par l'URL de la page d'accueil après la connexion
        else:
            error_message = 'Nom d\'utilisateur ou mot de passe incorrect.'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accueil')  # Remplacez 'accueil' par l'URL de la page d'accueil après la déconnexion
    else:
        return render(request, 'logout.html')

def accueil(request):
    return render(request, 'accueil.html')


