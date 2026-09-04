def get_mode_result(work, targets):
    """
    Generate mode-specific information based on
    the selected work and detected weed targets.
    """

    if not targets:
        return {
            "status": "NO TARGET",
            "message": "No weed detected."
        }

    if work == "Weed Removal":

        return {
            "status": "TARGET READY",
            "message": (
                f"{len(targets)} weed target(s) "
                "identified for removal."
            )
        }

    elif work == "Weed Spraying":

        return {
            "status": "SPRAY TARGET READY",
            "message": (
                f"{len(targets)} weed target(s) "
                "identified for spraying."
            )
        }

    elif work == "Sowing":

        return {
            "status": "POSITION DETECTED",
            "message": (
                f"{len(targets)} target position(s) "
                "available for sowing analysis."
            )
        }

    return {
        "status": "READY",
        "message": "Mode selected."
    }