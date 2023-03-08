odoo.define('timesheet_grid_enhancement.timesheet_grid_renderer', function (require) {
    "use strict";

    const TimesheetGridRenderer = require("timesheet_grid.GridRenderer")

    class TimesheetGridRendererEnhanced extends TimesheetGridRenderer {
        _onFocusComponent(ev) {
            const path = ev.path
            this.trigger('open_timesheet_popup', {
                ev
            });
        }
    }

    return TimesheetGridRendererEnhanced;
});
