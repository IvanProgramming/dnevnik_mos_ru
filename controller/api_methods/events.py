from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request

from model.event import Event
from view.api_response import OKResponse


class EventEndpoint(HTTPEndpoint):
    async def get(self, request: Request):
        profile = request.state.profile
        return OKResponse(Event.get_events_for_user(profile, as_dicts=True))

    async def post(self, request: Request):
        profile = request.state.profile
        events = (await request.json())["events"]
        Event.register_many(events, profile.phone_number)
        return OKResponse({})
