# 主机列表 K8s 告警计数不显示 — 问题分析与修复

## 问题描述

主机列表页面中，部分主机明明有关联的告警事件（可在告警事件页面看到），但主机列表上"危险/严重"等告警级别标识显示为 0。

---

## 涉及的完整调用链

```
前端 GET /host_list/?bk_biz_id=xxx
  └─ HostListViewSet                                  (performance/views.py:49)
    └─ HostPerformanceResource.perform_request          (performance/resources.py:67)
      └─ [并发线程] get_alarm_count                      (performance/resources.py:54)
        └─ resource.cc.get_host_alarm_count(...)         (performance/resources.py:58)
          └─ get_host_alarm_count()                      (cc/resources/cmdb.py:449)
            ├─ 查 ES: AlertDocument.search(days=7)
            │    .filter(status=ABNORMAL, event.bk_biz_id=xxx)
            │    .source(["event.ip", "event.bk_cloud_id", "severity"])
            ├─ 构建映射: {(host.ip, host.bk_cloud_id) → host.bk_host_id}
            └─ 遍历告警:
                 ip = alert.event.ip          ← K8s告警此处为空！
                 bk_cloud_id = alert.event.bk_cloud_id
                 → 匹配失败 → continue → 计数为 0
```

---

## 涉及的接口和文件

### 查询侧

| 组件 | 文件 | 行号 | 说明 |
|------|------|------|------|
| `HostListViewSet` | `packages/monitor_web/performance/views.py` | :49 | 注册为 `/host_list/` 接口 |
| `HostPerformanceResource` | `packages/monitor_web/performance/resources.py` | :24 | 主机列表核心 Resource |
| `perform_request` | `packages/monitor_web/performance/resources.py` | :67 | 并发获取主机信息（Agent/性能/进程/告警） |
| `get_alarm_count` | `packages/monitor_web/performance/resources.py` | :54 | 调用 cc 模块的告警计数接口 |
| **`get_host_alarm_count`** | **`packages/monitor_web/cc/resources/cmdb.py`** | **:449** | **核心：从 ES 查告警并匹配主机** |

### 数据写入侧（Enricher 丰富化器）

#### 注册表 — `alarm_backends/service/alert/enricher/__init__.py`

**事件级 Enricher（:33-37）：**
```python
INSTALLED_EVENT_ENRICHER = [
    PreEventEnricher,         # :34
    CMDBEnricher,             # :35 ← 传统主机告警处理
    BizWhiteListFor3rdEvent,  # :36
]
```

**告警级 Enricher（:39-46）：**
```python
INSTALLED_AlERT_ENRICHER = [
    StrategySnapshotEnricher,     # :40
    StandardTranslateEnricher,    # :41
    MonitorTranslateEnricher,     # :42
    DimensionOrderEnricher,       # :43
    AssignInfoEnricher,           # :44
    KubernetesCMDBEnricher,       # :45 ← K8s 告警处理
]
```

#### 执行工厂

| 类 | 行号 | 说明 |
|----|------|------|
| `EventEnrichFactory` | :49 | 执行事件级 Enricher 流水线 |
| `AlertEnrichFactory` | :61 | 执行告警级 Enricher 流水线 |

#### 基类 — `alarm_backends/service/alert/enricher/base.py`

| 类 | 行号 | 说明 |
|----|------|------|
| `BaseEventEnricher` | :20 | 事件级 Enricher 基类，子类重写 `enrich_event()` |
| `BaseAlertEnricher` | :51 | 告警级 Enricher 基类，子类重写 `enrich_alert()`（仅对新告警生效 :59） |

#### 传统主机 Enricher — `alarm_backends/service/alert/enricher/cmdb.py`

| 内容 | 行号 | 说明 |
|------|------|------|
| `class CMDBEnricher(BaseEventEnricher)` | :28 | 继承 BaseEventEnricher |
| `enrich_host(self, event)` | :108 | 解析 event.target 获取主机信息 |
| `event.set("bk_host_id", ...)` | :180 | **写入 event.bk_host_id** ✅ |
| `event.set("ip", host.bk_host_innerip)` | :181 | **写入 event.ip** ✅ |
| `event.set("bk_cloud_id", host.bk_cloud_id)` | :183 | **写入 event.bk_cloud_id** ✅ |

