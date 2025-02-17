from django.db import models

# Create your models here.
class SoldierDocuments(models.Model):
    soldier = models.OneToOneField('soldires_apps.Soldier', on_delete=models.CASCADE, verbose_name="سرباز")
    personal_info_form = models.BooleanField("فرم اطلاعات فردی", default=False)
    training_skills_form = models.BooleanField("فرم مهارت‌آموزی", default=False)
    mental_health_form_training = models.BooleanField("برگه سلامت روان آموزشی", default=False)
    introduction_letter = models.BooleanField("معرفی نامه (پاراف شده)", default=False)
    green_dispatch_paper = models.BooleanField("برگه سبز اعزام", default=False)
    training_center_referral_paper = models.BooleanField("برگه مراجعه به مرکز آموزش", default=False)
    ideological_report_card = models.BooleanField("کارنامه عقیدتی", default=False)
    sater_paper = models.BooleanField("برگه ساتر", default=False)
    vaccination_paper = models.BooleanField("برگه واکسیناسیون", default=False)
    green_training_paper = models.BooleanField("برگه سبز آموزشی", default=False)
    educational_report_card = models.BooleanField("کارنامه آموزشی", default=False)
    photo = models.BooleanField("عکس", default=False)
    unit_mental_health_form = models.BooleanField("برگه سلامت روان یگان", default=False)
    five_skills_certificate = models.BooleanField("گواهینامه ۵ گانه", default=False)
    rank_certificate = models.BooleanField("حکم درجه", default=False)
    chip_delivery_form = models.BooleanField("برگه تحویل تراشه", default=False)
    national_card_copy = models.BooleanField("کپی کارت ملی", default=False)
    id_card_copy = models.BooleanField("کپی شناسنامه", default=False)
    spouse_national_card_copy = models.BooleanField("کپی کارت ملی همسر", default=False)
    spouse_id_card_copy = models.BooleanField("کپی شناسنامه همسر", default=False)
    marriage_certificate_copy = models.BooleanField("کپی ۴ صفحه اول سند ازدواج", default=False)
    children_id_card_copy = models.BooleanField("کپی شناسنامه فرزندان", default=False)
    blood_card_or_license = models.BooleanField("کارت خون یا گواهینامه", default=False)
    protection_sheet = models.BooleanField("چهاربرگ (ته برگ حفاظت)", default=False)
    supervision_sheet = models.BooleanField("چهاربرگ (ته برگ نظارت)", default=False)
    ideological_sheet = models.BooleanField("چهاربرگ (ته برگ عقیدتی)", default=False)
    judicial_sheet = models.BooleanField("چهاربرگ (ته برگ قضایی)", default=False)

    def __str__(self):
        return f"مدارک سرباز: {self.soldier}"
