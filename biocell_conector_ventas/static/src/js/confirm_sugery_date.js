odoo.define('biocell_conector_ventas.confirm_sugery_date', function (require) {
    "use strict";

    var basicFields = require('web.basic_fields');
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var fieldRegistry = require('web.field_registry');

    var _t = core._t;

    function isSameValue(oldValue, newValue) {
        if (!oldValue && !newValue) {
            return true;
        }
        if (oldValue && newValue && oldValue.isSame && newValue.isSame) {
            return oldValue.isSame(newValue);
        }
        return String(oldValue || '') === String(newValue || '');
    }

    function confirmSugeryDateChange(widget, value, options, applyValue) {
        return new Promise(function (resolve, reject) {
            Dialog.confirm(widget, _t("¿Está seguro de cambiar la Fecha/Hora Cirugía?"), {
                title: _t("Confirmar cambio"),
                confirm_callback: function () {
                    widget._isApplyingConfirmedSugeryDate = true;
                    Promise.resolve(applyValue(value, options)).then(function (result) {
                        widget._isApplyingConfirmedSugeryDate = false;
                        resolve(result);
                    }).catch(function (error) {
                        widget._isApplyingConfirmedSugeryDate = false;
                        reject(error);
                    });
                },
                cancel_callback: function () {
                    widget._render();
                    resolve();
                },
            });
        });
    }

    var ConfirmSugeryDate = basicFields.FieldDateTime.extend({
        _setValue: function (value, options) {
            if (this._isApplyingConfirmedSugeryDate || isSameValue(this.value, value)) {
                return this._super.apply(this, arguments);
            }
            return confirmSugeryDateChange(this, value, options, this._super.bind(this));
        },
    });

    basicFields.FieldDateTime.include({
        _setValue: function (value, options) {
            if (this.name !== 'sugery_date' || this._isApplyingConfirmedSugeryDate || isSameValue(this.value, value)) {
                return this._super.apply(this, arguments);
            }
            return confirmSugeryDateChange(this, value, options, this._super.bind(this));
        },
    });

    fieldRegistry.add('confirm_sugery_date', ConfirmSugeryDate);

    return ConfirmSugeryDate;
});
