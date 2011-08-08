# -*- coding: utf-8 -*-     
def is_user_manager(obj, user):
    if obj:
        project_manager = obj.project.project_manager
        component_responsable = obj.component
        return user.is_superuser or user is project_manager
    else:
        return user.is_superuser

def is_user_submitter(obj, user):
    subbmitter_group = obj.project.subbmitters

    return (
        (subbmitter_group and subbmitter_group in user.groups )
        or
        True
    )
    """"if subbmitter_group:
            return subbmitter_group in user.groups
        else:
            #if there is no submitter group all staff members are submitters
            return True """

def is_user_in_workgroup(obj, user):
    project_workgroup = obj.project.workteam
    component_workgroup = obj.component.project.workteam
    
    # returns True if user belongs to componet or project workgroup or both doesn't exist
    return (
        (project_workgroup and project_workgroup in user.groups)
        or
        (component_workgroup and component_workgroup in user.groups)
        or
        (not project_workgroup and not component_workgroup)
    )
    """if project_workgroup and project_workgroup in user.groups:
        return True
    elif component_workgroup and component_workgroup in user.groups:
        return True
    elif not project_workgroup and not component_workgroup:
        return True
    else:
        return False"""