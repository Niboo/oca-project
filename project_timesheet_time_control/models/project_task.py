# Copyright 2019 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectTask(models.Model):
    _name = "project.task"
    _inherit = ["project.task", "hr.timesheet.time_control.mixin"]

    is_group_hr_timesheet_user = fields.Boolean(
        compute="_compute_is_group_hr_timesheet_user",
    )

    def _compute_is_group_hr_timesheet_user(self):
        for task in self:
            task.is_group_hr_timesheet_user = (
                self.env.ref("hr_timesheet.group_hr_timesheet_user").id
                in self.env.user.groups_id.ids
            )

    @api.model
    def _relation_with_timesheet_line(self):
        return "task_id"

    @api.depends(
        "project_id.allow_timesheets",
        "timesheet_ids.employee_id",
        "timesheet_ids.unit_amount",
    )
    def _compute_show_time_control(self):
        result = super()._compute_show_time_control()
        for task in self:
            # Never show button if timesheets are not allowed in project
            if not task.project_id.allow_timesheets:
                task.show_time_control = False
        return result

    def button_start_work(self):
        result = super().button_start_work()
        result["context"].update({"default_project_id": self.project_id.id})
        return result
