"""
    In this file stored only Mounts to another routes, that can be placed in controller or in view
"""

from starlette.routing import Mount

import controller

APP_ROUTES = [
    Mount("", routes=controller.routes)
]
