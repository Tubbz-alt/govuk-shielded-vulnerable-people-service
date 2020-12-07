import json
import time
import hashlib
import random

from flask import request, current_app


def client_ip():
    if request:
        if request.environ.get("HTTP_X_FORWARDED_FOR") is None:
            return request.environ["REMOTE_ADDR"]
        else:
            # if behind a proxy
            return request.environ["HTTP_X_FORWARDED_FOR"]
    return None


def user_agent():
    result = {"platform": None, "browser": None, "version": None, "string": None}
    if request:
        ua_obj = request.user_agent
        result["platform"] = ua_obj.platform
        result["browser"] = ua_obj.browser
        result["version"] = ua_obj.version
        result["string"] = ua_obj.string
    return result


def peppering(obj):
    if obj is not None and current_app:
        pepper = current_app.config.get("SUBMISSION_TRACING_PEPPER")
        if pepper is not None:
            m = hashlib.sha256()
            # convert to string and lower case
            objstr = str(obj).lower()
            # get only the alphanumeric characters
            objstr = "".join(e for e in objstr if e.isalnum())
            # generate hash
            m.update(f"{pepper}:{objstr}".encode())
            # return first 32 characters of the 64 character hash hex
            return m.hexdigest()[:32]
    return None


def persist_answers_log(
    is_spl_match=None, submission_reference=None, submission_details=[], nhs_sub=None
):
    log_output = {}
    try:
        if not current_app or current_app.config.get("SUBMISSION_TRACING_PEPPER") is None:
            raise Exception("current_app not available or SUBMISSION_TRACING_PEPPER not set")

        if submission_details != []:
            random.shuffle(submission_details)

        log_output = {
            "time": time.time(),
            "event": "persist_answers",
            "client_ip": client_ip(),
            "user_agent": user_agent(),
            "is_spl_match": is_spl_match,
            "submission_reference": peppering(submission_reference),
            "submission_details": [
                peppering(sd) for sd in submission_details if sd is not None
            ],
            "nhs_sub": peppering(nhs_sub),
        }
    except Exception as e:
        log_output = {"time": time.time(), "event": "persist_answers", "error": str(e)}

    print(json.dumps(log_output))
