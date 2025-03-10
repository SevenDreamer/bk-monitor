# 接口

## ListBCSCluster

获取集群列表

### 请求方法

GET

### 请求 url

rest/v2/k8s/resources/list_bcs_cluster/

### 请求参数

| 字段      | 类型 | 必选 | 描述    |
|-----------|------|-----|-------|
| bk_biz_id | int  | 是   | 业务 id |

### 请求示例

```json
{"bk_biz_id": 2}
```

### 响应示例

```json
[
  {
    "id": "BCS-K8S-00000",
    "name": "蓝鲸7.0(BCS-K8S-00000)"
  }
]
```

## ScenarioMetricList

获取指定场景的指标列表

目前支持性能和网络两种场景

### 请求方法

GET

### 请求 url

rest/v2/k8s/resources/scenario_metric_list/

### 请求参数

| 字段      | 类型 | 必选 | 描述                                   |
|-----------|------|-----|--------------------------------------|
| bk_biz_id | int  | 是   | 业务 id                                |
| scenario  | str  | 是   | 接入场景, \["performance", "network"\] |

### 请求示例

#### 获取性能场景的指标

```json
{
    "bk_biz_id": 2,
    "scenario": "performance"
}
```

#### 获取网络场景的指标

```json
{
    "bk_biz_id": 2,
    "scenario": "network"
}
```

### 响应示例

#### 获取性能场景的指标

```json
[
  {
    "id": "CPU",
    "name": "CPU",
    "children": [
      {
        "id": "container_cpu_usage_seconds_total",
        "name": "CPU使用量",
        "unit": "core",
        "unsupported_resource": []
      },
      {
        "id": "kube_pod_cpu_requests_ratio",
        "name": "CPU request使用率",
        "unit": "percentunit",
        "unsupported_resource": [
          "namespace"
        ]
      },
      {
        "id": "kube_pod_cpu_limits_ratio",
        "name": "CPU limit使用率",
        "unit": "percentunit",
        "unsupported_resource": [
          "namespace"
        ]
      },
      {
        "id": "container_cpu_cfs_throttled_ratio",
        "name": "CPU 限流占比",
        "unit": "percentunit",
        "unsupported_resource": []
      }
    ]
  },
  {
    "id": "memory",
    "name": "内存",
    "children": [
      {
        "id": "container_memory_working_set_bytes",
        "name": "内存使用量(Working Set)",
        "unit": "bytes",
        "unsupported_resource": []
      },
      {
        "id": "kube_pod_memory_requests_ratio",
        "name": "内存 request使用率",
        "unit": "percentunit",
        "unsupported_resource": [
          "namespace"
        ]
      },
      {
        "id": "kube_pod_memory_limits_ratio",
        "name": "内存 limit使用率",
        "unit": "percentunit",
        "unsupported_resource": [
          "namespace"
        ]
      }
    ]
  },
  {
    "id": "network",
    "name": "流量",
    "children": [
      {
        "id": "container_network_receive_bytes_total",
        "name": "网络入带宽",
        "unit": "Bps",
        "unsupported_resource": [
          "container"
        ]
      },
      {
        "id": "container_network_transmit_bytes_total",
        "name": "网络出带宽",
        "unit": "Bps",
        "unsupported_resource": [
          "container"
        ]
      }
    ]
  }
]
```

#### 获取网络场景的指标

