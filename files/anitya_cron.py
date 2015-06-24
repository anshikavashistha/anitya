#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import logging
import itertools
import multiprocessing

import anitya
import anitya.app
import anitya.lib.exceptions
import anitya.lib.model


def update_project(project):
    """ Check for updates on the specified project. """
    print(project.name)
    session = anitya.lib.init(anitya.app.APP.config['DB_URL'])
    project = anitya.lib.model.Project.by_id(session, project.id)
    try:
        anitya.check_release(project, session),
    except anitya.lib.exceptions.AnityaException as err:
        print(err)
    finally:
        session.get_bind().dispose()
        session.remove()


def main(debug):
    ''' Retrieve all the packages and for each of them update the release
    version.
    '''
    session = anitya.app.SESSION
    LOG = logging.getLogger('anitya')
    LOG.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if debug:
        # Console handler
        chand = logging.StreamHandler()
        chand.setLevel(logging.INFO)
        chand.setFormatter(formatter)
        LOG.addHandler(chand)

    # Save the logs in a file
    fhand = logging.FileHandler('/var/tmp/anitya_cron.log')
    fhand.setLevel(logging.INFO)
    fhand.setFormatter(formatter)
    LOG.addHandler(fhand)

    projects = anitya.lib.model.Project.all(session)
    p = multiprocessing.Pool(anitya.app.APP.config.get('CRON_POOL', 10))
    p.map(update_project, projects)


if __name__ == '__main__':
    debug = '--debug' in sys.argv
    main(debug=debug)
