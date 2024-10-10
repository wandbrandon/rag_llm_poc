from rag_llm_poc import data
from langchain_core.tools import tool
from datetime import date, datetime
from typing import Annotated, Optional
from ast import literal_eval
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import InjectedState


@tool
def get_member_info(
    state: Annotated[dict, InjectedState],
    member_id: Optional[str] = None,
    date_of_birth: Optional[str] = None,
) -> dict:
    """Get the member info from member id, authenticate the user, and respond with the name of the user

    Args:
        member_id (Optional[str]): The member id of the user.
        date_of_birth (Optional[str]): The date of birth of the user, needs to be formated like "MMDDYYYY".

    Returns:
        dict: The member info of the user.
    """
    if not member_id:
        raise ValueError("No member_id provided")
    member_info = data.member_data.get((member_id, date_of_birth), None)
    if member_info:
        state["member_info"] = member_info
        state["authenticated"] = True
        return {
            "status": "Success",
            "first_name": member_info["first_name"],
            "last_name": member_info["last_name"],
        }
    raise ValueError("Member not found in records")


@tool
def get_inbound_profile(
    dnis: Optional[int] = None,
    ani: Optional[int] = None,
) -> dict:
    """
    Get info about dnis and save it to state of the bot. Once successeful, we move to the main assistant.

    Args:
        dnis (Optional[int]): The DNIS of the user, it is a 5 digit number.
        ani (Optional[int]): The ANI of the user, it is a 10 digit number.

    Returns:
        dict: Returns the info about the DNIS or ANI.
    """

    if dnis and ani:
        dnis_data = data.dnis.get(dnis, None)
        ani_data = data.ani.get(ani, None)
        if dnis_data and ani_data:
            return {
                "dnis": dnis_data,
                "ani": ani_data,
            }
        else:
            raise ValueError("DNIS or ANI not found in records")
    raise ValueError("Missing information in your request. I need a DNIS and an ANI")


@tool
def faq():
    "Returns a list of all frequently asked questions"
    return [
        {
            "question": "What is a claim and what information does it have?",
            "answer": "Claims can give you the status of a claim, the amount, and the date.",
        },
        {
            "question": "What is CVS Health or Aetna known for?",
            "answer": "Our quality service in providing health care and insurance!",
        },
    ]


@tool
def find_claim_status(
    state: Annotated[dict, InjectedState],
    claim_date: Optional[datetime | date] = None,
) -> list[dict]:
    """
    Search for claims by specific claim date, if no date is given, return all claims for the user.

    Args:
        claim_date (Optional[datetime | date]): The date of the claim the user is looking for.

    Returns:
        list[dict]: A list of claims found in the records
    """

    if not state["authenticated"]:
        raise ValueError(
            "User is not authenticated, please prompt for Member ID and DOB"
        )
    if not state["member_info"]:
        raise ValueError("No member_info found for the user")
    member_info = state["member_info"]

    if claim_date:
        claim = member_info.claims[claim_date]
        if claim:
            return {
                "status": "Success",
                "claim": claim,
            }
        else:
            raise ValueError(
                "No claim found for the given date, ask user for a different date."
            )

    return member_info.claims


@tool
def findcare_zip(provider_type: Optional[str], config: RunnableConfig) -> dict:
    """
    Find providers in the local area for the user based on the type of provider

    Args:
        provider_type (Optional[str]): The type of provider the user is looking for. Examples: Cardiologist, Dentist, Primary Care

    Returns:
        list[dict]: A list of providers near the user.
    """

    configuration = config.get("configurable", {})
    member_info = configuration.get("member_info", None)
    if not member_info:
        raise ValueError("No Zipcode found for the user")
    if not provider_type:
        raise ValueError("No provider_type was given from user")
    if member_info and provider_type:
        return data.findcare_zip.get(
            member_info["zip_code"], {"message": "No Providers found"}
        )
