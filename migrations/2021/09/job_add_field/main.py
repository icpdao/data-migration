import sys
import os
import time

from common.models.icpdao.dao import DAO
from common.models.icpdao.github_app_token import GithubAppToken
from common.utils.github_app import GithubAppClient

sys.path.append(os.path.abspath('../../../../'))
import settings

from common.models.icpdao import init_mongo

from common.models.icpdao.job import JobPR

init_mongo({
    'icpdao': {
        'host': settings.ICPDAO_MONGODB_ICPDAO_HOST,
        'alias': 'icpdao',
    }
})


def main_up():
    # get app client
    dao = DAO.objects(name='icpdao').first()
    assert dao, "not dao"
    app_token = GithubAppToken.get_token(
        app_id=settings.ICPDAO_GITHUB_APP_ID,
        app_private_key=settings.ICPDAO_GITHUB_APP_RSA_PRIVATE_KEY,
        github_owner_name=dao.github_owner_name,
        github_owner_id=dao.github_owner_id,
    )
    app_client = GithubAppClient(app_token, dao.github_owner_name)
    # get all job pr
    job_prs = JobPR.objects(github_pr_id__exists=False).all()
    speed_time = int(time.time())
    print("=== begin migration ===")
    count = 0
    need = len(job_prs)
    for pr in job_prs:
        try:
            success, pr_issue_info = app_client.get_issue(
                pr.github_repo_name,
                pr.github_pr_number,
            )
            if not success:
                print("=== warning === ", pr.to_json())
                continue
            pr.github_pr_id = pr_issue_info['id']
            pr.save()
            count += 1
        except Exception as e:
            print("=== warning === ", pr.to_json(), f'{e}')
    print(f'=== end migration, cost time = {int(time.time()) - speed_time}, need migration = {need}, real migration = {count}')


if __name__ == "__main__":
    main_up()
