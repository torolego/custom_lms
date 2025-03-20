from odoo import http
from odoo.http import request

class LMSWebsite(http.Controller):
    @http.route('/lms/courses', type='http', auth="public", website=True)
    def lms_courses(self):
        channels = request.env['slide.channel'].sudo().search([])
        return request.render('lms_carousel.lms_course_carousel', {
            'channels': channels
        })
