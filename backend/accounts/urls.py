from django.urls import path

from .views import dashboard, patient_identity, patient_search

app_name = "accounts"

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('patient/<int:pk>/identity/', patient_identity, name='patient_identity'),
    path('patient/rechercher/', patient_search, name="patient_search"),
]

### Recherche Patient
# patient/recherche?q=XXX
# patient/recherche_insi?q=XXX