#### K8s Enricher — `alarm_backends/service/alert/enricher/kubernetes_cmdb.py`

| 内容 | 行号 | 说明 |
|------|------|------|
| `class KubernetesCMDBEnricher(BaseAlertEnricher)` | :30 | 继承 BaseAlertEnricher |
| `enrich_alert(self, alert)` | :227 | 入口：尝试匹配 K8s 告警到主机 |
| `enrich_host(self, alert, host)` | :263 | 将主机信息写入 alert.dimensions |
| `"ip": host.bk_host_innerip` | :274-275 | 构建 ip 维度字典 |
| `"bk_cloud_id": host.bk_cloud_id` | :280-281 | 构建 bk_cloud_id 维度字典 |
| `alert.update_key_value_field("dimensions", dimensions)` | :303 | **写入 alert.dimensions** ⚠️（不是 event.ip） |
| `alert.update_key_value_field("assign_tags", dimensions)` | :305 | 同步到 assign_tags |

---

## 数据流对比

### 传统主机告警（正常）

```
事件产生
  → CMDBEnricher.enrich_host()                     (cmdb.py:108)
    → event.target 格式: "10.0.0.1|0"              → 解析成功
    → event.set("ip", host.bk_host_innerip)        (cmdb.py:181) ✅
    → event.set("bk_cloud_id", host.bk_cloud_id)   (cmdb.py:183) ✅
  → 告警入 ES（AlertDocument.event.ip 有值）
  → get_host_alarm_count()                          (cmdb.py:449)
    → ip = alert.event.ip                           (cmdb.py:469) ✅ 有值
    → 匹配成功 → 计数+1
```

### K8s 告警（异常）

```
事件产生
  → CMDBEnricher.enrich_host()                     (cmdb.py:108)
    → event.target 格式非 "ip|cloud_id"            → 解析失败
    → event.ip 保持为空 ❌
  → KubernetesCMDBEnricher.enrich_host()           (kubernetes_cmdb.py:263)
    → 找到关联主机 → 但写入的是 alert.dimensions   (kubernetes_cmdb.py:303)
    → 不是 event.ip ⚠️
  → 告警入 ES（AlertDocument.event.ip 为空）
  → get_host_alarm_count()                          (cmdb.py:449)
    → ip = alert.event.ip                           (cmdb.py:469) ❌ 为空
    → except → continue → 计数为 0
```

---

## 问题根因

`get_host_alarm_count`（cmdb.py:449）**只从 `event.ip` + `event.bk_cloud_id` 匹配主机**，但 K8s 告警的主机信息被 `KubernetesCMDBEnricher` 写在 `alert.dimensions` 中而非 `event.ip` 中。

两套 Enricher 的写入字段不一致，而查询侧只覆盖了传统告警的写入方式：

| Enricher | 类型 | 写入位置 | 查询覆盖 |
|---------|------|---------|---------|
| `CMDBEnricher` | 事件级 | `event.ip` / `event.bk_cloud_id` | ✅ 已覆盖 |
| `KubernetesCMDBEnricher` | 告警级 | `alert.dimensions` | ❌ 未覆盖 |

代码中的 TODO 也提到了类似问题：
> `cmdb.py:452` — todo: 在ipv6改造后，alert需要添加bk_host_id，该函数需要额外适配

---

## 修复方案

### 选择：改查询侧（commit: c48e4a752）

修改 `get_host_alarm_count`，新增 `_resolve_host_id_from_alert` 辅助函数，支持三级优先匹配：

1. **`event.bk_host_id`** 直接匹配（最准确，同时解决了 TODO 中提到的 ipv6 适配问题）
2. **`event.ip` + `event.bk_cloud_id`** 匹配（兼容传统主机告警）
3. **`alert.dimensions`** 中提取 `bk_host_id` / `ip` + `bk_cloud_id`（覆盖 K8s 告警）

### 改动范围

| 文件 | 变更 |
|------|------|
| `packages/monitor_web/cc/resources/cmdb.py` | +60 行 / -12 行 |

### 优点

- 改动集中在 1 个文件 1 个函数，风险可控
- 对新旧告警（含历史 K8s 告警）都立即生效
- 不影响告警数据写入流程
- 同时解决了 TODO 中提到的 bk_host_id 适配问题
