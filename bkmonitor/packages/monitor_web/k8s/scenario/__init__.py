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
from collections import namedtuple
from typing import Callable, Dict, List

# 用于动态导入模块
from django.utils.module_loading import import_string

Category = namedtuple("Category", ["id", "name", "children"])

Metric = namedtuple("Metric", ["id", "name", "unit", "unsupported_resource"])


def get_metrics(scenario) -> List[dict]:
    """
    获取指标
    """
    metrics_generator: Callable[..., List[Category]] = import_string(f"{get_metrics.__module__}.{scenario}.get_metrics")
    metrics: List[Category] = metrics_generator()  # 相当于调用 k8s.scenario.performance.get_metrics()

    """
    遍历每个 Category 对象，将其转换为字典格式。
    如果 Category 具有子指标（children），则将每个子指标（Metric 对象）也转换为字典格式。
    最后，将每个 Category 的字典形式添加到 metrics_list 中。
    """
    metrics_list = []
    for category in metrics:
        category_dict: Dict[str, str | List[Metric]] = category._asdict()
        if category_dict["children"]:
            category_dict["children"] = [dict(metric._asdict()) for metric in category_dict["children"]]
        metrics_list.append(dict(category_dict))
    return metrics_list
