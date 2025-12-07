from django.shortcuts import render

# Create your views here.
def guard_dashboard(request):
    entry_exit_acions  = [
        { "label": "دانلود اکسل", "icon": "📥", "base": "export_soldiers","disabled":True,'show':False },
        { "label": "چاپ", "icon": "🖨️", "base": "export_soldiers" ,"disabled":True,'show':False},
        { "label": "مشاهده", "icon": "👁️", "base": "soldier_list" ,"disabled":True,'show':True},
    ]
    # blue green red purple yellow
    analytics = [
        {
            "col": 6,
            "label": "ورود و خروج دژبانی (امروز)",
            "gradient": "gradient-red",
            "count": 'حاضرین و غائبین',
            "query": "",
            "itemsCol":4,
            "actions": entry_exit_acions,
            "items": [
                # ورود
                {"label": "ورود حاضر", "count": 0},
                {"label": "ورود غائب", "count": 0},
                {"label": "ورود تاخیر", "count": 0},

                # خروج
                {"label": "خروج حاضر", "count": 0},
                {"label": "خروج غائب", "count": 0},
                {"label": "خروج تاخیر", "count": 0},

                # حاضرین
                {"label": "حاضرین حاضر", "count": 0},
                {"label": "حاضرین غائب", "count": 0},
                {"label": "حاضرین تاخیر", "count": 0},
            ]


        },        
        {
            "col": 6,
            "label": "ورود و خروج دژبانی (امروز)",
            "gradient": "gradient-blue",
            "count": 'اشخاص و وسیله نقلیه',
            "query": "",
            "itemsCol":6,
            "actions": entry_exit_acions,
            "items": [
                {"label": "ورود اشخاص", "count": 0},
                {"label": "ورود وسیله نقلیه", "count": 0},
                {"label": "خروج اشخاص", "count": 0},
                {"label": "خروج وسیله نقلیه", "count": 0},
                {"label": "حاضرین اشخاص", "count": 0},
                {"label": "حاضرین وسیله نقلیه", "count": 0},
            ],
            
        },
        {
            "col": 6,
            "label": "ورود و خروج دژبانی (امروز)",
            "gradient": "gradient-green",
            "count": 'وضعیت تردد',
            "query": "",
            "itemsCol":4,
            "actions": entry_exit_acions,
            "items": [
                # ورود
                {"label": "ورود اداری", "count": 0},
                {"label": "ورود شیفتی", "count": 0},
                {"label": "ورود پستی", "count": 0},

                # خروج
                {"label": "خروج اداری", "count": 0},
                {"label": "خروج شیفتی", "count": 0},
                {"label": "خروج پستی", "count": 0},

                # حاضرین
                {"label": "حاضرین اداری", "count": 0},
                {"label": "حاضرین شیفتی", "count": 0},
                {"label": "حاضرین پستی", "count": 0},
            ]

        },
        {
            "col": 6,
            "label": "ورود و خروج دژبانی (امروز)",
            "gradient": "gradient-purple",
            "count": 'وضعیت سلامت',
            "query": "",
            "itemsCol":4,
            "actions": entry_exit_acions,
            "items": [
                # ورود
                {"label": "ورود سالم", "count": 0},
                {"label": "ورود معاف از رزم", "count": 0},
                {"label": "ورود گروه ب", "count": 0},
                # خروج
                {"label": "خروج سالم", "count": 0},
                {"label": "خروج معاف از رزم", "count": 0},
                {"label": "خروج گروه ب", "count": 0},
                # حاضرین
                {"label": "حاضرین سالم", "count": 0},
                {"label": "حاضرین معاف از رزم", "count": 0},
                {"label": "حاضرین گروه ب", "count": 0},
            ]

        },
    ]
    context={
        'analytics':analytics,
    }
    return render(request,'gurd_apps/gurd_dashboard.html',context)


def guard_corrections(request):
    context={
    }    
    return render(request,'gurd_apps/guard_corrections.html',context)
