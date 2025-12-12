from odoo import models, fields, api

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'date_published desc, name'

    # --- 基本信息 ---
    name = fields.Char(string='Title', required=True)
    author = fields.Char(string='Author')
    isbn = fields.Char(string='ISBN', help="International Standard Book Number")
    date_published = fields.Date(string='Date Published')
    category = fields.Selection([
        ('fiction', 'Fiction'),
        ('nonfiction', 'Non-fiction'),
        ('science', 'Science'),
        ('biography', 'Biography'),
        ('other', 'Other'),
    ], string='Category', default='other')

    # --- 扩展信息 ---
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)

    # --- 自动计算字段示例 ---
    age_in_years = fields.Integer(
        string='Age (Years)',
        compute='_compute_age_in_years',
        store=True
    )

    @api.depends('date_published')
    def _compute_age_in_years(self):
        """计算图书出版至今的年数"""
        for record in self:
            if record.date_published:
                delta = fields.Date.today() - record.date_published
                record.age_in_years = delta.days // 365
            else:
                record.age_in_years = 0

    # --- 示例按钮行为 ---
    def action_mark_old_books(self):
        """示例动作：将出版超过10年的书标记为不活跃"""
        old_books = self.filtered(lambda b: b.age_in_years > 10)
        old_books.write({'active': False})
        return True
