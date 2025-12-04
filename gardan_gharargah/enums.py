from enum import Enum
from typing import List, Dict

# -----------------------------
# Action Types
# -----------------------------
class ActionType(Enum):
    DISCIPLINE = "تنبیه"
    REWARD = "تشویق"
# -----------------------------
# Articles (مواد)
# -----------------------------
class Article(Enum):
    ARTICLE_113 = "113"
    ARTICLE_116 = "116"
# -----------------------------
# Clauses (بندها)
# -----------------------------
class Clause(Enum):
    A = "الف"
    B = "ب"
    C = "ج"
    D = "د"
    E = "ه"
    F = "و"
    Z = "ز"
    H = "ح"
    T = "ط"
    Y = "ی"
    K = "ک"
    L = "ل"
    M = "م"
    N = "ن"
    S = "ص"
    ZD = "ض"
    GH = "غ"
    Q = "ق"
# -----------------------------
# Titles (عنوان‌ها)
# -----------------------------
class DisciplinaryTitle(Enum):
    UNIFORM_AND_HYGIENE = "عدم آراستگی و نظافت شخصی"
    RESPECT_AND_ETIQUETTE = "عدم رعایت ادب و سلسله مراتب"
    BAD_BEHAVIOR_TOWARDS_PERSONNEL = "بدرفتاری نسبت به پرسنل جمعی"
    LATE_OR_ABSENCE = "بی توجهی به زمان حضور"
    NON_ESCAPEE_ABSENCE = "غیبت بدون فرار"
    FAKING_ILLNESS = "تمارض و تظاهر به بیماری"
    NEGLECTED_TRAINING = "بی توجهی به آموزش"
    LACK_OF_RESPONSIBILITY = "عدم احساس مسئولیت"
    BREAKING_RULES = "عدم رعایت قوانین و مقررات"
    CARELESSNESS_IN_DUTY = "سستی و سهل انگاری در وظیفه"
    DELAY_AND_INACCURACY = "تاخیر غیرموجه و عدم دقت در گزارش"
    FALSE_REPORTS = "گزارشات و اظهارات خلاف واقع"
    IGNORING_ENEMY_PSYCHE_OPS = "سهل انگاری در مقابله با تبلیغات دشمن"
    SPREADING_RUMORS = "پخش شایعات و تخریب روحیه"
    GUARD_DUTY_NEGLECT = "سهل انگاری در امور نگهبانی و پاسداری"
    EQUIPMENT_MISUSE = "قصور در حفظ تجهیزات و اموال نظامی"
    UNAUTHORIZED_DOCUMENTS = "تسلیم مدارک به افراد غیرمجاز"
    UNMILITARY_BEHAVIOR = "ارتکاب رفتار خلاف شئون نظامی"
    DEFENSE_NEGLECT = "سهل انگاری در بکارگیری توان دفاعی"
    PREVENTION_FAILURE = "قصور در جلوگیری از فرار و پراکندگی پرسنل"
    PROTECTION_FAILURE = "سهل انگاری در حفظ مواضع و مناطق حساس"

