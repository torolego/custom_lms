from odoo import http
from odoo.http import request
import os
import logging

# Logger globale
_logger = logging.getLogger(__name__)

# Calcoliamo `module_name` una sola volta e lo rendiamo disponibile in tutto il modulo
MODULE_NAME = os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class ChapterMain_Controller(http.Controller):

    # http://localhost:8069/channel/4
    @http.route(['/channel/<int:channel_id>'], type='http', auth='public', website=True)
    def channel(self, channel_id, **kwargs):
        """Visualizza un canale specifico."""
        channel = request.env['slide.channel'].sudo().browse(channel_id).exists()
        user = request.env.user  # Recupero dell'utente loggato

        return request.render(f'{MODULE_NAME}.custom_slide_main_template', {
            'type': 'channel',
            'object': channel,
            'channel': channel,
            'chapter': None,  # Nessun chapter in questa view
            'user': user
        })

    # http://localhost:8069/channel/chapter/5
    @http.route('/channel/chapter/<int:chapter_id>', type='http', auth='public', website=True)
    def course_chapter(self, chapter_id, **kwargs):
        """Visualizza un capitolo specifico di un canale."""
        
        chapter = request.env['slide.slide'].sudo().browse(chapter_id).exists()

        # Assicurati che il capitolo sia effettivamente una sezione (categoria)
        if not chapter or not chapter.is_category:
            return request.not_found()

        channel = chapter.channel_id.sudo() if chapter.channel_id else None
        user = request.env.user  # Recupero dell'utente loggato

        _logger.info(f"Chapter: {chapter.name}, Channel: {channel.name if channel else 'None'}, User: {user.name}")

        return request.render(f'{MODULE_NAME}.custom_slide_main_template', {
            'type': 'chapter',
            'object': chapter,
            'channel': channel,
            'chapter': chapter,
            'user': user
        })

    #https://mindle-stage17-3-18937827.dev.odoo.com/it/slides/slide/8760-la-gestione-del-tempo-53?fullscreen=1
    # http://localhost:8069/channel/chapter/lesson/81
    @http.route(['/channel/chapter/lesson/<int:lesson_id>'], type='http', auth='public', website=True)
    def lesson(self, lesson_id, **kwargs):
        """Visualizza una lezione specifica."""
        lesson = request.env['slide.slide'].sudo().browse(lesson_id).exists()
        if not lesson:
            return request.not_found()

        chapter = lesson.chapter_id.sudo() if lesson.chapter_id else None
        channel = chapter.channel_id.sudo() if chapter and chapter.channel_id else None
        user = request.env.user  # Recupero dell'utente loggato

        return request.render(f'{MODULE_NAME}.custom_slide_main_template', {
            'type': 'lesson',
            'object': lesson,
            'channel': channel,
            'chapter': chapter,
            'user': user
        })

    # carousels netflix style
    @http.route('/lms/courses', type='http', auth="public", website=True)
    def lms_courses(self):
        channels = request.env['slide.channel'].sudo().search([])
        return request.render(f'{MODULE_NAME}.lms_course_carousel', {
            'channels': channels
        })
