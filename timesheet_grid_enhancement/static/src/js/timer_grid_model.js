odoo.define('timesheet_grid_enhancement.timer_grid_model', function (require) {
    "use strict";

    const TimerGridModel = require('timesheet_grid.TimerGridModel');

    const TimerGridModelEnhanced = TimerGridModel.extend({
        /**
         * @private
         * @param {task} task
         * @returns {str}
         */
        _getLabel: function (task) {
            if (task.label[0] == false) {
                return "";
            }

            return task.label[0];
        },
       /**
         * @private
         * @param {task, task} a, b
         * @returns {bool}
         */
        _compareTask: function (a, b) {
            if ( typeof b !== 'undefined' && this._getLabel(a) > this._getLabel(b) ) {
                return true;
            }

            return false;
        },
        /**
         * @private
         * @param {array, array, array} rowArray, gridArray, totalArray
         * @returns {array, array, array}
        */
        _bubbleSort: function (rowArray, gridArray, totalArray) {
            let swapped = true;

            do {
                swapped = false;
                for (let j = 0; j < rowArray.length; j++) {
                    if (this._compareTask(rowArray[j], rowArray[j + 1])) {
                        let temp = rowArray[j];
                        rowArray[j] = rowArray[j + 1];
                        rowArray[j + 1] = temp;

                        let tempGrid = gridArray[j];
                        gridArray[j] = gridArray[j + 1];
                        gridArray[j + 1] = tempGrid;

                        let tempTotal = totalArray['rows'][j];
                        totalArray['rows'][j] = totalArray['rows'][j + 1];
                        totalArray['rows'][j + 1] = tempTotal;

                        swapped = true;
                    }
                }
            } while (swapped);

            return [rowArray, gridArray, totalArray];
        },
        /**
         * @private
         * @param {project, project} a, b
         * @returns {integer}
         */
        _compareProject: function (a, b) {
          if ( a.__label[1] < b.__label[1] ) {
            return -1;
          }
          if ( a.__label[1] > b.__label[1] ) {
            return 1;
          }
          return 0;
        },
        /**
         * @override
         * @private
         * @param {string[]} groupBy
         * @returns {Promise}
         */
        _fetchGroupedData: async function (groupBy) {
            await this._super(groupBy);

            // Sort task by name for each project
            this._gridData.data.forEach((group, groupIndex) => {
                let sortedArrays = this._bubbleSort(group.rows, group.grid, group.totals);
                this._gridData.data[groupIndex].rows = sortedArrays[0];
                this._gridData.data[groupIndex].grid = sortedArrays[1];
                this._gridData.data[groupIndex].totals = sortedArrays[2];
            });

            // Sort project by name
            this._gridData.data = this._gridData.data.sort(this._compareProject);

            // TODO: find a better way to order the total array instead of recomputing it a second time
            this._gridData.totals = this._computeTotals(_.flatten(_.pluck(this._gridData.data, 'grid'), true));
        },
    });

    return TimerGridModelEnhanced;
});
