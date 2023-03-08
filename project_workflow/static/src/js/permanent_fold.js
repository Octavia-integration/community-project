odoo.define('project_workflow.permanent_fold', function (require) {
    'use strict';
    var KanbanRenderer = require('web.KanbanRenderer');
    var KanbanColumn = require('web.KanbanColumn');
    const {session} = require('@web/session');

    KanbanRenderer.include({
        init: function (parent, data, options, recordOptions) {
            this._super(parent, data, options, recordOptions);
            this.current_user_uid = session.uid;
        },
        willStart: function () {
            var def1 = this._super();
            var def2 = this.get_user_folded_steps_ids();
            return Promise.all([def1, def2]);
        },
        get_user_folded_steps_ids: function () {
            var self = this;
            return self._rpc( {
                model: 'res.users',
                method: 'get_folded_step_ids',
                args: [[self.current_user_uid]],
            })
                .then(function (folded_steps_ids) {
                    self.user_folded_steps_ids = folded_steps_ids;
                });
        },
    });

    KanbanColumn.include({
        events: Object.assign({}, KanbanColumn.prototype.events, {
            'click .o_kanban_toggle_fold_permanently': '_onToggleFoldPermanent',
            'click .o_kanban_toggle_unfold_permanently': '_onToggleUnfoldPermanent',
        }),
        init: function (parent, data, options, recordOptions) {
            this._super(parent, data, options, recordOptions);
            this.permanent_fold = data.model === "project.task" &&
                options.relation === "project.task.step";
            this.current_step_id = data.res_id;
            this.kanban_renderer = parent;
            this.permanent_fold_available = this.permanent_fold &&
                !this.kanban_renderer.user_folded_steps_ids.includes(
                    this.current_step_id);
        },
        _onToggleFoldPermanent: function (event) {
            event.preventDefault();
            if (this.relation === "project.task.step" &&
                    this.modelName === "project.task") {
                this._rpc({
                    model: 'res.users',
                    method: 'add_folded_step',
                    args: [[this.data.context.uid], this.data.res_id],
                });

                if (!this.kanban_renderer.user_folded_steps_ids.includes(
                    this.data.res_id)) {
                    this.kanban_renderer.user_folded_steps_ids.push(this.data.res_id);
                }
                this.trigger_up('column_toggle_fold');
            }
        },
        _onToggleUnfoldPermanent: function (event) {
            event.preventDefault();
            if (this.relation === "project.task.step" &&
                    this.modelName === "project.task") {
                this._rpc({
                    model: 'res.users',
                    method: 'remove_folded_step',
                    args: [[this.data.context.uid], this.data.res_id],
                });
                const index =
                    this.kanban_renderer.user_folded_steps_ids.indexOf(
                        this.data.res_id);
                if (index > -1) {
                    this.kanban_renderer.user_folded_steps_ids.splice(index, 1);
                }
                this.trigger_up('reload');
            }
        },
    });
});
