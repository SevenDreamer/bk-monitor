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

from typing import Dict

from monitor_web.k8s.core.errors import K8sResourceNotFound, MultiWorkloadError

filter_options = {}


def register_filter(filter_cls):
    global filter_options
    filter_options[filter_cls.resource_type] = filter_cls
    return filter_cls


class ResourceFilter(object):
    """
    特定资源过滤器的基类
    """

    resource_type = ""  # 可以理解为是表名
    filter_field = ""  # 可以理解为是这个表唯二的字段

    def __init__(self, value, fuzzy=False):
        """
        接受一个值和一个可选的模糊搜索标志。
        确保 value 是一个 List | Tuple，并将其转换为 List[str]，
        最后对其进行排序。
        """
        if not isinstance(value, (list, tuple)):
            value = [value]
        value = list(map(str, value))
        self.value = sorted(value)
        self.fuzzy = fuzzy

    @property
    def filter_uid(self):
        """
        返回一个唯一的标识符
        由 resource_type + filter_field + value 构成
        相当于，表名+字段名+值
        """
        return f"{self.resource_type}{self.filter_field}{self.value}"

    @property
    def filter_dict(self) -> Dict:
        """
        用于构建查询条件
        根据 value 的长度和 fuzzy 标志，它构建相应的查询条件

        如果只有一个值且 fuzzy 为 True，则使用模糊匹配。
        如果只有一个值且 fuzzy 为 False，则直接匹配。
        如果有多个值，则使用 __in 进行查询。
        """
        if len(self.value) == 1:
            if self.fuzzy:
                return {f"{self.filter_field}__icontains": self.value[0]}
            return {self.filter_field: self.value[0]}
        return {f"{self.filter_field}__in": self.value}

    def filter_string(self) -> str:
        """
        用于构建查询条件
        根据 value 的长度和 fuzzy 标志，构建相应的查询字符串：

        如果 fuzzy 为 True，调用 fuzzy_filter_string 方法。 => `key=~"value1|value2|..."`
        如果只有一个值，构建简单的等式。 => `key=value`
        如果有多个值，构建正则表达式匹配 => `key=~"^(value1|value2|...)$"`
        """
        if self.fuzzy:
            return self.fuzzy_filter_string()
        if len(self.value) == 1:
            return f'{self.filter_field}="{self.value[0]}"'
        value_regex = "|".join(self.value)
        return f'{self.filter_field}=~"^({value_regex})$"'

    def fuzzy_filter_string(self) -> str:
        return f'''{self.filter_field}=~"({"|".join(self.value)})"'''


@register_filter
class NamespaceFilter(ResourceFilter):
    resource_type = "namespace"
    filter_field = "namespace"


@register_filter
class PodFilter(ResourceFilter):
    resource_type = "pod"
    filter_field = "pod_name"


@register_filter
class WorkloadFilter(ResourceFilter):
    resource_type = "workload"
    filter_field = "workload"

    @property
    def filter_dict(self) -> Dict[str, str]:
        filter = {}  # 初始化一个字典，用于存储构建的过滤条件。

        # 检查传入的值的数量。如果超过一个值，抛出 MultiWorkloadError 异常，表示不支持多个工作负载的过滤。
        if len(self.value) > 1:
            raise MultiWorkloadError()

        # 将传入的第一个值按冒号 : 分割为工作负载类型和名称。只分割一次，因此最多会得到两个部分
        parsed = self.value[0].split(":", 1)
        # 分割结果包含两个部分，表示用户提供了工作负载类型和名称
        if len(parsed) == 2:
            workload_kind, workload_name = self.value[0].split(":")

            if workload_kind:
                filter["workload_kind"] = workload_kind.strip()
            if workload_name:
                filter["workload_name"] = workload_name.strip()
        # 如果只提供了一个值，检查 fuzzy 标志：
        # 如果 fuzzy 为 True，则使用 __icontains 进行模糊匹配。
        # 否则，进行精确匹配。
        else:
            if self.fuzzy:
                filter["workload_name__icontains"] = self.value[0].strip()
            else:
                filter["workload_name"] = self.value[0].strip()

        return filter

    def filter_string(self) -> str:
        if self.fuzzy:
            # e.g. 'workload_name=~"name1|name2"'
            return f'''workload_name=~"{self.value[0].strip()}"'''

        # e.g. "field1=value1, field2=value2, ..."
        where = ""
        for field, value in self.filter_dict.items():
            where += "," if where else ""
            where += f'{field}="{value}"'
        return where


@register_filter
class ContainerFilter(ResourceFilter):
    resource_type = "container"
    filter_field = "container_name"


@register_filter
class DefaultContainerFilter(ResourceFilter):
    resource_type = "container_exclude"
    filter_field = "container_name"

    def filter_string(self):
        return 'container_name!="POD"'

    @property
    def filter_dict(self):
        return {}


@register_filter
class NodeFilter(ResourceFilter):
    resource_type = "node"
    filter_field = "node"


@register_filter
class ClusterFilter(ResourceFilter):
    resource_type = "bcs_cluster_id"
    filter_field = "bcs_cluster_id"


@register_filter
class SpaceFilter(ResourceFilter):
    resource_type = "bk_biz_id"
    filter_field = "bk_biz_id"


@register_filter
class IngressFilter(ResourceFilter):
    resource_type = "ingress"
    filter_field = "ingress"


@register_filter
class ServiceFilter(ResourceFilter):
    resource_type = "service"
    filter_field = "service"


def load_resource_filter(resource_type: str, filter_value, fuzzy=False) -> ResourceFilter:
    # 根据给定的资源类型、过滤值和模糊匹配标志来加载对应的资源过滤器
    if resource_type not in filter_options:
        # 兼容xxx_name字段
        if resource_type.endswith("_name"):
            return load_resource_filter(resource_type.split("_name")[0], filter_value, fuzzy)
        raise K8sResourceNotFound(resource_type=resource_type)
    # 返回实例化的过滤器对象
    filter_obj = filter_options[resource_type](filter_value, fuzzy)
    return filter_obj
