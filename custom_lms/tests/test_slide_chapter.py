from odoo.tests import TransactionCase

class TestSlideChapter(TransactionCase):
    def setUp(self):
        super().setUp()
        self.course = self.env['slide.channel'].create({'name': 'Test Course'})
        self.chapter = self.env['slide.chapter'].create({'name': 'Test Chapter', 'course_id': self.course.id})
        self.lesson = self.env['slide.slide'].create({'name': 'Test Lesson', 'chapter_id': self.chapter.id})

    def test_chapter_creation(self):
        self.assertEqual(self.chapter.course_id, self.course)
        self.assertIn(self.lesson, self.chapter.lesson_ids)
