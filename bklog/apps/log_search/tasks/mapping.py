# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making BK-LOG 蓝鲸日志平台 available.
Copyright (C) 2021 THL A29 Limited, a Tencent company.  All rights reserved.
BK-LOG 蓝鲸日志平台 is licensed under the MIT License.
License for BK-LOG 蓝鲸日志平台:
--------------------------------------------------------------------
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
We undertake not to change the open source license (MIT license) applicable to the current version of
the project delivered to anyone in the future.
"""
from datetime import datetime, timedelta

from blueapps.contrib.celery_tools.periodic import periodic_task
from blueapps.core.celery.celery import app
from celery.schedules import crontab

from apps.exceptions import ApiResultError
from apps.log_search.constants import BkDataErrorCode
from apps.log_search.models import LogIndexSet, UserIndexSetSearchHistory
from apps.utils.log import logger
from apps.utils.task import high_priority_task


@periodic_task(run_every=crontab(minute="*/10"))
def sync_index_set_mapping_snapshot():
    logger.info("[sync_index_set_mapping_snapshot] task publish start")
    # 仅更新近一周用户检索过的索引集快照
    index_set_ids = list(
        UserIndexSetSearchHistory.objects.filter(created_at__gte=datetime.now() - timedelta(days=1)).values_list(
            "index_set_id", flat=True
        )
    )
    index_set_list = LogIndexSet.objects.filter(index_set_id__in=index_set_ids, is_active=True)

    for index_set in index_set_list:
        sync_single_index_set_mapping_snapshot_periodic.delay(index_set.index_set_id)

    logger.info(f"[sync_index_set_mapping_snapshot] task publish end, total: {len(index_set_list)}")


def sync_mapping_snapshot_subtask(index_set_id=None):
    try:
        index_set_obj = LogIndexSet.objects.get(index_set_id=index_set_id)
    except LogIndexSet.DoesNotExist:
        logger.exception(f"[sync_single_index_set_mapping_snapshot]index_set({index_set_id}) not exist")
        return

    try:
        index_set_obj.sync_fields_snapshot()
    except ApiResultError as e:
        # 当数据平台返回为无法获取元数据报错情况
        if e.code in [BkDataErrorCode.STORAGE_TYPE_ERROR, BkDataErrorCode.COULD_NOT_GET_METADATA_ERROR]:
            index_set_obj.is_active = False
            index_set_obj.save()
        logger.exception(
            f"[sync_single_index_set_mapping_snapshot] index_set({index_set_obj.index_set_id} call mapping error: {e})"
        )
    except Exception as e:  # pylint: disable=broad-except
        logger.exception(
            f"[sync_single_index_set_mapping_snapshot] index_set({index_set_obj.index_set_id}) sync failed: {e}"
        )
    else:
        logger.info(f"[sync_single_index_set_mapping_snapshot] index_set({index_set_obj.index_set_id}) sync success")


@app.task(ignore_result=True)
def sync_single_index_set_mapping_snapshot_periodic(index_set_id=None):  # pylint: disable=function-name-too-long
    sync_mapping_snapshot_subtask(index_set_id)


@high_priority_task(ignore_result=True)
def sync_single_index_set_mapping_snapshot(index_set_id=None):  # pylint: disable=function-name-too-long
    sync_mapping_snapshot_subtask(index_set_id)
