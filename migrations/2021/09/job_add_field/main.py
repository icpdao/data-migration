import sys
import os
sys.path.append(os.path.abspath('../../../../'))
import settings

from common.models.icpdao import init_mongo

from common.models.icpdao.job import Job

init_mongo({
    'icpdao': {
        'host': settings.ICPDAO_MONGODB_ICPDAO_HOST,
        'alias': 'icpdao',
    }
})


def main_up():
    print(Job.objects().count())
    pass


if __name__ == "__main__":
    main_up()
