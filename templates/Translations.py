"""
Simple translation dictionary — Hindi / Marathi / English.

Naya text add karna ho toh bas TRANSLATIONS dict mein teeno languages
ke liye ek entry daal do, phir template mein {{ t('key_name') }} likh do.

Naya language add karna ho (e.g. Punjabi):
1. TRANSLATIONS ke har key mein 'pa': '...' add karo
2. LANGUAGES list mein ('pa', 'ਪੰਜਾਬੀ') add karo
"""

LANGUAGES = [
    ('hi', 'हिंदी'),
    ('mr', 'मराठी'),
    ('en', 'English'),
]

TRANSLATIONS = {
    # ── Navbar / Sidebar ──
    'nav_dashboard':   {'hi': 'डैशबोर्ड',          'mr': 'डॅशबोर्ड',           'en': 'Dashboard'},
    'nav_profile':     {'hi': 'मेरी प्रोफ़ाइल',      'mr': 'माझी प्रोफाइल',       'en': 'My Profile'},
    'nav_weather':     {'hi': 'मौसम',              'mr': 'हवामान',              'en': 'Weather'},
    'nav_crop':        {'hi': 'फसल गाइड',           'mr': 'पीक मार्गदर्शन',       'en': 'Crop Guide'},
    'nav_pest':        {'hi': 'कीट पहचान',          'mr': 'कीड ओळख',            'en': 'Pest Detection'},
    'nav_chatbot':     {'hi': 'एआई चैटबॉट',         'mr': 'एआय चॅटबॉट',          'en': 'AI Chatbot'},
    'nav_market':      {'hi': 'मंडी भाव',            'mr': 'बाजार भाव',           'en': 'Market Prices'},
    'nav_expense':     {'hi': 'खर्च ट्रैकर',          'mr': 'खर्च ट्रॅकर',          'en': 'Expense Tracker'},
    'nav_schemes':     {'hi': 'सरकारी योजनाएँ',      'mr': 'सरकारी योजना',        'en': 'Govt Schemes'},
    'nav_tips':        {'hi': 'खेती सुझाव',          'mr': 'शेती टिप्स',          'en': 'Farming Tips'},
    'sign_in':         {'hi': 'लॉगिन करें',          'mr': 'लॉगिन करा',           'en': 'Sign In'},
    'sign_out':        {'hi': 'लॉगआउट',             'mr': 'लॉगआउट',             'en': 'Sign Out'},
    'get_started':     {'hi': 'शुरू करें →',          'mr': 'सुरू करा →',          'en': 'Get Started →'},

    # ── Common actions ──
    'listen':          {'hi': '🔊 सुनें',            'mr': '🔊 ऐका',              'en': '🔊 Listen'},
    'ask_ai_voice':    {'hi': '🎤 बोलकर पूछें',      'mr': '🎤 बोलून विचारा',      'en': '🎤 Ask by Voice'},
    'save':            {'hi': 'सेव करें',            'mr': 'सेव्ह करा',           'en': 'Save'},

    # ── Dashboard quick-access ──
    'todays_weather':  {'hi': 'आज का मौसम',         'mr': 'आजचे हवामान',         'en': "Today's Weather"},
    'my_crop':         {'hi': 'मेरी फसल',            'mr': 'माझे पीक',            'en': 'My Crop'},
    'crop_problem':    {'hi': 'फसल में समस्या',      'mr': 'पिकातील समस्या',       'en': 'Crop Problem'},
    'water_info':      {'hi': 'पानी की जानकारी',     'mr': 'पाण्याची माहिती',      'en': 'Water Info'},
    'todays_price':    {'hi': 'आज का भाव',           'mr': 'आजचा भाव',            'en': "Today's Price"},
}


def get_translator(lang):
    """Returns a function t(key) that looks up the string for given lang."""
    if lang not in ('hi', 'mr', 'en'):
        lang = 'hi'

    def t(key):
        entry = TRANSLATIONS.get(key)
        if not entry:
            return key  # fallback — key hi dikha do taaki missing translation turant pata chale
        return entry.get(lang, entry.get('hi', key))

    return t