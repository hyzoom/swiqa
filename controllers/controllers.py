# -*- coding: utf-8 -*-
from odoo import http

# class Swiqa(http.Controller):
#     @http.route('/swiqa/swiqa/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/swiqa/swiqa/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('swiqa.listing', {
#             'root': '/swiqa/swiqa',
#             'objects': http.request.env['swiqa.swiqa'].search([]),
#         })

#     @http.route('/swiqa/swiqa/objects/<model("swiqa.swiqa"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('swiqa.object', {
#             'object': obj
#         })