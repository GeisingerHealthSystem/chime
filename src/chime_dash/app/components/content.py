"""Initializes the content dash html
"""
from collections import OrderedDict

from dash_html_components import Main
from dash_bootstrap_components import Container
from chime_dash.app.components.base import Component, HTMLComponentError
from chime_dash.app.components.footer import Footer
from chime_dash.app.components.header import Header
from chime_dash.app.components.intro import Intro, ToolDetails
from chime_dash.app.components.visualizations import Visualizations


class Content(Component):
    """Glues together the individual body components
    """

    def __init__(self, language, defaults):
        """
        """
        super().__init__(language, defaults)
        self.components = OrderedDict(
            header=Header(language, defaults),
            intro=Intro(language, defaults),
            tool_details=ToolDetails(language, defaults),
            visualizations=Visualizations(language, defaults),
            footer=Footer(language, defaults),
        )
        self.callback_outputs = []
        self.callback_inputs = OrderedDict()
        for component in self.components.values():
            self.callback_outputs += component.callback_outputs
            self.callback_inputs.update(component.callback_inputs)

    def get_html(self):
        """Initializes the content container dash html
        """
        content = Main(
            className="py-5",
            style={
                "margin-left": "320px",
                "margin-top": "56px"
            },
            children=
                [Container(
                    children=
                        self.components["header"].html
                        + self.components["intro"].html
                        + self.components["tool_details"].html
                )]
                + self.components["visualizations"].html
                + [Container(
                    children=
                        self.components["footer"].html
                )],
        )

        return [content]

    def callback(self, *args, **kwargs):
        """Combines individual callbacks
        """
        callback_returns = []
        for component in self.components.values():
            try:
                callback_returns += component.callback(**kwargs)
            except Exception as error:
                raise HTMLComponentError(component, error)

        return callback_returns