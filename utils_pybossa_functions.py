#!/bin/python
# -*- coding: UTF-8 -*-
# Authors: B. Herfort 2018
########################################################################################################################


# good docu for pbclient https://pythonhosted.org/pybossa-client/
def create_pybossa_project(pbclient, project_name, project_shortname, project_description, task_presenter_template_file):
    # you might need to publish your project manually in the web interface

    # first create the project
    pbclient.create_project(project_name, project_shortname, project_description)
    project = pbclient.find_project(short_name=project_shortname)[0]

    # Then update Task Presenter
    project.info['task_presenter'] = open(task_presenter_template_file).read()
    project.info['task_presenter'] = project.info['task_presenter'].replace('{project_shortname}',
                                                                            project_shortname)
    pbclient.update_project(project)

    return project



def delete_all_pybossa_tasks(pbclient, pybossa_project):
    # get all tasks for this project
    deleted = 0
    all_tasks = pbclient.get_tasks(pybossa_project.id, last_id=None)

    # we can only request 100 tasks at a time
    while len(all_tasks) > 0:
        # delete tasks one after the other
        for task in all_tasks:
            pbclient.delete_task(task.id)
            deleted += 1
            last_id = task.id

        all_tasks = pbclient.get_tasks(pybossa_project.id, last_id=last_id)

    print('after deleting %s tasks there are %s tasks for project: %s' % (deleted, len(all_tasks), pybossa_project))


def delete_all_pybossa_taskruns(pbclient, pybossa_project):
    # get all tasks for this project
    deleted = 0
    all_taskruns = pbclient.get_taskruns(pybossa_project.id, last_id=None)

    # we can only request 100 tasks at a time
    while len(all_taskruns) > 0:
        # delete tasks one after the other
        for task in all_taskruns:
            pbclient.delete_taskrun(task.id)
            deleted += 1
            last_id = task.id

        all_taskruns = pbclient.get_taskruns(pybossa_project.id, last_id=last_id)

    print('after deleting %s taskruns there are %s taskruns for project: %s' % (
    deleted, len(all_taskruns), pybossa_project))


def get_all_task_runs(pbclient, pybossa_project):
    # get all tasks for this project
    all_task_runs = {}

    task_runs = pbclient.get_taskruns(pybossa_project.id)

    # we can only request 100 tasks at a time
    while len(task_runs) > 0:
        for taskrun in task_runs:
            task_id = taskrun.info['id']
            answer = taskrun.info['answer']

            try:
                all_task_runs[task_id].append(answer)
            except:
                all_task_runs[task_id] = []
                all_task_runs[task_id].append(answer)

            last_id = taskrun.id

        task_runs = pbclient.get_taskruns(pybossa_project.id, last_id=last_id)

    return all_task_runs
