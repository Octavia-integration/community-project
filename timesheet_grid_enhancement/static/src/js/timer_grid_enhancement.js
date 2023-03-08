odoo.define('timesheet_grid_enhancement.timer_grid_enhancement', function(require) {
    'use strict';

    const TimerGridView = require("timesheet_grid.TimerGridView");
    const TimerGridRendererEnhanced = require("timesheet_grid_enhancement.timer_grid_renderer")
    const TimerGridControllerEnhanced  = require("timesheet_grid_enhancement.timer_grid_controller")
    const viewRegistry = require('web.view_registry');

    let TimerGridViewEnhanced = TimerGridView.extend({

        config: _.extend({}, TimerGridView.prototype.config, {
            Renderer: TimerGridRendererEnhanced,
            Controller : TimerGridControllerEnhanced,
        }),
    });
    viewRegistry.add('timer_grid_enhanced', TimerGridViewEnhanced);
});
