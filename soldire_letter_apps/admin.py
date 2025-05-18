from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(NormalLetter)
admin.site.register(ClearanceLetter)
admin.site.register(NormalLetterJudicialInquiry)
admin.site.register(NormalLetterMentalHealthAssessmentAndEvaluation)
admin.site.register(NormalLetterDomesticSettlement)
admin.site.register(IntroductionLetter)