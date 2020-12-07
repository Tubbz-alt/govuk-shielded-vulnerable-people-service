from flask import session, current_app, redirect

from .blueprint import form
from .shared.constants import PostcodeTier
from .shared.querystring_utils import append_querystring_params
from .shared.render import render_template_with_title
from .shared.routing import route_to_next_form_page, dynamic_back_url
from .shared.session import persist_answers_from_session, form_answers, get_summary_rows_from_form_answers, \
    get_postcode_tier, is_very_high_plus_shielding_without_basic_care_needs_answer
from ..integrations import govuk_notify_client


@form.route("/check-your-answers", methods=["GET"])
def get_check_your_answers():
    session["check_answers_page_seen"] = True
    exclude_answers = None

    if current_app.is_tiering_logic_enabled:
        if is_very_high_plus_shielding_without_basic_care_needs_answer():
            return redirect(append_querystring_params("/basic-care-needs"))
        if get_postcode_tier() == PostcodeTier.VERY_HIGH.value:
            exclude_answers = ['basic_care_needs']

    return render_template_with_title(
        "check-your-answers.html",
        previous_path=dynamic_back_url(),
        summary_rows=get_summary_rows_from_form_answers(exclude_answers)
    )


@form.route("/check-your-answers", methods=["POST"])
def post_check_your_answers():
    registration_number, is_spl_match = persist_answers_from_session()
    session["registration_number"] = registration_number

    if "NOTIFY_DISABLED" not in current_app.config:
        govuk_notify_client.send_notification(registration_number, is_spl_match)

    return route_to_next_form_page()
