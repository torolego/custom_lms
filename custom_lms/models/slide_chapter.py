#Custom html out-raw
import html
import re
from odoo import models, fields, api


#custom html out-raw
from markupsafe import Markup
from odoo.tools.safe_eval import safe_eval


# ==================================================================================================================
# CORSO | COURSE aka (ODOO.LMS)(WEBSITE_SLIDES) "CHANNEL" > LEVEL 1
# ==================================================================================================================

class SlideChannel(models.Model):
    _inherit = 'slide.channel'

    # | LEVEL 1 | THIS OBJECT|
    # channel_id = fields.Many2one('slide.channel', string="Course", required=True, ondelete='cascade')

# relazione con SLIDES: slide.slide
# ==================================================================================================================

    # | LEVEL 2 |  CAPITOLI (CHAPTERS)

    # slide_category_ids = fields.One2many('slide.slide', string='Categories Chapthers', compute="_compute_category_and_slide_ids")
    
    # | LEVEL 3 | ASSOCIAZIONE ALLE LEZIONI (LESSONS) | RELAZIONE ONE2MANY
   
        # CAPITOLI (CHAPTERS) E LEZIONI (LESSONS)
  
    chapter_ids = fields.One2many('slide.slide', 'channel_id', string="Slides and categories (Chapters)", copy=True)
    # slide_ids = fields.One2many('slide.slide', 'channel_id', string="Slides and categories (Chapters)", copy=True)

        # CONTENUTI (LESSONS & CHAPTERS & CATEGORIES)

     # slide_content_ids = fields.One2many('slide.slide', string='Content', compute="_compute_category_and_slide_ids")

# ==================================================================================================================

    short_description = fields.Html(
        string="Descrizione Breve",
        compute="_compute_short_description",
        store=True,  # Opzionale: memorizza il valore nel database
    )

    @api.depends('description')
    def _compute_short_description(self):
        for record in self:
            
            if record.description and len(record.description) > 30:
                record.short_description = Markup(html.unescape(self.description[:30])) + '...'
                #record.short_description = record.description[:30] + '...'
            else:
                record.short_description = record.description or "Nessuna descrizione disponibile"

    

    # CUSTOM HTML SECTION (PRE-MAIN CONTENT | PRE-HOME SECTION)
    # ==================================================================================================================
    custom_html_code = fields.Html(string="Codice HTML Personalizzato", sanitize=False)
    #20250213 Custom Aggiunta function pwe markare come sicuri i contenuti html
    def get_safe_html(self):    
        if self.custom_html_code:
            return Markup(html.unescape(self.custom_html_code or ""))
            # return Markup(safe_eval(self.custom_html_code, {})) KO
        return ""
    # ==================================================================================================================


# OPEN POINT ?
# E NECESSARIO DEFINIRE UN OGGETTO CAPITOLO O E SUFFICIENTE SLIDE.SLIDE SIA PER LEZIONI CHE CAPITOLI (CATEGORIE/SEZIONI) ?
# IN TAL CASO IN COSA VA ESTESO ?

# ==================================================================================================================
# CAPITOLO | CHAPTER aS (ODOO.LMS)(WEBSITE_SLIDES) "SLIDE" (SECTION > IS_CATEGORY=TRUE) > LEVEL 2
# ==================================================================================================================

class SlideChapter(models.Model):
   # _name = 'slide.chapter'  # Nome tecnico del nuovo modello
    _inherit = 'slide.slide'  # Eredita da slide.slide
    _description = "Course Chapter"

    name = fields.Char('Title', required=True, translate=False)  # ❌ Rimuoviamo la traduzione
    #slide_id = fields.Many2one('slide.slide', string="Content", ondelete="cascade", index=True, required=True)

  #  name_string = fields.Char(
  #      string="Name String",
  #      compute="_compute_name_string",
  #      store=False
  #  )

 #   @api.depends('name')
 #   def _compute_name_string(self):
 #       for record in self:
 # 
   
    # | LEVEL 1 |  ASSOCIAZIONE AL CORSO
    # channel_id = fields.Many2one('slide.channel', string="Course", required=True, ondelete='cascade')

    # | LEVEL 2 | THIS OBJECT| POLIMORFISMO SU SLIDE (CONTENUTO) DEL CORSO COME RAGGRUPPAMENTO DI ALTRE SLIDES/CONTENUTI
    is_category = fields.Boolean(default=True)  # Rende il capitolo una categoria/sezione

    # | LEVEL 3  | ASSOCIAZIONE ALLE LEZIONI (LESSONS) | RELAZIONE ONE2MANY
    #slide_ids = fields.One2many('slide.slide', "category_id", string="Content")
    lesson_ids = fields.One2many('slide.slide', "category_id", string="Lessons")

    #TODO da verifcare eventuale Grouping di capitolo se renderlo possibile o evotarlo (quindi codifiare controllo)
    #category_id = fields.Many2one("slide.slide", string="Section")  # Relazione gerarchica
    #category_id = fields.Many2one("slide.slide", string="Chapter")  # Relazione gerarchica

    # ALTRI ATTRIBUTI
    #===========================================================================
    #name = fields.Char('Title', required=True, translate=True)
    #description = fields.Html('Description', translate=True, sanitize_attributes=False, sanitize_overridable=True)
   
    #image_1920 = fields.Image(compute="_compute_image_1920", store=True, readonly=False)  # image.mixin override
    #active = fields.Boolean(default=True, tracking=100)
    #sequence = fields.Integer('Sequence', default=0)
    #user_id = fields.Many2one('res.users', string='Uploaded by', default=lambda self: self.env.uid)
    #===========================================================================   

    description = fields.Char(string="Descrizione", default="Description Course Chapter")
    description_html = fields.Html(
        string="Desc. HTML",
        sanitize=False,
        default="<p>Descrizione HTML di default per il capitolo del corso.</p>"
    )

    # Funzione per rendere sicura la descrizione HTML
    def get_safe_description(self):    
        if self.description_html:
            return Markup(html.unescape(self.description_html or ""))
        return ""


    # DA VERIFICARE SE ANCORA NECESSARIO
    #===========================================================================
    # Rinomina channel_id per mantenere la compatibilità
    #channel_id = fields.Many2one("slide.channel", string="Course", required=True)

    # Rinomina il campo Many2many per evitare conflitti
    chapter_tag_ids = fields.Many2many(
        'slide.tag',  # Modello relazionato
        'slide_chapter_tag_rel',  # Nome della tabella di relazione
        'chapter_id',  # Nome della colonna per slide.chapter
        'tag_id',  # Nome della colonna per slide.tag
        string='Chapter Tags'
    )

    progress = fields.Float(
        string="Progress (%)",
         compute="_compute_progress",
         store=True,
         default=0.0
     )

    @api.depends('slide_ids.completed')
    def _compute_progress(self):
         for chapter in self:
             total_lessons = len(chapter.slide_ids)
             if total_lessons > 0:
                 completed_lessons = sum(lesson.completed for lesson in chapter.slide_ids)
                 chapter.progress = (completed_lessons / total_lessons) * 100
             else:
                 chapter.progress = 0.0
    #===========================================================================



