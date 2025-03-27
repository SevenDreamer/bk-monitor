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

from monitor_web.k8s.core.meta import (
    K8sContainerMeta,
    K8sIngressMeta,
    K8sNamespaceMeta,
    K8sPodMeta,
    K8sServiceMeta,
    K8sWorkloadMeta,
    load_resource_meta,
)


class TestK8sResourceMeta:
    def test_get_from_meta(self):
        ...

    def test_get_from_promql(self):
        ...

    @pytest.mark.parametrize(
        ["resource_type", "order_by"],
        [
            ["pod", "column"],
        ],
    )
    def test_meta_by_sort(self, resource_type, order_by: str):
        pass
        # meta = load_resource_meta("pod", 2, "BCS-K8S-00000")
        # column = order_by.strip("-")

        # meta_prom_func = f"meta_prom_with_{column}"
        # assert hasattr(meta, meta_prom_func)

        # if order_by.startswith("-"):
        #     promql = f"topk(20, {getattr(meta, meta_prom_func)})"
        # else:
        #     promql = f"topk(20, {getattr(meta, meta_prom_func)} * -1) * -1"

        # assert promql == f"topk(20, )"

    def test_with_k8s_pod_meta(self):
        ...

    def test_with_k8s_node_meta(self):
        ...

    def test_with_k8s_naespace_meta(self):
        ...

    def test_with_k8s_ingress_meta(self):
        ...

    def test_with_k8s_service_meta(self):
        ...

    def test_with_k8s_workload_meta(self):
        ...

    def test_with_k8s_container_meta(self):
        ...


@pytest.mark.parametrize(
    ["resource_type", "meta_class"],
    [
        # ["node", K8sNodeMeta],  # 目前暂不可用
        ["container", K8sContainerMeta],
        ["container_name", K8sContainerMeta],
        ["pod", K8sPodMeta],
        ["pod_name", K8sPodMeta],
        ["workload", K8sWorkloadMeta],
        ["namespace", K8sNamespaceMeta],
        ["ingress", K8sIngressMeta],
        ["service", K8sServiceMeta],
    ],
)
def test_load_resource_meta(resource_type, meta_class):
    meta = load_resource_meta(resource_type, 2, "BCS-K8S-00000")
    assert isinstance(meta, meta_class)
