from fastapi import APIRouter
from fastapi import Depends
from attempts.schemas import Attempt, AttemptState, NestedAttemptState
from users.schemas import User
from users.handle_users import current_active_verified_user
from db import database
from beanie import PydanticObjectId
from datetime import datetime, timedelta, timezone
from edist.sed import sed_backtrace
from edist import edits
from edist.edits import Insertion, Deletion, Replacement, Script

router = APIRouter(prefix="/attempt")


@router.get("/get_state/{task_unique_name}")
async def get_attempt_state(task_unique_name, user: User = Depends(current_active_verified_user)):
    attempt = await database.find_attempt(task_unique_name, user.id, user.current_course)
    if attempt is None:
        attempt = Attempt(user_id = str(user.id), task_unique_name=task_unique_name, state_log=[], 
                          course_unique_name=user.current_course, current_state="",
                          start_time_list=[datetime.now().astimezone(timezone.utc).strftime("%d.%m.%Y %H:%M:%S")], 
                          duration_list=[str(timedelta(0))])
        await database.create_attempt(attempt)
        course_enrollment = course_enrollment = await database.get_course_enrollment(user, user.current_course)
        tasks_attempted = course_enrollment.tasks_attempted
        if not task_unique_name in tasks_attempted:
            tasks_attempted.append(task_unique_name)
        await database.update_course_enrollment(course_enrollment, {"tasks_attempted": tasks_attempted})
        return({"attempt_id": str(attempt.id), "code": ""})
    #if len(attempt.state_log)==0:
    #    return({"attempt_id": str(attempt.id), "code": ""})
    else:
        logged_current_state = attempt.current_state
        attempt.start_time_list.append(datetime.now().astimezone(timezone.utc).strftime("%d.%m.%Y %H:%M:%S"))
        attempt.duration_list.append(str(timedelta(0)))
        await database.update_attempt(attempt)
        if user.settings["dataCollection"] == True:
            compiled_current_state = compile_state_log("", attempt.state_log)
            if compiled_current_state != logged_current_state:
                state = f"\nA problem occured. We are not sure what your last state is.\nWe have compiled the following state:\n{compiled_current_state}\n but logged the following:\n{logged_current_state}"
                return({"attempt_id": str(attempt.id), "code": state})
        return({"attempt_id": str(attempt.id), "code": logged_current_state})

#def compile_state_log(previous_state, change_log: list):
#    if len(change_log) == 0:
#        return previous_state
#    else:
#        changed_line = change_log[0]["code"][0][0]
#        if changed_line == -1:
#            next_state = change_log[0]["code"][0][1]
#        else:
#            next_state = previous_state.split("\n")
#            n_lines = len(next_state)
#            if changed_line == n_lines+1:
#                next_state.append("")
#            elif changed_line > n_lines + 1:
#                raise Exception("Corrupted state log: too many new lines")
#            next_state[changed_line - 1] = change_log[0]["code"][0][1]
#            #-1 encodes for a deleted line
#            if next_state[changed_line - 1] == -1:
#                next_state.remove(-1)
#            next_state = "\n".join(next_state)
#        return compile_state_log(next_state, change_log[1:])


    
def compile_state_log(previous_state, change_log: list):
    if not previous_state is list:
        previous_state = list(previous_state)
    if len(change_log) == 0:
        return "".join(previous_state)
    else:
        storage_diff = change_log[0]["diff"]
        diff = []
        for edit in storage_diff:
            if edit[0] == "I":
                diff.append(Insertion(edit[1], edit[2]))
            elif edit[0] == "D":
                diff.append(Deletion(edit[1]))
            elif edit[0] == "R":
                diff.append(Replacement(edit[1], edit[2]))
            else:
                raise Exception(f"Unknown edit type: {edit[0]}")
        diff = Script(lst=diff)
        next_state = diff.apply(previous_state)
        return compile_state_log(next_state, change_log[1:])

def get_line_diff(previous_code: str, line_update: tuple):
    changed_line = line_update[0][0]
    change_to = line_update[0][1]
    previous_lines = previous_code.split("\n")
    if changed_line == -1:
        next_step = change_to
    elif changed_line == -2:
        #-2 is the code for submissions
        return Script(lst=[])
    else:
        next_step = previous_lines.copy()
        next_step[changed_line - 1] = change_to
        next_step = "\n".join(next_step)
    alignment = sed_backtrace(previous_code, next_step)
    script = edits.alignment_to_script(alignment, previous_code, next_step)
    return script
    
def apply_diff(previous_code: str, diff):
    char_list = list(previous_code)
    updated_code = diff.apply(char_list)
    return "".join(updated_code)

@router.post("/log")
async def log_attempt_state(state: NestedAttemptState, user: User = Depends(current_active_verified_user)):
    attempt = await database.get_attempt(state.attempt_id)
    #TODO: Handle case whre data collection settings are changed!
    if user.settings["dataCollection"] == True:
        state.id = str(PydanticObjectId())
        if len(attempt.state_log) > 0:
            previous_code = compile_state_log("", attempt.state_log)
        else: 
            previous_code = ""
        for i, code in enumerate(state.code_list):
            diff = get_line_diff(previous_code, code)
            submission_id = code[0][1] if code[0][0] == -2 else ""
            transform_edit = lambda edit: (edit.__class__.__name__[0], edit._index, edit._label) if hasattr(edit, "_label") else (edit.__class__.__name__[0], edit._index)
            storage_diff = [transform_edit(edit) for edit in diff]
            code_state = AttemptState(state_datetime=state.state_datetime_list[i], 
                                diff=storage_diff,
                                submission_id=submission_id, dataCollection=state.dataCollection)
            if state.dataCollection:
                attempt.state_log.append(code_state)
            previous_code = apply_diff(previous_code, diff)
    #if not state.dataCollection:
    #    latest_code = previous_code
    #    last_state_code = compile_state_log("", attempt.state_log) if len(attempt.state_log) > 0 else ""
    #    diff = get_line_diff(last_state_code, [[-1, latest_code]])
    #    storage_diff = [transform_edit(edit) for edit in diff]
    #    code_state = AttemptState(attempt_id=state.attempt_id, state_datetime=state.state_datetime, 
    #                        diff=storage_diff,
    #                        submission_id=state.submission_id, dataCollection=state.dataCollection)
    #    if len(attempt.state_log) > 0 and attempt.state_log[-1]["submission_id"]!="":
    #        attempt.state_log[-1] = code_state
    #    else:
    #       attempt.state_log.append(code_state)
    if len(state.state_datetime_list) > 0:
        current_attempt_time = datetime.strptime(state.state_datetime_list[-1]["utc"], "%d.%m.%Y %H:%M:%S.%f")
        current_start_time = datetime.strptime(attempt.start_time_list[-1], "%d.%m.%Y %H:%M:%S")
        attempt.duration_list[-1] = str(current_attempt_time - current_start_time)
        attempt.current_state = state.current_state
    await database.update_attempt(attempt)