class RewardTitle(Enum):
    EXHIBITING_MERIT = "ابراز لیاقت و شایستگی"
    CONTINUOUS_PRESENCE = "حضور مستمر در محل خدمت یا ماموریت"
    EFFECTIVE_SERVICE_EXTRA_TIME = "انجام خدمت موثر خارج از وقت مقرر"
    SPEED_AND_ACCURACY = "سرعت و دقت در اجرای دستورات سلسله مراتب"
    VOLUNTARY_PARTICIPATION = "شرکت داوطلبانه در عملیات مخاطره آمیز و ایثار"
    ROLE_MODEL = "نمونه و سرمشق بودن برای زیردستان"
    MILITARY_EDUCATION_DEVELOPMENT = "اقدامات موثر در توسعه آموزش‌های نظامی"
    PHYSICAL_TRAINING = "اقدامات موثر در پرورش جسمانی کارکنان"
    RESOURCE_MANAGEMENT = "صرفه جویی و ابتکار در مصرف اقلام و تجهیزات"
    PROPERTY_PRESERVATION = "اقدام موثر در حفظ و نگهداری اموال و اسناد نظامی"
    MANAGEMENT_AND_LEADERSHIP = "رعایت اصول مدیریت و روش رهبری"
    PROTECTIVE_SYSTEMS = "بکار بردن ابتکار در سیستم‌های حفاظتی"
    MAINTENANCE_READY_EQUIPMENT = "حفظ و آماده به کار نگه داشتن و تعمیر تجهیزات"
    BOOSTING_MORALE = "ارتقاء روحیه کارکنان"
    IMPROVING_UNIT_CAPACITY = "بالابردن چشمگیر روحیه کارکنان و توان رزمی یگان"
    EFFECTIVE_STAFF_ACTIONS = "اقدامات ستادی موثر و فوق العاده"
    INNOVATION_SELF_SUFFICIENCY = "نوآوری در خودکفایی و استحکامات"
    INTELLIGENCE_AND_PREVENTION = "کسب اخبار و اطلاعات مفید و جلوگیری از شایعات"
    RESISTANCE_IN_CAPTURE = "مقاومت در هنگام اسارت و تلاش برای فرار"
    EXTRAORDINARY_SAVING_LIVES = "تلاش فوق العاده برای نجات جان افراد"
    SUCCESSFUL_DEFENSIVE_MISSIONS = "اجرای موفق ماموریت‌های پدافندی"
    DEFENSIVE_MAINTENANCE = "حفظ مواضع در مقابل دشمن و اسارت دشمن"
    SUCCESSFUL_OFFENSIVE_MISSIONS = "اجرای موفق ماموریت‌های آفندی و ابراز رشادت"

