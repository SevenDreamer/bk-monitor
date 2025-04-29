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

import pytest  # noqa

from packages.monitor_web.k8s.scenario import Scenario

SCENARIO: Scenario = "capacity"


class TestResourceTrendResourceWithCapacity:
    def test_with_node(self, get_start_time, get_end_time):
        """
        性能场景下pod的数据详情
        """
        validated_request_data = {  # noqa
            "bk_biz_id": 2,
            "bcs_cluster_id": "BCS-K8S-00000",
            "filter_dict": {},
            "column": "column",
            "method": "max",
            "start_time": get_start_time,
            "end_time": get_end_time,
            "scenario": SCENARIO,
        }