```json
[
  {
    "id": "traffic",
    "name": "流量",
    "children": [
      {
        "id": "nw_container_network_receive_bytes_total",
        "name": "网络入带宽",
        "unit": "Bps",
        "unsupported_resource": []
      },
      {
        "id": "nw_container_network_transmit_bytes_total",
        "name": "网络出带宽",
        "unit": "Bps",
        "unsupported_resource": [
          "namespace"
        ]
      }
    ]
  },
  {
    "id": "packets",
    "name": "包量",
    "children": [
      {
        "id": "nw_container_network_receive_packets_total",
        "name": "网络入包量",
        "unit": "pps",
        "unsupported_resource": []
      },
      {
        "id": "nw_container_network_transmit_packets_total",
        "name": "网络出包量",
        "unit": "pps",
        "unsupported_resource": []
      },
      {
        "id": "nw_container_network_receive_errors_total",
        "name": "网络入丢包量",
        "unit": "pps",
        "unsupported_resource": []
      },
      {
        "id": "nw_container_network_transmit_errors_total",
        "name": "网络出丢包量",
        "unit": "pps",
        "unsupported_resource": []
      },
      {
        "id": "nw_container_network_receive_errors_ratio",
        "name": "网络入丢包率",
        "unit": "pps",
        "unsupported_resource": []
      },
      {
        "id": "nw_container_network_transmit_errors_ratio",
        "name": "网络出丢包率",
        "unit": "pps",
        "unsupported_resource": []
      }
    ]
  }
]
```

## ListK8SResources

获取 k8s 集群资源列表

### 请求方法

POST

### 请求 url

rest/v2/k8s/resources/list_resources/

### 请求参数

