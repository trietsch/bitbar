import traceback
from typing import List

import requests
from requests import Timeout

from .config import BitbucketConfig, BitbucketConstants
from ..common.util import epoch_ms_to_datetime, abbreviate_string, time_ago
from ..pull_requests import PullRequestStatus, PullRequest, PullRequestsOverview, PullRequestException


def get_open_pull_requests_to_review(_api_key, _url):
    params = dict(
        limit=50,
        state='OPEN',
        role='REVIEWER'
    )

    return list(filter(pr_should_be_reviewed_by_me, get_pull_requests(_api_key, _url, params)))


def get_authored_pull_requests_with_work(_api_key, _url):
    params = dict(
        limit=50,
        state='OPEN',
        role='AUTHOR'
    )

    return list(map(pr_is_marked_as_needs_work, get_pull_requests(_api_key, _url, params)))


def get_pull_requests(_api_key, _url, _params):
    headers = dict(
        Authorization=f'Bearer {_api_key}'
    )
    r = requests.get(_url + BitbucketConfig.BITBUCKET_API_PULL_REQUESTS, params=_params, timeout=5, headers=headers)

    body = r.json()
    pull_requests = body['values']

    is_last_page = body['isLastPage']
    if not is_last_page:
        _params['start'] = body['nextPageStart']
        pull_requests = pull_requests + get_pull_requests(_api_key, _url, _params)

    return pull_requests


def pr_should_be_reviewed_by_me(_pr):
    reviewers_filtered = list(
        filter(lambda reviewer: reviewer['user']['slug'] == BitbucketConfig.USER_SLUG, _pr['reviewers']))

    # If OMIT = True, don't show if status = Approved
    # If OMIT = False, show all
    if len(reviewers_filtered) > 0:
        pr_status = PullRequestStatus[reviewers_filtered[0]['status']]

        if (BitbucketConfig.OMIT_REVIEWED_AND_APPROVED and pr_status != PullRequestStatus.APPROVED) or \
                not BitbucketConfig.OMIT_REVIEWED_AND_APPROVED:
            _pr['overallStatus'] = pr_status
            return _pr


def pr_is_marked_as_needs_work(_pr):
    reviewers_status = [reviewer['status'] for reviewer in _pr['reviewers']]

    if PullRequestStatus.NEEDS_WORK in reviewers_status:
        _pr['overallStatus'] = PullRequestStatus.NEEDS_WORK
    elif PullRequestStatus.APPROVED not in reviewers_status:
        _pr['overallStatus'] = PullRequestStatus.APPROVED
    else:
        _pr['overallStatus'] = PullRequestStatus.UNAPPROVED

    return _pr


def extract_pull_request_data(_raw_pull_requests) -> List[PullRequest]:
    pull_requests: List[PullRequest] = list()

    for _pr in _raw_pull_requests:
        pr_activity = epoch_ms_to_datetime(_pr['updatedDate'])

        pull_requests.append(PullRequest(
            id=str(_pr['id']),
            title=abbreviate_string(_pr['title'], BitbucketConfig.ABBREVIATION_CHARACTERS),
            slug=_pr['toRef']['repository']['slug'],
            from_ref=_pr['fromRef']['displayId'],
            to_ref=_pr['toRef']['displayId'],
            overall_status=_pr['overallStatus'],
            activity=pr_activity,
            time_ago=time_ago(pr_activity),
            all_prs_href=_pr['toRef']['repository']['links']['self'][0]['href'].replace('browse', 'pull-requests'),
            href=_pr['links']['self'][0]['href']
        ))

    return pull_requests


def get_pull_request_overview(private_token: str, host: str) -> PullRequestsOverview:
    _prs_to_review: List[PullRequest] = []
    _prs_authored_with_work: List[PullRequest] = []
    _exception = None
    try:
        _prs_to_review: List[PullRequest] = extract_pull_request_data(
            get_open_pull_requests_to_review(private_token, host)
        )
        _prs_authored_with_work: List[PullRequest] = extract_pull_request_data(
            get_authored_pull_requests_with_work(private_token, host)
        )
    except Timeout as e:
        _exception = PullRequestException(BitbucketConstants.MODULE, BitbucketConstants.TIMEOUT_MESSAGE, e,
                                          traceback.format_exc())
    except ConnectionError as e:
        _exception = PullRequestException(BitbucketConstants.MODULE, BitbucketConstants.CONNECTION_MESSAGE, e,
                                          traceback.format_exc())
    except Exception as e:
        _exception = PullRequestException(BitbucketConstants.MODULE, BitbucketConstants.UNKNOWN_MESSAGE, e,
                                          traceback.format_exc())

    return PullRequestsOverview.create(_prs_to_review, _prs_authored_with_work, _exception)
