def build_memory_namespace(
    user_id: str,
    log_room_id: str,
    log_room_member_id: str,
) -> tuple[str, ...]:
    return (
        "memories",
        str(user_id),
        str(log_room_id),
        str(log_room_member_id),
    )
