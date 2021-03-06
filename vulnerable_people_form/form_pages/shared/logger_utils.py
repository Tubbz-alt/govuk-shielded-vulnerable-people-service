import logging
import sys


log_event_names = {
    "NHS_LOGIN_FAIL": "NhsLoginFailed",
    "NHS_LOGIN_SUCCESS": "NhsLoginSucceeded",
    "NHS_LOGIN_USER_INFO_REQUEST_FAIL": "NhsLoginUserInfoRequestFailed",
    "NHS_LOGIN_USER_CONSENT_NOT_GIVEN": "NhsLoginUserConsentNotGiven",
    "POSTCODE_INELIGIBLE": "IneligiblePostcodeEntered",
    "POSTCODE_ELIGIBLE": "EligiblePostcodeEntered",
    "MEDIUM_POSTCODE_TIER" : "MediumPostcodeTierEntered",
    "HIGH_POSTCODE_TIER" : "HighPostcodeTierEntered",
    "VERY_HIGH_POSTCODE_TIER" : "VeryHighPostcodeTierEntered",
    "VERY_HIGH_PLUS_SHIELDING_POSTCODE_TIER" : "VeryHighPlusShieldingPostcodeTierEntered",
    "ORDNANCE_SURVEY_LOOKUP_SUCCESS": "OrdnanceSurveyPlacesApiPostcodeLookupSucceeded",
    "ORDNANCE_SURVEY_LOOKUP_FAILURE": "OrdnanceSurveyPlacesApiPostcodeLookupFailed",
    "BOTO_CLIENT_ERROR": "BotoClientErrorOccurred",
    "AWS_ARN_INIT": "AwsRdsDatabaseAndSecretArnInitialised",
    "NOT_VALID_PHONE_NUMBER_FOR_TEXTS_ENTERED": "NotValidPhoneNumberForTextsEntered",
    "POSTCODE_TO_TIER_SUCCESS": "PostcodeToTierSuccess",
    "POSTCODE_TIER_NOT_FOUND": "PostcodeTierNotFound",
    "UPRN_TO_TIER_SUCCESS": "UprnToTierSuccess",
    "UPRN_TIER_NOT_FOUND": "UprnTierNotFound",
    "POSTCODE_IN_ENGLAND": "PostcodeInEngland",
    "POSTCODE_NOT_IN_ENGLAND": "PostcodeNotInEngland",
}


def init_logger(logger):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def create_log_message(event_name, event_detail):
    return f"coronavirus-shielding-support - {event_name} - {event_detail}"
