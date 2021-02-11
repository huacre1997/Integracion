def permission(request):
    permission=request.user.get_group_permissions()
    return {"perm":permission}
