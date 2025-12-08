def genrate_all_report_template():
    totals = {
        'edu': {
            'under_diploma': 0,
            'diploma': 0,
            'associate': 0,
            'bachelor': 0,
            'master': 0,
            'doctor': 0,
        },
        'health': {
            'healthy': 0,
            'exempt_from_service': 0,
            'group_b': 0,
            'exempt_plus_group_b': 0,
        },
        'commission': 0,
        'marital': {
            'single': 0,
            'married': 0,
        },
        'admin': 0,
        'shift': 0,
        'post': 0,
        'native': 0,
        'non_native': 0,
        'total': 0,
    }
    return totals

def generate_difference_report(org, temp):
    """Return difference = org - temp for each category."""

    result = genrate_all_report_template()

    # edu
    for key in result['edu']:
        result['edu'][key] = org['edu'][key] - temp['edu'][key]

    # health
    for key in result['health']:
        result['health'][key] = org['health'][key] - temp['health'][key]

    # commission
    result['commission'] = org['commission'] - temp['commission']

    # marital
    for key in result['marital']:
        result['marital'][key] = org['marital'][key] - temp['marital'][key]

    # traffic
    result['admin'] = org['admin'] - temp['admin']
    result['shift'] = org['shift'] - temp['shift']
    result['post'] = org['post'] - temp['post']

    # native / non-native
    result['native'] = org['native'] - temp['native']
    result['non_native'] = org['non_native'] - temp['non_native']

    # total
    result['total'] = org['total'] - temp['total']

    return result


def generate_all_report(soldiers):
    """Generate statistical report for any queryset of soldiers."""
    totals = {
        'edu': {
            'under_diploma': 0,
            'diploma': 0,
            'associate': 0,
            'bachelor': 0,
            'master': 0,
            'doctor': 0,
        },
        'health': {
            'healthy': 0,
            'exempt_from_service': 0,
            'group_b': 0,
            'exempt_plus_group_b': 0,
        },
        'commission': 0,
        'marital': {
            'single': 0,
            'married': 0,
        },
        'admin': 0,
        'shift': 0,
        'post': 0,
        'native': 0,
        'non_native': 0,
        'total': 0,
    }
    row = {
        'edu': {
            'under_diploma': soldiers.filter(degree__in=['زیر دیپلم', 'زیردیپلم']).count(),
            'diploma': soldiers.filter(degree='دیپلم').count(),
            'associate': soldiers.filter(degree='فوق دیپلم').count(),
            'bachelor': soldiers.filter(degree='لیسانس').count(),
            'master': soldiers.filter(degree='فوق لیسانس').count(),
            'doctor': soldiers.filter(degree__in=['دکترا', 'دکترا پزشکی', 'دکتری']).count(),
        },
        'health': {
            'healthy': soldiers.filter(health_status='سالم').count(),
            'exempt_from_service': soldiers.filter(health_status='معاف از رزم').count(),
            'group_b': soldiers.filter(health_status__in=['گروه ب', 'معاف+گروه ب']).count(),
            'exempt_plus_group_b': soldiers.filter(health_status='معاف+گروه ب').count(),
        },
        'commission': soldiers.filter(status='توجیحی').count(),
        'marital': {
            'single': soldiers.filter(marital_status='مجرد').count(),
            'married': soldiers.filter(marital_status='متاهل').count(),
        },
        'admin': soldiers.filter(traffic_status='اداری').count(),
        'shift': soldiers.filter(traffic_status='شیفتی').count(),
        'post': soldiers.filter(traffic_status='پستی').count(),
        'post': soldiers.filter(traffic_status='پستی').count(),
        'native': soldiers.exclude(residence_province__native=False).count(),
        'non_native': soldiers.filter(residence_province__native=False).count(),
        'total':0
    }

        # جمع کل
    for key, value in row['edu'].items():
        totals['edu'][key] += value
    for key, value in row['health'].items():
        totals['health'][key] += value
    totals['commission'] += row['commission']
    for key, value in row['marital'].items():
        totals['marital'][key] += value
    totals['admin'] += row['admin']
    totals['shift'] += row['shift']
    totals['post'] += row['post']
    totals['native'] += row['native']
    totals['non_native'] += row['non_native']
    totals['total'] += row['total']

    return row
