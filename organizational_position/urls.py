from django.urls import path
from . import views

urlpatterns = [
    path(''                     , views.organizational_position_index, name='organizational_position_index'),
    path('reports'              , views.organizational_position_reports, name='organizational_position_reports'),
    path('tree'                 , views.organizational_position_tree, name='organizational_position_tree'),
    path('database'             , views.organizational_position_database, name='organizational_position_database'),
    path('import/data'          , views.organizational_position_import_data, name='organizational_position_import_data'),
    path('import/data/sample'   , views.organizational_position_import_data_sample, name='organizational_position_import_data_sample'),
    path('import/assign'        , views.organizational_position_import_assign, name='organizational_position_import_assign'),
    path('import/assign/sample' , views.organizational_position_import_assign_sample, name='organizational_position_import_assign_sample'),
    path('export/data'          , views.organizational_position_export_data, name='organizational_position_export_data'),
    path('export/assign'        , views.organizational_position_export_assign, name='organizational_position_export_assign'),
]

