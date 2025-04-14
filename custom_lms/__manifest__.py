{
    'name': 'LMS Extension v2.0 | Mindle',
    'version': '17.0.1.0.0',
    'summary': 'Extends Odoo LMS (website_slides) to add chapter logic',
    'author': 'QuickStart2',
    'category': 'Website',
    'depends': ['website_slides'],
    'data': [
        "views/slide_chapter_views.xml",
        "views/slide_course_views.xml",
        "views/slide_lesson_views.xml",
        'templates/course_templates.xml',
        "templates/custom_slide_main_template.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'custom_lms/static/src/js/course_carousel.js',   
            'custom_lms/static/src/css/course_carousel.css',

        ],
    },
    'installable': True,
    'application': False,
    "auto_install": False,
    'license': 'LGPL-3',
}