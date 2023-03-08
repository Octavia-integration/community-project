odoo.define('timesheet_grid_enhancement.timer_grid_controller', function (require) {
    "use strict";

    const gridController = require('timesheet_grid.TimerGridController');
    const AbstractController = require('web.AbstractController');
    const dialogs = require('web.view_dialogs');
    const utils = require('web.utils');
    const core = require("web.core");

    const _t = core._t;


   const TimerGridControllerEnhanced = gridController.extend({

        custom_events: Object.assign({}, gridController.prototype.custom_events, {
            open_timesheet_popup: '_onClickCell',
        }),

        init: function (parent, model, renderer, params) {
            this._super.apply(this, arguments);
            this.displayEmpty = false;
        },

        _onClickCell: function (e) {
            var self = this;
            var cell_path = e.data.ev.detail.path.split('.');
            var row_path = cell_path.slice(0, -3).concat(['rows'], cell_path.slice(-2, -1));
            var state = this.model.get();
            var cell = utils.into(state.data, cell_path);
            var row = utils.into(state.data, row_path);
            var groupFields = state.groupBy.slice(state.isGrouped ? 1 : 0);
            var label = _.filter(_.map(groupFields, function (g) {
                return row.values[g][1];
            }), function (g) {
                return g;
            }).join(' - ');
            // pass group by, section and col fields as default in context
            var cols_path = cell_path.slice(0, -3).concat(['cols'], cell_path.slice(-1));
            var col = utils.into(state.data, cols_path);
            var column_value = col.values[state.colField][0];
            if (!column_value) {
                column_value = false;
            } else if (!_.isNumber(column_value)) {
                column_value = column_value.split("/")[0];
            }
                        var ctx = _.extend({}, this.context, {view_grid_add_line: true});

            var sectionField = _.find(this.renderer.fields, function (res) {
                return self.model.sectionField === res.name;
            });
            if (this.model.sectionField && state.groupBy && state.groupBy[0] === this.model.sectionField) {
                var value = state.data[parseInt(cols_path[0])].__label;
                ctx['default_' + this.model.sectionField] = _.isArray(value) ? value[0] : value;
            }
            _.each(groupFields, function (field) {
                ctx['default_' + field] = row.values[field][0] || false;
            });
            ctx['default_' + state.colField] = column_value;
            ctx['create'] = this.canCreate && !cell.readonly;
            ctx['edit'] = this.activeActions.edit && !cell.readonly;
            const context = this.model.getContext();
            const formViewID = context.quick_create_view || this.formViewID || false;
            new dialogs.FormViewDialog(this, {
                res_model: this.modelName,
                res_id: false,
                domain: cell.domain,
                context: ctx,
                view_id: formViewID,
                title: _t(label),
                on_saved: this.reload.bind(this, {}),
            }).open();
        },
        async _onStopTimer(event) {
            const timesheetId = event.data.timesheetId;
            const ctx = _.extend({}, this.context, {view_grid_add_line: true});
            await this.model._stopTimer(timesheetId);
            new dialogs.FormViewDialog(this, {
                res_model: this.modelName,
                res_id: timesheetId,
                view_id: this.formViewID,
                on_saved: this.reload.bind(this, {}),
            }).open();
        },
    })
    return TimerGridControllerEnhanced;
});
