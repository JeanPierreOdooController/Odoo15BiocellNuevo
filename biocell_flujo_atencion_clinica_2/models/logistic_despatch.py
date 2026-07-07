from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
class LogisticDespatch(models.Model):
    _inherit="logistic.despatch"
    
    tracking_update_bio_nota=fields.Boolean("",tracking=True)
    
    def update_bio_nota_logistic(self):
        
        if not self.picking_ids:
            return
        self.tracking_update_bio_nota= not self.tracking_update_bio_nota
        picking=self.picking_ids[0]
        partner=picking.picking_type_id.warehouse_id.partner_id
        oc_com_eqc= (partner.street_name or '') \
                    + (partner.street_number and (' ' + partner.street_number) or '') \
                    + (partner.street_number2 and (' ' + partner.street_number2) or '') \
                    + (partner.street2 and (' ' + partner.street2) or '') \
                    + (partner.district_id and ', ' + partner.district_id.name or '') \
                    + (partner.city_id and ', ' + partner.city_id.name or '') \
                    + (partner.state_id and ', ' + partner.state_id.name or '') \
                    + (partner.country_id and ', ' + partner.country_id.name or '')
        self.bio_nota = f"""<table width="100%" border="0" cellpadding="2" cellspacing="0">
			<colgroup>
				<col width="50%"/>
				<col width="50%"/>
			</colgroup>
			<tbody>
				<tr>
					<td style="vertical-align: top;">
						<strong>Código Cirugía: </strong>{picking.cod_cirugia or ''}<br/>
						<strong>Fecha de Cirugía: </strong>{(picking.sugery_date - timedelta(hours=5)).strftime("%d/%m/%Y") if picking.sugery_date else ''}<br/>
						<strong>Hora Cirugía: </strong>{(picking.sugery_date - timedelta(hours=5)).strftime("%H:%M:%S") if picking.sugery_date else ''}<br/>
						<strong>Ciudad: </strong>{picking.shop_id or ''}<br/>
						<strong>Seguro Médico: </strong><br/>
						<strong>Nombre Paciente: </strong>{picking.name_patient or ''}<br/>
						<strong>DNI/RUC Paciente: </strong>{picking.patient_vat or ''}<br/>
					</td>
					<td style="vertical-align: top;">
						<strong>Tipo: </strong>{picking.categoria_rel or ''}<br/>
						<strong>O.Com/EQC: </strong>{oc_com_eqc}<br/>
						<strong>No. Ingreso(HCL): </strong>ND<br/>
						<strong>Sede: </strong>{picking.medic_center or ''}<br/>
						<strong>Nombre Cirujano: </strong>{picking.name_doctor or ''}<br/>
					</td>
				</tr>
			</tbody>
		</table>"""      

