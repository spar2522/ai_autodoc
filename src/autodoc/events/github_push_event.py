from dataclasses import dataclass

from autodoc.events.event import Event


@dataclass
class GithubPushEvent(Event):

    github_repo: str

    commit_hash: str
