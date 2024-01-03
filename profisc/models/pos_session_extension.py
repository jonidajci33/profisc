import logging
import time

import requests
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_res_partner(self):
        params = super(PosSession, self)._loader_params_res_partner()
        params['search_params']['fields'].append("profisc_customer_vat_type")
        return params

    def set_cashbox_pos(self, cashbox_value, notes):
        for session in self:
            super(PosSession, self).set_cashbox_pos(cashbox_value, notes)
            return self.registerCashDeposit(cashbox_value, session)

    def try_cash_in_out(self, _type, amount, reason, extras):
        for session in self:
            super(PosSession, self).try_cash_in_out(_type, amount, reason, extras)
            action = 'DEPOSIT' if _type == 'in' else 'WITHDRAW'
            return self.registerCashDeposit(amount, session, action)

    def post_closing_cash_details(self, counted_cash):
        res = super(PosSession, self).post_closing_cash_details(counted_cash)
        for session in self:
            self.registerCashDeposit(counted_cash, session, 'WITHDRAW')
        return res

    def registerCashDeposit(self, cashbox_value, session, action='INITIAL'):

        request_manager = self.env['request.manager']
        pos_config = session.config_id
        company = self.env['profisc.auth'].get_current_company()
        timestamp = int(time.mktime(session.write_date.timetuple())) * 1000
        payload = {
            "nuis": company.vat,
            "date": timestamp,
            "actionType": action,
            "amount": cashbox_value,
            "subseq": 'none'
        }

        if action == 'INITIAL':
            payload['erp'] = session.name
        if pos_config.bu_code:
            payload['buc'] = pos_config.bu_code
        if pos_config.tcr_code:
            payload['tcr'] = pos_config.tcr_code

        _logger.info('set_cashbox_pos>payload> %s' % payload)
        endpoint = f"{company.profisc_api_endpoint}{company.profisc_cash_deposit}"
        try:

            res = request_manager.post_with_header(endpoint, payload=payload)
            if res:
                _logger.info('set_cashbox_pos>response> %s' % res)
                if res['errorCode'] == 'T044':
                    self.registerCashDeposit(cashbox_value, session, action='DEPOSIT')
                elif res['errorCode'] == 'T043':
                    self.message_post(body='<br/>\n'.join(res['message']))
        except requests.RequestException as e:
            _logger.error('Failed to make request: %s', e)
            raise

    def _loader_params_res_company(self):
        res = super(PosSession, self)._loader_params_res_company()
        res['search_params']['fields'].append('profisc_manual_fisc_select')
        return res
