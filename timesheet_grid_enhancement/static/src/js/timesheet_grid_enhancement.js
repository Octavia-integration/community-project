odoo.define('timesheet_grid_enhancement.timesheet_grid_enhancement', function(require) {
    'use strict';

    const TimesheetGridView = require("timesheet_grid.GridView");
    const TimesheetGridRendererEnhanced = require("timesheet_grid_enhancement.timesheet_grid_renderer")
    const TimesheetGridControllerEnhanced  = require("timesheet_grid_enhancement.timesheet_grid_controller")
    const viewRegistry = require('web.view_registry');

    let TimesheetGridViewEnhanced = TimesheetGridView.extend({
        config: _.extend({}, TimesheetGridView.prototype.config, {
            Renderer: TimesheetGridRendererEnhanced,
            Controller : TimesheetGridControllerEnhanced,
        }),
    });
    viewRegistry.add('timesheet_grid_enhanced', TimesheetGridViewEnhanced);
});
