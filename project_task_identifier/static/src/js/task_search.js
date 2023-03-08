/** @odoo-module alias=web.TaskSearch**/

import { _t } from 'web.core';
import session  from 'web.session';
import SystrayMenu from 'web.SystrayMenu';
import Widget from 'web.Widget';

var TaskSearch = Widget.extend({
    template: "WebClient.TaskSearch",
    xmlDependencies: ['/project_task_identifier/static/src/xml/task_search.xml'],
    events: {
        'keyup input': '_onKeyUpInput',
    },
    _onKeyUpInput: function (e) {
        var search_input = $(e.currentTarget);
        $(e.currentTarget).removeClass("o_field_invalid");
        if (e.which === $.ui.keyCode.ENTER) {
            var value = search_input.val();
            var self = this;
            var regex = RegExp('[^\\s-]+(-)[1-9]+');
            if (regex.test(value)) {
                var params = {
                    key: value,
                    company_ids: session.user_context.allowed_company_ids,
                };
                self._rpc({
                    route: '/project_task_identifier/get_task_link',
                    params: params}
                )
                    .then(function (action) {
                        if (action) {
                            self.do_action(action);
                        } else {
                            var search_input = $('.o_task_search');
                            search_input.addClass("o_field_invalid");
                            self.displayNotification({
                                type: 'danger',
                                title: _t('No Task found'),
                                message: _t('The Task you where looking for isn\'t reachable or does not exist in the system'),
                                sticky: false,
                            });
                        }
                    });
            } else if (!isNaN(parseInt(value, 10))) {
                var url_params = {};
                var url = '&' + window.location.hash;
                url.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
                    url_params[key.replace('#', '')] = value;
                });
                if (!url_params.model) {
                    url_params.model = false;
                }
                var params = {
                    key_int: parseInt(value, 10),
                    model: url_params.model,
                    record_id: parseInt(url_params.id, 10),
                    company_ids: session.user_context.allowed_company_ids,
                };
                if (isNaN(params.record_id)) {
                    params.record_id = false;
                }
                self._rpc(
                    {route: '/project_task_identifier/get_task_link_with_model', params: params}
                )
                    .then(function (action) {
                        if (action) {
                            self.do_action(action);
                        } else {
                            var search_input = $('.o_task_search');
                            search_input.addClass("o_field_invalid");
                            self.displayNotification({
                                type: 'danger',
                                title: _t('No Task found'),
                                message: _t('No active Task with the given number could not be reached of are available in the system'),
                                sticky: false,
                            });
                        }
                    });
            } else {
                var search_input = $('.o_task_search');
                search_input.addClass("o_field_invalid");
                self.displayNotification({
                    type: 'danger',
                    title: _t('Invalid format'),
                    message: _t(
                        'The input must follow the given scheme: 999 or XXX-999'),
                    sticky: false,
                });
            }
        }
    },
});

SystrayMenu.Items.push(TaskSearch);

export default TaskSearch;