class DisciplinaryRewardActions(Enum):
    # -----------------------------
    # Disciplinary Actions (تنبیهات)
    # -----------------------------
    UNIFORM_AND_HYGIENE = (ActionType.DISCIPLINE, Article.ARTICLE_116, Clause.A, DisciplinaryTitle.UNIFORM_AND_HYGIENE)
    RESPECT_AND_ETIQUETTE = (ActionType.DISCIPLINE, Article.ARTICLE_116, Clause.B, DisciplinaryTitle.RESPECT_AND_ETIQUETTE)
    BAD_BEHAVIOR_TOWARDS_PERSONNEL = (ActionType.DISCIPLINE, Article.ARTICLE_116, Clause.C, DisciplinaryTitle.BAD_BEHAVIOR_TOWARDS_PERSONNEL)
    LATE_OR_ABSENCE = (ActionType.DISCIPLINE, Article.ARTICLE_116, Clause.E, DisciplinaryTitle.LATE_OR_ABSENCE)
    NON_ESCAPEE_ABSENCE = (ActionType.DISCIPLINE, Article.ARTICLE_116, Clause.E, DisciplinaryTitle.NON_ESCAPEE_ABSENCE)
    FAKING_ILLNESS = (ActionType.DISCIPLINE, Article.ARTICLE_116, Clause.F, DisciplinaryTitle.FAKING_ILLNESS)
    NEGLECTED_TRAINING = (ActionType.DISCIPLINE, Article.ARTICLE_116, Clause.D, DisciplinaryTitle.NEGLECTED_TRAINING)
    LACK_OF_RESPONSIBILITY = (ActionType.DISCIPLINE, Article.ARTICLE_116, Clause.Z, DisciplinaryTitle.LACK_OF_RESPONSIBILITY)
    BREAKING_RULES = (ActionType.DISCIPLINE, Article.ARTICLE_116, Clause.Z, DisciplinaryTitle.BREAKING_RULES)
    CARELESSNESS_IN_DUTY = (ActionType.DISCIPLINE, Article.ARTICLE_116, Clause.H, DisciplinaryTitle.CARELESSNESS_IN_DUTY)
    DELAY_AND_INACCURACY = (ActionType.DISCIPLINE, Article.ARTICLE_116, Clause.T, DisciplinaryTitle.DELAY_AND_INACCURACY)
    FALSE_REPORTS = (ActionType.DISCIPLINE, Article.ARTICLE_116, Clause.T, DisciplinaryTitle.FALSE_REPORTS)
    IGNORING_ENEMY_PSYCHE_OPS = (ActionType.DISCIPLINE, Article.ARTICLE_116, Clause.Y, DisciplinaryTitle.IGNORING_ENEMY_PSYCHE_OPS)
    SPREADING_RUMORS = (ActionType.DISCIPLINE, Article.ARTICLE_116, Clause.K, DisciplinaryTitle.SPREADING_RUMORS)
    GUARD_DUTY_NEGLECT = (ActionType.DISCIPLINE, Article.ARTICLE_116, Clause.L, DisciplinaryTitle.GUARD_DUTY_NEGLECT)
    EQUIPMENT_MISUSE = (ActionType.DISCIPLINE, Article.ARTICLE_116, Clause.M, DisciplinaryTitle.EQUIPMENT_MISUSE)
    UNAUTHORIZED_DOCUMENTS = (ActionType.DISCIPLINE, Article.ARTICLE_116, Clause.M, DisciplinaryTitle.UNAUTHORIZED_DOCUMENTS)
    UNMILITARY_BEHAVIOR = (ActionType.DISCIPLINE, Article.ARTICLE_116, Clause.N, DisciplinaryTitle.UNMILITARY_BEHAVIOR)
    DEFENSE_NEGLECT = (ActionType.DISCIPLINE, Article.ARTICLE_116, Clause.S, DisciplinaryTitle.DEFENSE_NEGLECT)
    PREVENTION_FAILURE = (ActionType.DISCIPLINE, Article.ARTICLE_116, Clause.ZD, DisciplinaryTitle.PREVENTION_FAILURE)
    PROTECTION_FAILURE = (ActionType.DISCIPLINE, Article.ARTICLE_116, Clause.GH, DisciplinaryTitle.PROTECTION_FAILURE)

    # -----------------------------
    # Reward Actions (تشویقات)
    # -----------------------------
    EXHIBITING_MERIT = (ActionType.REWARD, Article.ARTICLE_113, Clause.T, RewardTitle.EXHIBITING_MERIT)
    CONTINUOUS_PRESENCE = (ActionType.REWARD, Article.ARTICLE_113, Clause.A, RewardTitle.CONTINUOUS_PRESENCE)
    EFFECTIVE_SERVICE_EXTRA_TIME = (ActionType.REWARD, Article.ARTICLE_113, Clause.A, RewardTitle.EFFECTIVE_SERVICE_EXTRA_TIME)
    SPEED_AND_ACCURACY = (ActionType.REWARD, Article.ARTICLE_113, Clause.E, RewardTitle.SPEED_AND_ACCURACY)
    VOLUNTARY_PARTICIPATION = (ActionType.REWARD, Article.ARTICLE_113, Clause.S, RewardTitle.VOLUNTARY_PARTICIPATION)
    ROLE_MODEL = (ActionType.REWARD, Article.ARTICLE_113, Clause.L, RewardTitle.ROLE_MODEL)
    MILITARY_EDUCATION_DEVELOPMENT = (ActionType.REWARD, Article.ARTICLE_113, Clause.B, RewardTitle.MILITARY_EDUCATION_DEVELOPMENT)
    PHYSICAL_TRAINING = (ActionType.REWARD, Article.ARTICLE_113, Clause.B, RewardTitle.PHYSICAL_TRAINING)
    RESOURCE_MANAGEMENT = (ActionType.REWARD, Article.ARTICLE_113, Clause.C, RewardTitle.RESOURCE_MANAGEMENT)
    PROPERTY_PRESERVATION = (ActionType.REWARD, Article.ARTICLE_113, Clause.D, RewardTitle.PROPERTY_PRESERVATION)
    MANAGEMENT_AND_LEADERSHIP = (ActionType.REWARD, Article.ARTICLE_113, Clause.E, RewardTitle.MANAGEMENT_AND_LEADERSHIP)
    PROTECTIVE_SYSTEMS = (ActionType.REWARD, Article.ARTICLE_113, Clause.F, RewardTitle.PROTECTIVE_SYSTEMS)
    MAINTENANCE_READY_EQUIPMENT = (ActionType.REWARD, Article.ARTICLE_113, Clause.F, RewardTitle.MAINTENANCE_READY_EQUIPMENT)
    BOOSTING_MORALE = (ActionType.REWARD, Article.ARTICLE_113, Clause.F, RewardTitle.BOOSTING_MORALE)
    IMPROVING_UNIT_CAPACITY = (ActionType.REWARD, Article.ARTICLE_113, Clause.Z, RewardTitle.IMPROVING_UNIT_CAPACITY)
    EFFECTIVE_STAFF_ACTIONS = (ActionType.REWARD, Article.ARTICLE_113, Clause.H, RewardTitle.EFFECTIVE_STAFF_ACTIONS)
    INNOVATION_SELF_SUFFICIENCY = (ActionType.REWARD, Article.ARTICLE_113, Clause.Y, RewardTitle.INNOVATION_SELF_SUFFICIENCY)
    INTELLIGENCE_AND_PREVENTION = (ActionType.REWARD, Article.ARTICLE_113, Clause.K, RewardTitle.INTELLIGENCE_AND_PREVENTION)
    RESISTANCE_IN_CAPTURE = (ActionType.REWARD, Article.ARTICLE_113, Clause.M, RewardTitle.RESISTANCE_IN_CAPTURE)
    EXTRAORDINARY_SAVING_LIVES = (ActionType.REWARD, Article.ARTICLE_113, Clause.M, RewardTitle.EXTRAORDINARY_SAVING_LIVES)
    SUCCESSFUL_DEFENSIVE_MISSIONS = (ActionType.REWARD, Article.ARTICLE_113, Clause.N, RewardTitle.SUCCESSFUL_DEFENSIVE_MISSIONS)
    DEFENSIVE_MAINTENANCE = (ActionType.REWARD, Article.ARTICLE_113, Clause.N, RewardTitle.DEFENSIVE_MAINTENANCE)
    SUCCESSFUL_OFFENSIVE_MISSIONS = (ActionType.REWARD, Article.ARTICLE_113, Clause.Q, RewardTitle.SUCCESSFUL_OFFENSIVE_MISSIONS)