| 字段           | 类型 | 必选 | 描述                                                                            |
|----------------|------|-----|-------------------------------------------------------------------------------|
| bk_biz_id      | int  | 是   | 业务 id                                                                         |
| bcs_cluster_id | str  | 是   | 集群id                                                                          |
| filter_dict    | dict | 否   | 精确过滤字典                                                                    |
| resource_type  | str  | 是   | 资源类型, \["pod", "workload", "namespace", "container", "ingress", "service"\] |
| query_string   | str  | 否   | 名字过滤, 用于模糊查询                                                          |
| start_time     | int  | 是   | 开始时间                                                                        |
| end_time       | int  | 是   | 结束时间                                                                        |
| scenario       | str  | 是   | 场景, \["performance", "network"\]                                              |
| with_history   | bool | 否   | 是否查询包含历史的资源                                                          |
| page_size      | int  | 否   | 分页大小, 默认为5                                                               |
| page           | int  | 否   | 页数, 默认为1                                                                   |
| page_type      | str  | 否   | 分页标识, 默认为"scrolling", \["scrolling", "traditional"\]                     |
| order_by       | str  | 否   | 排序, 默认为"desc", \["desc", "asc"\]                                           |
| method         | str  | 否   | 聚合方法, 默认"sum", \["max", "avg", "min", "sum", "count"\]                    |
| column         | str  | 否   | [指标名](#指标列表), 默认为"container_cpu_usage_seconds_total"                  |

### 示例

#### 示例 1

TODO 等待真实数据进行不全

返回pod资源类型5条内容

##### 请求响应

```json
{
  "bk_biz_id": 2,
  "bcs_cluster_id": "BCS-K8S-00000",
  "resource_type": "pod",
  "start_time": 1732240257,
  "end_time": 1732243857,
  "sernario": "performance"
}
```

##### 响应示例

```json
{
  "result": true,
  "code": 200,
  "message": "OK",
  "data": {
    "count": 163,
    "items": [
      {
        "pod": "pod-1",
        "namespace": "default",
        "workload": "Deployment:workload-1"
      },
      {
        "pod": "pod-2",
        "namespace": "default",
        "workload": "Deployment:workload-1"
      },
      {
        "pod": "pod-3",
        "namespace": "default",
        "workload": "Deployment:workload-2"
      },
      {
        "pod": "pod-4",
        "namespace": "default",
        "workload": "Deployment:workload-2"
      },
      {
        "pod": "pod-5",
        "namespace": "default",
        "workload": "Deployment:workload-3"
      }
    ]
  }
}
```

## GetResourceDetail

获取指定资源的详情

### 请求方法

GET

### 请求 url

rest/v2/k8s/resources/get_resource_detail

### 请求参数

| 字段           | 类型 | 必选 | 描述                                                   |
|----------------|------|-----|------------------------------------------------------|
| bk_biz_id      | int  | 是   | 业务 id                                                |
| bcs_cluster_id | str  | 是   | 集群id                                                 |
| namespace      | str  | 是   | 命名空间                                               |
| resource_type  | str  | 是   | 资源类型,\["pod", "workload", "container", "cluster"\] |
| pod_name       | str  | 否   | pod 名称                                               |
| container_name | str  | 否   | container 名称                                         |
| workload_name  | str  | 否   | workload 名称                                          |
| workload_type  | str  | 否   | workload 类型                                          |

### 请求示例

```json
{
  "bk_biz_id": 2,
  "pod_name": "python-backend--0--session-default---experiment-clear-backbvcgm",
  "resource_type": "pod",
  "namespace": "aiops-default",
  "bcs_cluster_id": "BCS-K8S-00000"
}
```

### 响应示例

```json
[
  {
    "key": "name",
    "name": "Pod名称",
    "type": "string",
    "value": "python-backend--0--session-default---experiment-clear-backbvcgm"
  },
  {
    "key": "status",
    "name": "运行状态",
    "type": "string",
    "value": "Running"
  },
  {
    "key": "ready",
    "name": "是否就绪(实例运行数/期望数)",
    "type": "string",
    "value": "1/1"
  },
  {
    "key": "bcs_cluster_id",
    "name": "集群ID",
    "type": "string",
    "value": "BCS-K8S-00000"
  },
  {
    "key": "bk_cluster_name",
    "name": "集群名称",
    "type": "string",
    "value": "蓝鲸7.0"
  },
  {
    "key": "namespace",
    "name": "NameSpace",
    "type": "string",
    "value": "aiops-default"
  },
  {
    "key": "total_container_count",
    "name": "容器数量",
    "type": "string",
    "value": 1
  },
  {
    "key": "restarts",
    "name": "重启次数",
    "type": "number",
    "value": 0
  },
  {
    "key": "monitor_status",
    "name": "采集状态",
    "type": "status",
    "value": {
      "type": "success",
      "text": "正常"
    }
  },
  {
    "key": "age",
    "name": "存活时间",
    "type": "string",
    "value": "2 months"
  },
  {
    "key": "request_cpu_usage_ratio",
    "name": "CPU使用率(request)",
    "type": "progress",
    "value": {
      "value": 0.7,
      "label": "0.7%",
      "status": "SUCCESS"
    }
  },
  {
    "key": "limit_cpu_usage_ratio",
    "name": "CPU使用率(limit)",
    "type": "progress",
    "value": {
      "value": 0.35,
      "label": "0.35%",
      "status": "SUCCESS"
    }
  },
  {
    "key": "request_memory_usage_ratio",
    "name": "内存使用率(request)",
    "type": "progress",
    "value": {
      "value": 12.12,
      "label": "12.12%",
      "status": "SUCCESS"
    }
  },
  {
    "key": "limit_memory_usage_ratio",
    "name": "内存使用率(limit) ",
    "type": "progress",
    "value": {
      "value": 6.06,
      "label": "6.06%",
      "status": "SUCCESS"
    }
  },
  {
    "key": "resource_usage_cpu",
    "name": "CPU使用量",
    "type": "string",
    "value": "7m"
  },
  {
    "key": "resource_usage_memory",
    "name": "内存使用量",
    "type": "string",
    "value": "497MB"
  },
  {
    "key": "resource_usage_disk",
    "name": "磁盘使用量",
    "type": "string",
    "value": "2GB"
  },
  {
    "key": "resource_requests_cpu",
    "name": "cpu request",
    "type": "string",
    "value": "1000m"
  },
  {
    "key": "resource_limits_cpu",
    "name": "cpu limit",
    "type": "string",
    "value": "2000m"
  },
  {
    "key": "resource_requests_memory",
    "name": "memory request",
    "type": "string",
    "value": "4GB"
  },
  {
    "key": "resource_limits_memory",
    "name": "memory limit",
    "type": "string",
    "value": "8GB"
  },
  {
    "key": "pod_ip",
    "name": "Pod IP",
    "type": "string",
    "value": "127.0.0.1"
  },
  {
    "key": "node_ip",
    "name": "节点IP",
    "type": "string",
    "value": "127.0.0.1"
  },
  {
    "key": "node_name",
    "name": "节点名称",
    "type": "string",
    "value": "node-127-0-0-1"
  },
  {
    "key": "workload",
    "name": "工作负载",
    "type": "string",
    "value": "Deployment:python-backend--0--session-default---experiment-clear-backend---owned"
  },
  {
    "key": "label_list",
    "name": "标签",
    "type": "kv",
    "value": []
  },
  {
    "key": "images",
    "name": "镜像",
    "type": "list",
    "value": [
      "mirrors.tencent.com/build/blueking/bkbase-aiops:1.12.30"
    ]
  }
]
```

## WorkloadOverview

### 请求方法

GET

### 请求 url

rest/v2/k8s/resources/workload_overview/

### 请求参数

| 字段           | 类型 | 必选 | 描述     |
|----------------|------|-----|--------|
| bk_biz_id      | int  | 是   | 业务 id  |
| bcs_cluster_id | str  | 是   | 集群id   |
| namespace      | str  | 否   | 命名空间 |
| query_string   | str  | 否   | 名字过滤 |

### 请求示例

```json
{
  "bk_biz_id": 2,
  "bcs_cluster_id": "BCS-K8S-00000"
}
```

### 响应示例

```json
[
  [ "Deployment", 608 ],
  [ "StatefulSet", 68 ],
  [ "DaemonSet", 11 ],
  [ "Job", 628 ],
  [ "CronJob", 7 ]
]
```

## ResourceTrendResource

### 请求方法

POST

### 请求 url

rest/v2/k8s/resources/resource_trend/

### 请求参数

| 字段           | 类型        | 必选 | 描述                                                                            |
|----------------|-------------|-----|-------------------------------------------------------------------------------|
| bk_biz_id      | int         | 是   | 业务 id                                                                         |
| filter_dict    | dict        | 否   | 精确过滤字典                                                                    |
| bcs_cluster_id | str         | 是   | 集群id                                                                          |
| column         | str         | 是   | [指标名](#指标列表)                                                             |
| resource_type  | str         | 是   | 资源类型, \["pod", "workload", "namespace", "container", "ingress", "service"\] |
| method         | str         | 是   | 聚合方法, \["max", "avg", "min", "sum", "count"\]                               |
| resource_list  | List\[str\] | 是   | 资源列表                                                                        |
| start_time     | int         | 是   | 开始时间                                                                        |
| end_time       | int         | 是   | 结束时间                                                                        |
| scenario       | str         | 是   | 接入场景, \["performance", "network"\]                                          |

### 请求示例

```json
{
    "scenario": "performance",
    "bcs_cluster_id": "BCS-K8S-00000",
    "start_time": 1741597068,
    "end_time": 1741600668,
    "filter_dict": {},
    "column": "container_cpu_cfs_throttled_ratio",
    "method": "sum",
    "resource_type": "namespace",
    "resource_list": [
        "bkmonitor-operator",
        "bkbase-flink",
        "bkmonitor-operator-bkte",
        "bkbase",
        "blueking",
        "deepflow",
        "trpc-micros-stag",
        "kube-system",
        "bk-bscp",
        "bk-system",
        "aiops-default",
        "bcs-system",
        "bkapp-bkaidev-prod",
        "bkapp-csu230208-stag",
        "bkapp-bk0us0cmdb0us0saas-prod",
        "bkapp-bkbase0us0admin0us0t-m-backend-stag",
        "bkapp-bk0us0dataweb-m-aiops-prod",
        "bkapp-bk0us0sops-m-pipeline-prod",
        "bkapp-bk0us0sops-m-pipeline-stag",
        "bkapp-csu230512-stag"
    ],
    "bk_biz_id": 2
}
```

### 响应示例

```json
[
  {
    "resource_name": "aiops-default",
    "container_cpu_cfs_throttled_ratio": {
      "datapoints": [
        [
          0.002558,
          1741600560000
        ]
      ],
      "unit": "percentunit",
      "value_title": "CPU 限流占比"
    }
  },
  {
    "resource_name": "bcs-system",
    "container_cpu_cfs_throttled_ratio": {
      "datapoints": [
        [
          0,
          1741600560000
        ]
      ],
      "unit": "percentunit",
      "value_title": "CPU 限流占比"
    }
  },
  {
    "resource_name": "bk-bscp",
    "container_cpu_cfs_throttled_ratio": {
      "datapoints": [
        [
          0.466171,
          1741600560000
        ]
      ],
      "unit": "percentunit",
      "value_title": "CPU 限流占比"
    }
  },
  {
    "resource_name": "bk-system",
    "container_cpu_cfs_throttled_ratio": {
      "datapoints": [
        [
          0.013289,
          1741600560000
        ]
      ],
      "unit": "percentunit",
      "value_title": "CPU 限流占比"
    }
  },
  {
    "resource_name": "bkapp-bk0us0cmdb0us0saas-prod",
    "container_cpu_cfs_throttled_ratio": {
      "datapoints": [
        [
          0,
          1741600560000
        ]
      ],
      "unit": "percentunit",
      "value_title": "CPU 限流占比"
    }
  },
  {
    "resource_name": "bkapp-bk0us0dataweb-m-aiops-prod",
    "container_cpu_cfs_throttled_ratio": {
      "datapoints": [
        [
          0,
          1741600560000
        ]
      ],
      "unit": "percentunit",
      "value_title": "CPU 限流占比"
    }
  },
  {
    "resource_name": "bkapp-bk0us0sops-m-pipeline-prod",
    "container_cpu_cfs_throttled_ratio": {
      "datapoints": [
        [
          0,
          1741600560000
        ]
      ],
      "unit": "percentunit",
      "value_title": "CPU 限流占比"
    }
  },
  {
    "resource_name": "bkapp-bk0us0sops-m-pipeline-stag",
    "container_cpu_cfs_throttled_ratio": {
      "datapoints": [
        [
          0,
          1741600560000
        ]
      ],
      "unit": "percentunit",
      "value_title": "CPU 限流占比"
    }
  },
  {
    "resource_name": "bkapp-bkaidev-prod",
    "container_cpu_cfs_throttled_ratio": {
      "datapoints": [
        [
          0,
          1741600560000
        ]
      ],
      "unit": "percentunit",
      "value_title": "CPU 限流占比"
    }
  },
  {
    "resource_name": "bkapp-bkbase0us0admin0us0t-m-backend-stag",
    "container_cpu_cfs_throttled_ratio": {
      "datapoints": [
        [
          0,
          1741600560000
        ]
      ],
      "unit": "percentunit",
      "value_title": "CPU 限流占比"
    }
  },
  {
    "resource_name": "bkapp-csu230208-stag",
    "container_cpu_cfs_throttled_ratio": {
      "datapoints": [
        [
          0,
          1741600560000
        ]
      ],
      "unit": "percentunit",
      "value_title": "CPU 限流占比"
    }
  },
  {
    "resource_name": "bkapp-csu230512-stag",
    "container_cpu_cfs_throttled_ratio": {
      "datapoints": [
        [
          0,
          1741600560000
        ]
      ],
      "unit": "percentunit",
      "value_title": "CPU 限流占比"
    }
  },
  {
    "resource_name": "bkbase",
    "container_cpu_cfs_throttled_ratio": {
      "datapoints": [
        [
          4.702747,
          1741600560000
        ]
      ],
      "unit": "percentunit",
      "value_title": "CPU 限流占比"
    }
  },
  {
    "resource_name": "bkbase-flink",
    "container_cpu_cfs_throttled_ratio": {
      "datapoints": [
        [
          7.459486,
          1741600560000
        ]
      ],
      "unit": "percentunit",
      "value_title": "CPU 限流占比"
    }
  },
  {
    "resource_name": "bkmonitor-operator",
    "container_cpu_cfs_throttled_ratio": {
      "datapoints": [
        [
          18.265733,
          1741600560000
        ]
      ],
      "unit": "percentunit",
      "value_title": "CPU 限流占比"
    }
  },
  {
    "resource_name": "bkmonitor-operator-bkte",
    "container_cpu_cfs_throttled_ratio": {
      "datapoints": [
        [
          5.414493,
          1741600560000
        ]
      ],
      "unit": "percentunit",
      "value_title": "CPU 限流占比"
    }
  },
  {
    "resource_name": "blueking",
    "container_cpu_cfs_throttled_ratio": {
      "datapoints": [
        [
          4.240089,
          1741600560000
        ]
      ],
      "unit": "percentunit",
      "value_title": "CPU 限流占比"
    }
  },
  {
    "resource_name": "deepflow",
    "container_cpu_cfs_throttled_ratio": {
      "datapoints": [
        [
          1.544696,
          1741600560000
        ]
      ],
      "unit": "percentunit",
      "value_title": "CPU 限流占比"
    }
  },
  {
    "resource_name": "kube-system",
    "container_cpu_cfs_throttled_ratio": {
      "datapoints": [
        [
          0.556802,
          1741600560000
        ]
      ],
      "unit": "percentunit",
      "value_title": "CPU 限流占比"
    }
  },
  {
    "resource_name": "trpc-micros-stag",
    "container_cpu_cfs_throttled_ratio": {
      "datapoints": [
        [
          1.086197,
          1741600560000
        ]
      ],
      "unit": "percentunit",
      "value_title": "CPU 限流占比"
    }
  }
]
```

# 其他待处理

## 指标列表

checked 记得删除这行

| 值                                          | 描述                    |
|---------------------------------------------|-----------------------|
| container_cpu_usage_seconds_total           | CPU使用量               |
| kube_pod_cpu_requests_ratio                 | CPU request使用率       |
| kube_pod_cpu_limits_ratio                   | CPU limit使用率         |
| container_memory_working_set_bytes          | 内存使用量(Working Set) |
| kube_pod_memory_requests_ratio              | 内存 request使用率      |
| kube_pod_memory_limits_ratio                | 内存 limit使用率        |
| container_cpu_cfs_throttled_ratio           | CPU 限流占比            |
| container_network_transmit_bytes_total      | 网络出带宽              |
| container_network_receive_bytes_total       | 网络入带宽              |
| nw_container_network_transmit_bytes_total   | 网络出带宽              |
| nw_container_network_receive_bytes_total    | 网络入带宽              |
| nw_container_network_receive_errors_ratio   | 网络入丢包率            |
| nw_container_network_transmit_errors_ratio  | 网络出丢包率            |
| nw_container_network_transmit_errors_total  | 网络出丢包量            |
| nw_container_network_receive_errors_total   | 网络入丢包量            |
| nw_container_network_receive_packets_total  | 网络入包量              |
| nw_container_network_transmit_packets_total | 网络出包量              |

# 源码解读

## k8s.core.errors.K8sResourceNotFound

找不到对应的资源类型
例如当前端传来 resource_type 为 xxx，不属于现有支持的 resource_type

## k8s.core.errors.MultiWorkloadError

不支持多个 workload 查询

## k8s.core.filters.filter_options

全局字典，用于存储注册的 [过滤器类 ResourceFilter](#k8scorefiltersresourcefilterobject)。
通过类的 `resource_type` 属性，可以将不同类型的过滤器与它们对应的类关联起来。

## k8s.core.filters.ResourceFilter(object)
