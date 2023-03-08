odoo.define('timesheet_grid_enhancement.timer_grid_renderer', function (require) {
    "use strict";

    const TimesheetGridRenderer = require("timesheet_grid.TimerGridRenderer")
    const { useRef } = owl.hooks;

    class TimerGridRendererEnhanced extends TimesheetGridRenderer {
        _onFocusComponent(ev) {
            const path = ev.path
            this.trigger('open_timesheet_popup', {
                ev
            });
        }

        async _onKeydown(ev) {
            if (ev.key === 'Shift' && !this.stateTimer.timerRunning && !this.state.editMode) {
                this.stateTimer.addTimeMode = true;
            }
        }

        async _stop_timer() {
            if(this.stateTimer.description == "") {
                const descriptionField = $(
                    ".input_description"
                )
                descriptionField.addClass("o_field_invalid")
                return;
            }
            return super._stop_timer(...arguments);
        }
    }

    return TimerGridRendererEnhanced;
});
