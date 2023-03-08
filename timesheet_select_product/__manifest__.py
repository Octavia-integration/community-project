# © 2016 Pierre Faniel, Sam Lefever
# © 2016 Niboo SRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Timesheet - Select product",
    "category": "Project",
    "summary": "Select a product for each timesheet entry",
    "website": "https://www.niboo.com/",
    "version": "15.0.1.2.0",
    "license": "AGPL-3",
    "description": """
Create precise invoices by allowing employees to select a service product for
 each timesheet log.
This makes it possible to keep an overview on logged hours differentiated by
 seniority and pay grade. # Might be standard
- Makes it possible to specify a product for each timesheet entry # Standard
- Makes it possible to use a specific sale order for each task # Standard
- Makes it mandatory that the linked Sale  order is validated to timesheet on
 the task
- Adds some visual improvement (smart buttons to ease the navigation process)
- Allows you to ingnore TS in your invoice # New
        """,
    "author": "Niboo",
    "depends": ["sale_timesheet_enterprise", "sale_subscription","timesheet_invoiceable_context"],
    "data": [
        "security/ir.model.access.csv",
        "views/project_task.xml",
        "views/timesheet_views.xml",
        "views/account_move.xml",
        "views/product_template_views.xml",
        "wizards/task_link_sale_order_view.xml",
        "wizards/task_link_sale_order_check_view.xml",
        "wizards/project_task_create_timesheet_views.xml",
        "wizards/timesheet_link_invoice_view.xml",
    ],
    "images": ["static/description/hr_timesheet_select_product_cover.png"],
    "installable": False,
    "application": False,
    "post_load": "load_monkey_patches",
}
