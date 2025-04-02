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

from monitor_web.k8s.core.filters import ClusterFilter, load_resource_filter
from monitor_web.k8s.core.meta import (
    FilterCollection,
    K8sContainerMeta,
    K8sIngressMeta,
    K8sNamespaceMeta,
    K8sPodMeta,
    K8sServiceMeta,
    K8sWorkloadMeta,
    load_resource_meta,
)
from monitor_web.tests.k8s.test_filter import PodFilter


@pytest.mark.django_db
class TestFilterCollection:
    def test_has_only_fields(self, create_pods):
        """
        测试 meta 有 only_fields 属性时的处理逻辑
        """
        meta = load_resource_meta("pod", 2, "BCS-K8S-00000")
        # assert isinstance(meta, K8sPodMeta)
        # filter_collection = FilterCollection(meta=meta)
        assert len(list(meta.filter.query_set)) > 0
        assert list(meta.filter.query_set) == list(
            meta.resource_class.objects.all().order_by("id").only(*meta.only_fields)
        )

    def test_add_and_remove_filter(self, create_pods):
        """
        测试 add 和 remove 方法
        """
        meta = load_resource_meta("pod", 2, "BCS-K8S-00000")

        space_filter = load_resource_filter("bk_biz_id", meta.bk_biz_id)

        # remove
        meta.filter.remove(space_filter)
        assert space_filter.filter_uid not in meta.filter.filters

        # add
        meta.filter.add(space_filter)
        assert space_filter.filter_uid in meta.filter.filters

    def test_filter_queryset(self, create_pods):
        meta = load_resource_meta("pod", 2, "BCS-K8S-00000")
        query_set = meta.filter.filter_queryset
        assert (
            str(query_set.query)
            == "SELECT `bkmonitor_bcspod`.`id`, `bkmonitor_bcspod`.`bk_biz_id`, `bkmonitor_bcspod`.`bcs_cluster_id`, `bkmonitor_bcspod`.`name`, `bkmonitor_bcspod`.`namespace`, `bkmonitor_bcspod`.`workload_type`, `bkmonitor_bcspod`.`workload_name` FROM `bkmonitor_bcspod` WHERE (`bkmonitor_bcspod`.`bcs_cluster_id` = BCS-K8S-00000 AND `bkmonitor_bcspod`.`bk_biz_id` = 2) ORDER BY `bkmonitor_bcspod`.`id` ASC"
        )

    def test_transform_filter_dict(self, create_pods):
        meta = load_resource_meta("pod", 2, "BCS-K8S-00000")

        # 拿 ClusterFilter的过滤器检查是否有对应的meta
        filter_obj = list(meta.filter.filters.values())[0]
        assert isinstance(filter_obj, ClusterFilter)
        filter_meta = load_resource_meta(filter_obj.resource_type, meta.bk_biz_id, meta.bcs_cluster_id)
        assert filter_meta is None
        assert meta.filter.transform_filter_dict(filter_obj) == filter_obj.filter_dict

        # 传 pod_name 传一个值
        filter_obj = load_resource_filter("pod_name", "test-pod-1")
        assert isinstance(filter_obj, PodFilter)
        filter_meta = load_resource_meta(filter_obj.resource_type, meta.bk_biz_id, meta.bcs_cluster_id)
        assert filter_meta is not None
        assert meta.filter.transform_filter_dict(filter_obj) == {"name": "test-pod-1"}

        # 传 pod_name 并模糊匹配
        filter_obj = load_resource_filter("pod_name", "test-pod-1", True)
        assert meta.filter.transform_filter_dict(filter_obj) == {"name__icontains": "test-pod-1"}

        # 传 pod_name 传多个值
        filter_obj = load_resource_filter("pod_name", ["test-pod-1", "test-pod-2"])
        assert meta.filter.transform_filter_dict(filter_obj) == {"name__in": ["test-pod-1", "test-pod-2"]}


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
