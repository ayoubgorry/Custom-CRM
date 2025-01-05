from odoo import models, fields, api
from datetime import datetime, timedelta

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    customer_rating = fields.Selection(related='partner_id.customer_rating', string='Note Client', readonly=True)
    last_followup_date = fields.Datetime('Dernier suivi')
    next_followup_date = fields.Datetime('Prochain suivi', compute='_compute_next_followup')
    feedback_received = fields.Boolean('Feedback reçu', default=False)
    feedback_survey_id = fields.Many2one('survey.survey', string='Questionnaire Feedback',
        domain=[('is_feedback_survey', '=', True)])
    feedback_submitted = fields.Boolean('Feedback soumis', default=False)
    feedback_score = fields.Float('Score Feedback', default=0.0)
    lost_reason_detailed = fields.Selection([
        ('price', 'Prix trop élevé'),
        ('communication', 'Manque de communication'),
        ('product', 'Produit inadapté')
    ], string='Raison détaillée de la perte')
    lost_price_difference = fields.Float('Différence de prix (%)')

    @api.depends('last_followup_date')
    def _compute_next_followup(self):
        for lead in self:
            if lead.last_followup_date:
                lead.next_followup_date = lead.last_followup_date + timedelta(days=1)
            else:
                lead.next_followup_date = fields.Datetime.now() + timedelta(days=1)

    def action_set_lost(self):
        action = self.env.ref('custom_crm.action_lost_reason_wizard').read()[0]
        action['context'] = {'default_lead_id': self.id}
        return action

    def mark_followup_done(self):
        self.write({
            'last_followup_date': fields.Datetime.now(),
        })
        # Envoyer un email de confirmation au commercial
        template = self.env.ref('custom_crm.email_template_followup_done')
        for lead in self:
            template.send_mail(lead.id)

    @api.model
    def _cron_opportunity_reminder(self):
        opportunities = self.search([
            ('type', '=', 'opportunity'),
            ('active', '=', True),
            ('stage_id.is_won', '=', False),
            ('feedback_received', '=', False)
        ])

        now = fields.Datetime.now()
        reminder_template = self.env.ref('custom_crm.email_template_opportunity_reminder')
        
        for opp in opportunities:
            days_passed = (now - opp.create_date).days
            if days_passed in [1, 2, 3, 7]:  # 24h, 48h, 72h, 1 semaine
                reminder_template.send_mail(opp.id)

            if days_passed >= 30 and not opp.feedback_received:
                opp.action_archive()
                # Envoyer email d'archivage
                archive_template = self.env.ref('custom_crm.email_template_opportunity_archived')
                archive_template.send_mail(opp.id)

    def action_mark_won(self):
        res = super(CrmLead, self).action_mark_won()
        # Envoyer notification au manager
        template = self.env.ref('custom_crm.email_template_opportunity_won')
        for lead in self:
            template.send_mail(lead.id)
        return res
