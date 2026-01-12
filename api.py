import requests
from typing import TypedDict, Literal

class Profile(TypedDict):
  auth_providers: ...
  avatar_url: str
  badges: int
  bio: str
  created: str
  email: str | None
  email_verified: bool | None
  github_id: str | None
  has_password: bool
  has_totp: bool
  id: str
  name: None
  payout_data: "... | None"
  role: Literal["developer"]
  username: str

class API:
  token: str
  me: Profile = None

  def get_profile(self) -> Profile:
    res = requests.get("https://api.modrinth.com/v2/user", headers={
      "Authorization": self.token
    }).json()
    self.me = res
    return res

  def get_projects(self) -> list[...]:
    assert self.me != None
    return requests.get(
      "https://api.modrinth.com/v2/user/%s/projects" % self.me['username'],
      headers={
        "Authorization": self.token
      }
    ).json()

  def get_thread(self, threadId: str) -> "... | None":
    resp = requests.get("https://api.modrinth.com/v2/thread/%s" % threadId, headers={
      "Authorization": self.token
    })
    if resp.status_code == 404:
      return None

    return resp.json()