from typing import List, Dict
class DisciplinaryRewardActionsHelper:
    # -----------------------------
    # همه موارد به صورت لیست
    # -----------------------------
    @staticmethod
    def items() -> List[DisciplinaryRewardActions]:
        return list(DisciplinaryRewardActions)

    # -----------------------------
    # فقط تنبیهات
    # -----------------------------
    @staticmethod
    def discipline_items() -> List[DisciplinaryRewardActions]:
        return [item for item in DisciplinaryRewardActions if item.value[0] == ActionType.DISCIPLINE]

    # -----------------------------
    # فقط تشویقات
    # -----------------------------
    @staticmethod
    def reward_items() -> List[DisciplinaryRewardActions]:
        return [item for item in DisciplinaryRewardActions if item.value[0] == ActionType.REWARD]

    # -----------------------------
    # موارد به صورت آرایه از دیکشنری‌ها
    # -----------------------------
    @staticmethod
    def obj_items() -> List[Dict]:
        return [
            {
                "type": item.value[0],
                "label": item.value[3].value,
                "clause": item.value[2].value,
                "article": item.value[1].value
            }
            for item in DisciplinaryRewardActions
        ]

    @staticmethod
    def discipline_obj_items() -> List[Dict]:
        return [
            {
                "type": item.value[0],
                "label": item.value[3].value,
                "clause": item.value[2].value,
                "article": item.value[1].value
            }
            for item in DisciplinaryRewardActions if item.value[0] == ActionType.DISCIPLINE
        ]

    @staticmethod
    def reward_obj_items() -> List[Dict]:
        return [
            {
                "type": item.value[0],
                "label": item.value[3].value,
                "clause": item.value[2].value,
                "article": item.value[1].value
            }
            for item in DisciplinaryRewardActions if item.value[0] == ActionType.REWARD
        ]

    # -----------------------------
    # فیلتر بر اساس نوع
    # -----------------------------
    @staticmethod
    def filter_by_type(action_type: ActionType) -> List[DisciplinaryRewardActions]:
        return [item for item in DisciplinaryRewardActions if item.value[0] == action_type]

    # -----------------------------
    # فیلتر بر اساس ماده
    # -----------------------------
    @staticmethod
    def filter_by_article(article: Article) -> List[DisciplinaryRewardActions]:
        return [item for item in DisciplinaryRewardActions if item.value[1] == article]

    # -----------------------------
    # فیلتر بر اساس بند
    # -----------------------------
    @staticmethod
    def filter_by_clause(clause: Clause) -> List[DisciplinaryRewardActions]:
        return [item for item in DisciplinaryRewardActions if item.value[2] == clause]

    # -----------------------------
    # فیلتر بر اساس عنوان
    # -----------------------------
    @staticmethod
    def filter_by_title(title: Enum) -> List[DisciplinaryRewardActions]:
        return [item for item in DisciplinaryRewardActions if item.value[3] == title]
