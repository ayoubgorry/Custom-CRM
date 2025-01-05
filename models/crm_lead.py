from odoo import models, fields, api
from datetime import datetime, timedelta

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    feedback_survey_id = fields.Many2one('survey.survey', string='Feedback Survey')
    feedback_submitted = fields.Boolean(string='Feedback Submitted', default=False)
    feedback_score = fields.Float(string='Feedback Score', readonly=True)
    
    def _cron_archive_opportunities(self):
        """Cron job to archive opportunities older than 30 days"""
        deadline = datetime.now() - timedelta(days=30)
        old_opportunities = self.search([
            ('create_date', '<', deadline),
            ('type', '=', 'opportunity'),
            ('active', '=', True)
        ])
        old_opportunities.write({'active': False})

    @api.model
    def create(self, vals):
        """Override create to attach default feedback survey"""
        record = super(CrmLead, self).create(vals)
        if record.type == 'opportunity':
            default_survey = self.env.ref('custom_crm.default_feedback_survey', False)
            if default_survey:
                record.feedback_survey_id = default_survey.id
        return record

    def activity_feedback(self, feedback=None, attachment_ids=None):
        """Override to send feedback survey when activity is marked as done"""
        res = super(CrmLead, self).activity_feedback(feedback=feedback, attachment_ids=attachment_ids)
        if not self.feedback_submitted and self.feedback_survey_id:
            template = self.env.ref('custom_crm.email_template_feedback_request')
            if template:
                template.send_mail(self.id, force_send=True)
        return res

    def process_feedback_submission(self, survey_id, score):
        """Process feedback submission from survey"""
        if self.feedback_survey_id.id == survey_id:
            self.write({
                'feedback_submitted': True,
                'feedback_score': score
            })
