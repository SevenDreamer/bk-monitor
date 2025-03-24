# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云 - 监控平台 (BlueKing - Monitor) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""


import pytest
from django.test import TestCase
from django.utils import timezone

from bkmonitor.models import BCSCluster

pytestsmark = pytest.mark.django_db


def pytest_configure():
    TestCase.databases = {"default", "monitor_api"}


@pytest.fixture()
def create_bcs_cluster(db):
    BCSCluster(
        bk_biz_id=2,
        bcs_cluster_id="BCS-K8S-00000",
        name="蓝鲸7.0",
        area_name="",
        project_name="",
        environment="正式",
        updated_at=timezone.now(),
        node_count=18,
        cpu_usage_ratio=19.22,
        memory_usage_ratio=65.36,
        disk_usage_ratio=51.45,
        created_at=timezone.now(),
        status="RUNNING",
        monitor_status="success",
        last_synced_at=timezone.now(),
    ).save()
