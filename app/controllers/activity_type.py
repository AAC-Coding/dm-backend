from google.cloud.firestore_v1.base_query import FieldFilter

from app import db
from app.models import ActivityType
from app.controllers.user import users_collection


activity_type_collection = db.collection("activity_type")


def create_activity_types(data: dict):
    duration = int(data.get("duration"))
    user_id = data.get("user_id")
    user_ref = users_collection.document(user_id)
    _activity_type_exists = _get_activity_type_by_name(data.get("name"), user_ref)
    if any(_activity_type_exists):
        raise Exception("Activity Type already exists")
    activity_type = ActivityType(
            user_ref=user_ref,
            name=data.get("name"),
            duration=duration
    )
    activity_type_collection.add(activity_type.to_dict())
    activity_type.user_ref = user_ref.path
    return activity_type.to_dict()


def get_activity_types(
    user_id: str,
):
    user_ref = users_collection.document(user_id)
    query = (
        activity_type_collection.where(filter=FieldFilter("user_ref", "==", user_ref))
    )
    activity_types = query.stream()
    activity_types_list = []
    for activity_type in activity_types:
        activity_dict = activity_type.to_dict()
        activity_dict["user_ref"] = activity_dict["user_ref"].id
        activity_dict["id"] = activity_type.id
        activity_types_list.append(activity_dict)

    return activity_types_list


def get_activity_type(activity_type_id: str):
    activity_type = activity_type_collection.document(activity_type_id).get()
    activity_dict = activity_type.to_dict()
    if not activity_dict:
        raise Exception("activity_type not found")
    activity_dict["user_ref"] = activity_dict["user_ref"].id
    activity_dict["id"] = activity_type.id
    return activity_dict


def update_activity_type(activity_type_id: str, data: dict):
    if "id" in data:
        raise Exception("Cannot update id field")
    if "user_id" in data:
        raise Exception("Cannot update user_id field")
    activity_type_collection.document(activity_type_id).update(data)
    return "activity_type updated successfully"


def delete_activity_type(activity_type_id: str):
    activity_type_collection.document(activity_type_id).delete()
    return "activity_type deleted successfully"


def _get_activity_type_by_name(name: str, user_ref):
    query = (
        activity_type_collection.where(filter=FieldFilter("name", "==", name))
        .where(filter=FieldFilter("user_ref", "==", user_ref))
    )
    activity_type = query.stream()
    return activity_type


def create_default_activity_types(user_id: str):
    user_ref = users_collection.document(user_id)
    default_activity_types = [
        {"name": "Dials", "duration": 1},
        {"name": "Presentation", "duration": 120},
        {"name": "Recruiting Interview", "duration": 20},
        {"name": "Doorknock", "duration": 5},
        {"name": "Appointment", "duration": 0}
    ]
    for activity_type in default_activity_types:
        activity_type = ActivityType(
                user_ref=user_ref,
                name=activity_type["name"],
                duration=activity_type["duration"]
        )
        activity_type_collection.add(activity_type.to_dict())
    return "Default activity types created successfully"