# ==================================================================================================================
# LEZIONE SINGOLA | LESSON aka (ODOO.LMS)(WEBSITE_SLIDES) "SLIDE"  (IS_CATEGORY=FALSE) | LEVEL 3
# ==================================================================================================================
class SlideLesson(models.Model):
    _inherit = 'slide.slide'
 
    #_name = 'slide.slide'
    name = fields.Char('Title', required=True, translate=False)  #  Rimossa la traduzione

  #  name_string = fields.Char(
  #      string="Name String",
  #      compute="_compute_name_string",
  #      store=False
  #  )

 #   @api.depends('name')
 #   def _compute_name_string(self):
 #       for record in self:
 #           record.name_string = str(record.name) if record.name else "No Name" 




    # | LEVEL 1 |  ASSOCIAZIONE AL CORSO
    # channel_id = fields.Many2one('slide.channel', string="Course", required=True, ondelete='cascade')

    # | LEVEL 2 | Capitolo | Sezione (Categoria)
    category_id = fields.Many2one('slide.slide', string="Chapter", compute="_compute_category_id", store=True)
    
    # | LEVEL 3  | THIS OBJECT ASSOCIAZIONE ALLE LEZIONI (LESSONS) | RELAZIONE ONE2MANY  
    is_category = fields.Boolean(default=False)  # Rende il Lezione una slide 'foglia" NON categoria/sezione
    
    # ALTRI ATTRIBUTI
    #===========================================================================
    #name = fields.Char('Title', required=True, translate=True)
    #description = fields.Html('Description', translate=True, sanitize_attributes=False, sanitize_overridable=True)
   
    #image_1920 = fields.Image(compute="_compute_image_1920", store=True, readonly=False)  # image.mixin override
    #active = fields.Boolean(default=True, tracking=100)
    #sequence = fields.Integer('Sequence', default=0)
    #user_id = fields.Many2one('res.users', string='Uploaded by', default=lambda self: self.env.uid)
    #===========================================================================   

    # business field
    completed = fields.Boolean(string="Completed", default=False)
    image = fields.Binary(string="Lesson Image")
    description = fields.Text(string="Short Description")
    slug = fields.Char(compute="_compute_slug", store=True)
    
    @api.depends('name')
    def _compute_slug(self):
        for slide in self:
            slide.slug = re.sub(r'[^a-zA-Z0-9]+', '-', slide.name).strip('-').lower()


    # Funzione per rendere sicura la descrizione HTML
    def get_safe_description(self):    
        if self.description:
            return Markup(html.unescape(self.description or ""))
        return ""


class SlideSlide(models.Model):
    _inherit = 'slide.slide'

    def open_slide_form(self):
        """Apre la vista corretta in base al tipo di elemento"""
        self.ensure_one()

        # Controllo per verificare il valore di is_category
        if not self.is_category:
            return

        view_id = 'custom_lms.view_slide_chapter_form' if self.is_category else 'custom_lms.view_slide_lesson_form'
        
        return {
            'name': "Edit Slide",
            'type': 'ir.actions.act_window',
            'res_model': 'slide.slide',
            'view_mode': 'form',
            'res_id': self.id,
            'view_id': self.env.ref(view_id).id,
            'target': 'current'
        }

    description_html = fields.Html(
        string="Desc. HTML",
        sanitize=False,
        default="<p>Descrizione <strong>HTML</strong></p>"
    )

    # Funzione per rendere sicura la descrizione HTML
    def get_safe_description(self):    
        if self.description_html:
            return Markup(html.unescape(self.description_html or ""))
        return ""

    # Rinomina il campo Many2many per evitare conflitti
    tag_ids = fields.Many2many(
            'slide.tag',  # Modello relazionato
            'slide_slide_tag_rel',  # Nome della tabella di relazione
            'slide_id',  # Nome della colonna per slide.slide
            'tag_id',  # Nome della colonna per slide.tag
            string='Tags'
        )
