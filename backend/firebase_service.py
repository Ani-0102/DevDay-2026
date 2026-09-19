import os

import firebase_admin
from fastapi import HTTPException
from firebase_admin import credentials, firestore


def get_firestore_db():
    service_account_path = os.getenv(
        "FIREBASE_SERVICE_ACCOUNT_PATH"
    )

    if not service_account_path:
        raise HTTPException(
            status_code=500,
            detail=(
                "Missing FIREBASE_SERVICE_ACCOUNT_PATH "
                "in .env"
            ),
        )

    # Make relative paths work reliably
    if not os.path.isabs(service_account_path):
        backend_directory = os.path.dirname(
            os.path.abspath(__file__)
        )

        service_account_path = os.path.join(
            backend_directory,
            service_account_path.removeprefix("./"),
        )

    if not os.path.exists(service_account_path):
        raise HTTPException(
            status_code=500,
            detail=(
                "Firebase service account file "
                f"not found: {service_account_path}"
            ),
        )

    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate(
                service_account_path
            )

            firebase_admin.initialize_app(
                cred
            )

        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=(
                    "Could not initialize Firebase: "
                    f"{error}"
                ),
            )

    return firestore.client()


def get_favorites(
    user_id: str,
) -> list:

    try:
        db = get_firestore_db()

        favorite_doc = (
            db.collection("favorites")
            .document(user_id)
            .get()
        )

        if not favorite_doc.exists:
            return []

        favorite_data = (
            favorite_doc.to_dict()
            or {}
        )

        return favorite_data.get(
            "items",
            [],
        )

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=(
                "Could not get favorites: "
                f"{error}"
            ),
        )


def toggle_favorite(
    user_id: str,
    food: dict,
) -> list:

    try:
        db = get_firestore_db()

        favorite_ref = (
            db.collection("favorites")
            .document(user_id)
        )

        favorites = get_favorites(
            user_id
        )

        food_id = food.get("id")

        if food_id is None:
            raise HTTPException(
                status_code=400,
                detail="Food item is missing an id",
            )

        already_favorited = any(
            str(item.get("id"))
            == str(food_id)
            for item in favorites
        )

        if already_favorited:
            favorites = [
                item
                for item in favorites
                if str(item.get("id"))
                != str(food_id)
            ]

        else:
            favorites.append(food)

        favorite_ref.set(
            {
                "items": favorites
            }
        )

        return favorites

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=(
                "Could not update favorites: "
                f"{error}"
            ),
        )