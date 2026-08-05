def build_memory_namespace(
    context,
) -> tuple[str, ...]:
    return (
        "memories",
        str(context.log_room_id),
        str(context.log_room_member_id),
        str(context.user_id),
    )
