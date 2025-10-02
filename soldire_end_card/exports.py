import io
import zipfile
import os
import pandas as pd

from django.shortcuts import get_object_or_404
from soldires_apps.models import Soldier
from .models import CardSend, CardSeries
from soldier_service_apps.models import SoldierService

def get_soldiers_info_for_series(series_id):
    # دریافت سری کارت
    series = get_object_or_404(CardSeries, id=series_id)
    
    # دریافت کارت‌های سری به همراه سرباز و سرویسش
    card_sends = CardSend.objects.filter(series=series).select_related(
        'soldier', 'soldier__soldierservice'
    ).order_by('-created_at')
    
    soldiers_data = []

    for card in card_sends:
        soldier = card.soldier
        service = getattr(soldier, 'soldierservice', None)
        
        data = {
            "first_name": f"{soldier.first_name}",
            "last_name": f"{soldier.last_name}",
            "full_name": f"{soldier.first_name} {soldier.last_name}",
            "national_code": soldier.national_code,
            "father_name": soldier.father_name,
            "id_card_code": soldier.id_card_code,
            "birth_date": soldier.birth_date,
            "birth_place": soldier.birth_place,
            "issuance_place": soldier.issuance_place,
            "rank": soldier.rank,
            "dispatch_date": soldier.dispatch_date,
            "service_end_date": soldier.service_end_date,
            "total_service_adjustment": soldier.total_service_adjustment,
            "service_deduction_type": soldier.service_deduction_type,
            "service_extension_type": soldier.service_extension_type,
            "address": soldier.address,
            "phone_mobile": soldier.phone_mobile,
            "postal_code": soldier.postal_code,
            "is_sayyed": soldier.is_sayyed,
            "photo_scan": soldier.photo_scan.url if soldier.photo_scan else None,
        }

        # اطلاعات کسری و اضافه خدمت
        if service:
            data.update({
                "reduction_veterans": service.reduction_veterans,
                "reduction_disability": service.reduction_disability,
                "reduction_bsj": service.reduction_bsj,
                "reduction_project": service.reduction_project,
                "reduction_children": service.reduction_children,
                "reduction_spouse": service.reduction_spouse,
                "reduction_operational_areas": service.reduction_operational_areas,
                "reduction_seniority": service.reduction_seniority,
                "reduction_non_local": service.reduction_non_local,
                "reduction_system_adjustment": service.reduction_system_adjustment,
                "reduction_other": service.reduction_other,
                "reduction_total": service.reduction_total,
                "addition_seniority": service.addition_seniority,
                "addition_discipline": service.addition_discipline,
                "addition_gap": service.addition_gap,
                "addition_system": service.addition_system,
                "addition_other": service.addition_other,
                "addition_total": service.addition_total,
            })

        soldiers_data.append(data)
    
    return soldiers_data

# -----------------------------
# 1. تولید Excel
# -----------------------------
def generate_excel(soldiers_data):
    # فقط ستون‌های لازم را انتخاب می‌کنیم
    df = pd.DataFrame([
        {
            "کد ملی": s["national_code"],
            "نام": s["full_name"].split(" ")[0],
            "نام خانوادگی": " ".join(s["full_name"].split(" ")[1:]),
            "پست": s.get("position", ""),
            "تاریخ اعزام": s.get("dispatch_date", ""),
            "تاریخ پایان": s.get("service_end_date", ""),
        }
        for s in soldiers_data
    ])
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    return buffer

