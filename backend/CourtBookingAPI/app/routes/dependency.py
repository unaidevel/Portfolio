from app.routes.routes import RoleChecker


admin_only = RoleChecker(allowed_roles=['admin'])
staff_only = RoleChecker(allowed_roles=['staff'])