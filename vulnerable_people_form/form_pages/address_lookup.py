import json

from flask import redirect, session, current_app

from ..integrations import postcode_lookup_helper
from .blueprint import form
from .shared.constants import SESSION_KEY_ADDRESS_SELECTED
from .shared.querystring_utils import append_querystring_params
from .shared.render import render_template_with_title
from .shared.routing import route_to_next_form_page
from .shared.session import get_errors_from_session, request_form, form_answers, update_test_postcode_data
from .shared.validation import validate_address_lookup
from .shared.location_tier import update_location_tier_by_uprn


@form.route("/address-lookup", methods=["GET"])
def get_address_lookup():
    postcode = session.get("postcode")
    if not postcode:
        postcode = form_answers()["support_address"]["postcode"]
    try:
        addresses = postcode_lookup_helper.get_addresses_from_postcode(postcode)
    except postcode_lookup_helper.PostcodeNotFound:
        session["error_items"] = {
            **session.setdefault("error_items", {}),
            "support_address": {"postcode": "Could not find postcode, please enter your address manually"},
        }
        return redirect("/support-address")
    except postcode_lookup_helper.NoAddressesFoundAtPostcode:
        session["error_items"] = {
            **session.setdefault("error_items", {}),
            "support_address": {
                "support_address": f"No addresses found for {postcode}, please enter your address manually",
            },
        }
        return redirect("/support-address")
    except postcode_lookup_helper.ErrorFindingAddress:
        session["error_items"] = {
            **session.setdefault("error_items", {}),
            "support_address": {
                "support_address": "An error has occurred, please enter your address manually",
            },
        }
        return redirect("/support-address")

    prev_path = append_querystring_params("/postcode-eligibility")

    return render_template_with_title(
        "address-lookup.html",
        previous_path=prev_path,
        postcode=postcode,
        addresses=addresses,
        **get_errors_from_session("postcode"),
    )


@form.route("/address-lookup", methods=["POST"])
def post_address_lookup():
    session["form_answers"] = {
        **session.setdefault("form_answers", {}),
        "support_address": {**json.loads(request_form()["address"])},
    }
    session["error_items"] = {}

    uprn = {**json.loads(request_form()["address"])}.get("uprn", None)
    postcode = {**json.loads(request_form()["address"])}.get("postcode", None)
    update_location_tier_by_uprn(uprn, current_app)
    update_test_postcode_data(session["postcode"],current_app)
    
    if not validate_address_lookup():
        return redirect("/address-lookup")
    session[SESSION_KEY_ADDRESS_SELECTED] = True
    return route_to_next_form_page()
