from flask import redirect

from .answers_enums import YesNoAnswers, get_radio_options_from_enum
from .blueprint import form
from .render_utils import render_template_with_title
from .routing_utils import route_to_next_form_page
from .session_utils import (
    form_answers,
    get_errors_from_session,
    request_form,
    update_session_answers_from_form,
)
from .validation import validate_essential_supplies


@form.route("/essential-supplies", methods=["GET"])
def get_essential_supplies():
    return render_template_with_title(
        "essential-supplies.html",
        radio_items=get_radio_options_from_enum(
            YesNoAnswers, form_answers().get("essential_supplies")
        ),
        previous_path="/nhs-number",
        **get_errors_from_session("essential_supplies"),
    )


@form.route("/essential-supplies", methods=["POST"])
def post_essential_supplies():
    update_session_answers_from_form()
    if not validate_essential_supplies():
        return redirect("/essential-supplies")
    return route_to_next_form_page()