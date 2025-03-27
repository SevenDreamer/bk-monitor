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

import itertools
from typing import List

import mock
import pytest

from monitor_web.k8s.core.filters import load_resource_filter
from monitor_web.k8s.core.meta import (
    K8sNamespaceMeta,
    K8sPodMeta,
    K8sResourceMeta,
    load_resource_meta,
)
from monitor_web.k8s.resources import GetScenarioMetric, ResourceTrendResource


class TestMetaPromQL:
    @staticmethod
    def build_argvalues() -> List[pytest.param]:
        columns = [
            "nw_container_network_transmit_bytes_total",
            "nw_container_network_receive_bytes_total",
            "nw_container_network_receive_errors_ratio",
            "nw_container_network_transmit_errors_ratio",
            "nw_container_network_transmit_errors_total",
            "nw_container_network_receive_errors_total",
            "nw_container_network_receive_packets_total",
            "nw_container_network_transmit_packets_total",
        ]
        argvalues = []

        for column in columns:
            argvalues.append(pytest.param(column, id=f"{column}"))

        return argvalues

    @pytest.mark.parametrize(["column"], build_argvalues())
    def test_meta_by_sort_with_pod(self, column):
        """测试网络场景pod的指标promql是否没有问题"""
        meta: K8sPodMeta = load_resource_meta("pod", 2, "BCS-K8S-00000")
        assert hasattr(meta, f"meta_prom_with_{column}")

        # TODO: 下一步断言完整的promql语句


# TODO: 这个还没有写完
class TestResourceTrend:
    @staticmethod
    def build_argvalues() -> List[pytest.param]:
        scenario = "network"
        columns = [
            "nw_container_network_transmit_bytes_total",
            "nw_container_network_receive_bytes_total",
            "nw_container_network_receive_errors_ratio",
            "nw_container_network_transmit_errors_ratio",
            "nw_container_network_transmit_errors_total",
            "nw_container_network_receive_errors_total",
            "nw_container_network_receive_packets_total",
            "nw_container_network_transmit_packets_total",
        ]
        resource_types = ["namespace", "pod", "ingress", "service"]
        resource_list = ["aiops-default"]
        argvalues = []

        for column, resource_type in itertools.product(columns, resource_types):
            argvalues.append(
                pytest.param(
                    scenario, column, resource_type, resource_list, id=f"{column}-{resource_type}-{resource_list}"
                )
            )

        return argvalues

    @pytest.mark.parametrize(
        ["_scenario", "_column", "_resource_type", "_resource_list"],
        build_argvalues(),
    )
    @mock.patch("core.drf_resource.resource.grafana.graph_unify_query")
    def test_get_resource_trend(
        self, graph_unify_query, _scenario, _column, _resource_type, _resource_list, ensure_test_get_scenario_metric
    ):
        validated_request_data = {
            "resource_list": _resource_list,
            "scenario": _scenario,
            "bcs_cluster_id": "BCS-K8S-00000",
            "start_time": 1742286763,
            "end_time": 1742290363,
            "filter_dict": {},
            "column": _column,
            "method": "sum",
            "resource_type": _resource_type,
            "bk_biz_id": 2,
        }

        # 校验1, 直接从请求参数进行校验
        bk_biz_id = validated_request_data["bk_biz_id"]
        bk_cluster_id = validated_request_data["bcs_cluster_id"]
        resource_type = validated_request_data["resource_type"]
        agg_method = validated_request_data["method"]
        start_time = validated_request_data["start_time"]
        end_time = validated_request_data["end_time"]
        column = validated_request_data["column"]
        scenario = validated_request_data["scenario"]
        resource_list = validated_request_data["resource_list"]

        # meta: K8sResourceMeta = load_resource_meta(
        #     resource_type, bk_biz_id, bk_cluster_id
        # )
        # assert isinstance(meta, K8sNamespaceMeta)

        # # 构造promql
        # meta.set_agg_method(agg_method)  # agg_method -> sum
        # meta.set_agg_interval(start_time, end_time)  # agg_interval -> 1m
        # meta.filter.add(load_resource_filter(resource_type, resource_list))

        # assert (
        #     getattr(meta, f"meta_prom_with_{column}")
        #     == f"""sum by (namespace) (last_over_time(
        #         rate(
        #             {column[3:]}{{
        #                 bcs_cluster_id="BCS-K8S-40000",
        #                 bk_biz_id="2",
        #                 container_name!="POD",
        #                 namespace=~"^(aiops-default|bcs-system)$"
        #             }}[1m]
        #         )[1m:]
        #     ))"""
        # )

        # 校验2, 对最终的结果进行校验
        query_result = [
            {
                "dimensions": {
                    "bcs_cluster_id": "BCS-K8S-00000",
                    "bk_biz_id": "2",
                    "namespace": "aiops-default",
                },
                "target": "{bcs_cluster_id=BCS-K8S-00000, bk_biz_id=2, namespace=aiops-default}",
                "metric_field": "_result_",
                "datapoints": [
                    [0.411495, 1742290260000],
                ],
                "alias": "_result_",
                "type": "line",
                "dimensions_translation": {},
                "unit": "",
            },
        ]
        metric = GetScenarioMetric()({"bk_biz_id": bk_biz_id, "scenario": scenario, "metric_id": column})
        graph_unify_query.return_value = {"series": query_result}
        assert ResourceTrendResource()(validated_request_data) == [
            {
                "resource_name": "aiops-default",
                metric["id"]: {
                    "datapoints": [[0.411495, 1742290260000]],
                    "unit": metric["unit"],
                    "value_title": metric["name"],
                },
            }
        ]


class TestK8sListResource:
    network_resource_type = ["namespace", "ingress", "service", "pod"]
    network_columns = [
        "nw_container_network_transmit_bytes_total",
        "nw_container_network_receive_bytes_total",
        "nw_container_network_receive_errors_ratio",
        "nw_container_network_transmit_errors_ratio",
        "nw_container_network_transmit_errors_total",
        "nw_container_network_receive_errors_total",
        "nw_container_network_receive_packets_total",
        "nw_container_network_transmit_packets_total",
    ]

    def setup_method(self, create_workloads, create_pods, create_containers):
        pass

    def test_with_namespace(self, column, method):
        validated_request_data = {
            "bk_biz_id": 2,
            "bcs_cluster_id": "BCS-K8S-00000",
            "filter_dict": {},
            "column": column,
            "resource_type": "namespace",
            "scenario": "network",
            "start_time": 1742286763,
            "end_time": 1742290363,
            "method": method,
        }

    def test_with_ingress(self):
        pass

    def test_with_service(self):
        pass

    def test_with_pod(self):
        pass