# -----------------------------
# 2. تولید Nzsa (XML)
# -----------------------------
def generate_nzsa_xml(soldiers_data):
    """
    تولید فایل NZSA (XML) برای لیست سربازان
    soldiers_data: لیستی از دیکشنری‌های سرباز (از get_soldiers_info_for_series)
    """
    def format_date(d):
        return d.strftime("%Y/%m/%d") if d else ""

    xml_lines = ['<?xml version="1.0" encoding="utf-8"?>', '<NewDataSet>']

    for s in soldiers_data:
        xml_lines.append("  <P>")
        xml_lines.append(f"    <m_iTxtSalaryNumber>{s.get('id_card_code','')}</m_iTxtSalaryNumber>")
        xml_lines.append(f"    <m_sTxtFirstName>{s.get('first_name','')}</m_sTxtFirstName>")
        xml_lines.append(f"    <m_sTxtLastName>{s.get('last_name','')}</m_sTxtLastName>")
        xml_lines.append(f"    <m_sTxtFatherName>{s.get('father_name','')}</m_sTxtFatherName>")
        xml_lines.append(f"    <m_sTxtIdCard>{s.get('national_code','')}</m_sTxtIdCard>")
        xml_lines.append(f"    <m_sTxtExportPlace>{s.get('issuance_place','')}</m_sTxtExportPlace>")
        xml_lines.append(f"    <m_iTxtBirthYear>{s.get('birth_date').year if s.get('birth_date') else ''}</m_iTxtBirthYear>")
        xml_lines.append(f"    <m_sTxtBirthPlace>{s.get('birth_place','')}</m_sTxtBirthPlace>")
        xml_lines.append(f"    <m_sCmbEdjRate>{s.get('degree','')}</m_sCmbEdjRate>")
        xml_lines.append(f"    <m_sCmbColorEye>{s.get('eye_color','')}</m_sCmbColorEye>")
        xml_lines.append(f"    <m_sCmbBloodGroup>{s.get('blood_group','')}</m_sCmbBloodGroup>")
        xml_lines.append(f"    <m_iTxtLength>{s.get('height','')}</m_iTxtLength>")
        xml_lines.append(f"    <m_sCmbMemberType>{s.get('rank','')}</m_sCmbMemberType>")
        xml_lines.append(f"    <m_sCmbGrade>{s.get('grade','')}</m_sCmbGrade>")
        xml_lines.append(f"    <m_sCmbMilitaryGroup>{s.get('skill_group','')}</m_sCmbMilitaryGroup>")
        xml_lines.append(f"    <m_TinyTxtMilitaryMonth>{s.get('training_duration','')}</m_TinyTxtMilitaryMonth>")
        xml_lines.append(f"    <m_sTxtStartDate>{format_date(s.get('dispatch_date'))}</m_sTxtStartDate>")
        xml_lines.append(f"    <m_sTxtEndDate>{format_date(s.get('service_end_date'))}</m_sTxtEndDate>")
        xml_lines.append(f"    <m_TinyTxtDidMonth>{s.get('addition_total',0)}</m_TinyTxtDidMonth>")
        xml_lines.append(f"    <m_TinyTxtDidDay>{s.get('addition_days',0)}</m_TinyTxtDidDay>")
        xml_lines.append(f"    <m_iTxtBaseNumber>{s.get('national_code','')}</m_iTxtBaseNumber>")
        xml_lines.append(f"    <m_sTxtGuideCenter>{s.get('basic_training_center','')}</m_sTxtGuideCenter>")
        xml_lines.append(f"    <m_sTxtSender>{s.get('sender','')}</m_sTxtSender>")
        xml_lines.append(f"    <m_sTxtRegion>{s.get('current_parent_unit','')}</m_sTxtRegion>")
        xml_lines.append(f"    <m_sTxtDesc>{s.get('reduction_total','')}</m_sTxtDesc>")
        xml_lines.append(f"    <m_Tell>{s.get('phone_home','')}</m_Tell>")
        xml_lines.append(f"    <m_Cell>{s.get('phone_mobile','')}</m_Cell>")
        xml_lines.append(f"    <m_Email>{s.get('saman_username','')}</m_Email>")
        xml_lines.append(f"    <m_Address>{s.get('address','')}</m_Address>")
        photo = s.get('photo_scan','')
        xml_lines.append(f"    <m_Pic>{os.path.basename(photo) if photo else ''}</m_Pic>")

        # فیلدهای کامل کسری و اضافه خدمت
        reduction_fields = [
            "KasrTamdidi", "KasrRazmandegan", "KasrJanbazan", "KasrBasij",
            "KasrMahroom", "KasrAmaliati", "KasrGhabli", "KasrTahsili",
            "KasrOlad", "KasrTaahol", "KasreGheireBoomi", "KasrTalfighi",
            "KasrSanavati", "EzafeSanavati", "EzafeDadsara", "Khala",
            "KasrNokhbegan", "KasrAzade", "KasrAbhava", "EzafeYegani"
        ]
        for field in reduction_fields:
            xml_lines.append(f"    <m_{field}>{s.get(field,0)}</m_{field}>")

        # سایر فیلدهای تکمیلی
        xml_lines.append(f"    <m_RegionCode>10375 </m_RegionCode>")
        xml_lines.append(f"    <m_CodePosti>{s.get('postal_code','')}</m_CodePosti>")
        xml_lines.append(f"    <m_KindRahaee>{s.get('kind_rahaee','کارت پايان خدمت')}</m_KindRahaee>")
        xml_lines.append(f"    <m_MoafRazm>{s.get('moaf_razm',False)}</m_MoafRazm>")
        xml_lines.append(f"    <m_Kefayat>{s.get('kefayat',False)}</m_Kefayat>")

        xml_lines.append("  </P>")

    xml_lines.append("</NewDataSet>")
    return "\n".join(xml_lines).encode("utf-8")
# -----------------------------
# 3. افزودن تصاویر سربازان به ZIP
# -----------------------------
def add_soldier_pics_to_zip(zf, card_sends, pic_folder):
    pic_zip_folder = "Pic/"
    
    zf.writestr(pic_zip_folder, "")
    for c in card_sends:
        soldier = c.soldier
        pic_path = os.path.join(pic_folder, f"{soldier.national_code}.JPG")
        if os.path.exists(pic_path):
            # فقط سربازان موجود در card_sends اضافه می‌شوند
            zf.write(pic_path, arcname=os.path.join(pic_zip_folder, f"{soldier.national_code}.JPG"))

# -----------------------------
# 4. تابع اصلی ساخت ZIP
# -----------------------------
def generate_series_zip(series, card_sends, pic_folder):
    soldiers_data = get_soldiers_info_for_series(series.id)
    excel_buffer = generate_excel(soldiers_data)
    xml_content = generate_nzsa_xml(soldiers_data)
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        # اضافه کردن Excel
        zf.writestr(f"{series.title}_soldiers.xlsx", excel_buffer.getvalue())

        # اضافه کردن Nzsa
        zf.writestr(f"data.nzsa", xml_content)

        # اضافه کردن تصاویر
        add_soldier_pics_to_zip(zf, card_sends, pic_folder)

    zip_buffer.seek(0)
    return zip_buffer
