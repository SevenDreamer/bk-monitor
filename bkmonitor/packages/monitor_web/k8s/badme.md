# Inbox 
## 思考前端网络场景会如何设计
1. 左侧k8s对象 namespace、ingress、service、pod
A: 不像性能场景，四层层级结构，这里为2层层级结构，但是多个
从model来看， Model.ingress 有多个 service (service_list) ,  Model.service 有多个 pod (pod_name_list)

2. 左下指标列表网络出入带宽、网络出入包量、网络出入丢包量
# 混沌

吃透性能场景
结合tapd 思考网络场景怎样
然后具体怎么实现

## 自身困惑的点
1. 对容器部分名词的概念不够理解
2. 为什么要设计容器监控场景

### 1. 容器监控名词概念相关的解释

### 为什么要设计容器监控场景
需要实时监控资源所有的信息情况
从性能场景看，需要关注 CPU、内存、存储和网络带宽, 即通过指标的形式进行记录
从网络场景看，需要关注 网络出入带宽、网络出入包量、网络出入丢包量

## 需要执行的点(吃透性能场景)
1. 熟悉页面每个点击操作都会触发哪些网络请求，每个请求的参数会是什么
2. 从现有代码上理透 promql 语句的组装, 收集整理所有的 promql 语句模板，把不明白地方问清楚
3. namespace +  ingress / service/pod 
4.  promql语句中的 label_replace，   * on (namespace, service) group_left(pod)  呈现的是什么效果


## 结合 TAPD 网络场景如何设计
1. 左侧k8s对象
[cluster]、namespace、ingress、service、pod
2. 左下指标列表网络出入带宽、网络出入包量、网络出入丢包量

# 前端点击反馈
## 上面聚合维度
按照 namespace, workload, pod, container， 层级关系依次为 namespace/workload/pod/container
其中 namespace 为固定维度，即promql 语句类似于   <agg_method> by (namespace) (metric_name)

核心是 /rest/v2/k8s/resources/list_resources/ 请求  resource_type

其中 namespace 为固定维度，即promql 语句类似于   <agg_method> by (workload_kind,namespace) (metric_name)


# AI -> Q&A
## Q: k8s 的 namespace、ingress、service、pod

1. Namespace（命名空间）
定义：命名空间是 Kubernetes 中的一种虚拟化机制，用于将集群中的资源进行逻辑分隔。每个命名空间可以包含不同的资源（如 Pod、Service 等），这样可以在同一物理集群中支持多个用户或项目。
用途：
隔离环境：不同项目或团队可以在不同的命名空间中工作，减少资源冲突。
资源管理：可以在命名空间级别设置资源配额、策略等。
示例：默认情况下，Kubernetes 集群会有 default、kube-system 和 kube-public 这三个命名空间。
2. Ingress（入口）
定义：Ingress 是一种 API 对象，用于管理外部访问 Kubernetes 服务的方式，通常通过 HTTP/HTTPS 协议来处理流量。
用途：
路由流量：根据请求的域名或路径将流量路由到不同的服务。
SSL/TLS 管理：可以配置 SSL/TLS 终端点以保护流量。
简化配置：通过 Ingress 资源，可以在一个地方定义多个路由规则。
示例：一个 Ingress 资源可以将 example.com 的请求路由到 service-A，而 example.com/api 的请求路由到 service-B。
3. Service（服务）
定义：Service 是一种抽象，它定义了如何访问一组 Pod。Service 可以被视为 Pod 的一个稳定的访问点。
用途：
服务发现：通过 Service 名称，其他 Pod 可以轻松地找到并访问这些 Pod。
负载均衡：Service 会自动将流量分配到其后端的 Pod 上，保证负载均衡。
服务类型：Kubernetes 支持多种服务类型，如 ClusterIP（内部访问）、NodePort（通过节点的 IP 访问）和 LoadBalancer（在云环境中提供外部负载均衡器）。
示例：一个 Service 可以选择标签为 app=backend 的 Pod，并将其流量通过 http://backend-service 访问。
4. Pod（容器组）
定义：Pod 是 Kubernetes 中最小的可调度单元，代表一个或多个容器的集合，这些容器共享同一个网络命名空间和存储卷。
用途：
运行应用：Pod 是运行应用程序的地方，可以包含单个容器或多个紧密相关的容器（如一个应用和其日志收集代理）。
共享资源：同一 Pod 内的容器可以共享网络和存储资源，有助于提高性能。
示例：一个 Pod 可以运行一个 Web 服务器和一个日志收集容器，这两个容器可以通过 localhost 通信。


## Q: ingress和service是多对多的关系？
A: 是的，Ingress 和 Service 之间的关系可以被视为多对多的关系。以下是对此关系的详细解释：

### 多对多的关系

1. **多个 Ingress 对多个 Service**：
   - 一个 Ingress 对象可以配置多个路由规则，每个规则可以指向不同的 Service。因此，一个 Ingress 可以路由不同的路径或域名到多个后端 Service。
   - 例如，一个 Ingress 可以配置如下路由：
     - `example.com/api` 路由到 `service-A`
     - `example.com/static` 路由到 `service-B`
   - 这样，一个 Ingress 可以同时处理来自不同 Service 的请求。

2. **多个 Service 对多个 Ingress**：
   - 同样，一个 Service 也可以被多个 Ingress 对象引用。不同的 Ingress 可以定义不同的路由规则来访问相同的 Service。
   - 例如，`service-A` 可以通过以下两个不同的 Ingress 被访问：
     - `example1.com` 路由到 `service-A`
     - `example2.com/api` 路由到 `service-A`

### 总结

由于 Ingress 可以指向多个 Service，而 Service 也可以被多个 Ingress 引用，因此它们之间的确存在多对多的关系。这种灵活性使得在 Kubernetes 中管理和配置 HTTP/HTTPS 流量变得更加方便和高效。通过合理配置 Ingress 和 Service，可以实现复杂的路由策略和流量管理。

## Q: namespace +  ingress / service/pod 为什么可以这么组合
在 Kubernetes 中，命名空间（Namespace）是用于将集群内的资源进行逻辑分隔的机制。通过组合命名空间与 Ingress、Service 和 Pod，Kubernetes 可以实现更好的资源管理、访问控制和组织结构。以下是为什么可以将命名空间与这些资源组合的原因：

### 1. 资源隔离

- **逻辑分隔**：命名空间提供了一种将资源分组的方式，使得不同的团队或项目可以在同一个 Kubernetes 集群中并行工作而不会相互干扰。例如，团队 A 的应用可以在 `namespace-a` 中运行，而团队 B 的应用可以在 `namespace-b` 中运行。
- **避免资源冲突**：在同一命名空间中，资源（如 Pod、Service、Ingress 等）需要具有唯一的名称，但在不同命名空间中，相同名称的资源可以共存，这样避免了名称冲突。

### 2. 访问控制

- **RBAC（基于角色的访问控制）**：Kubernetes 提供了基于命名空间的访问控制机制。通过定义角色和角色绑定，可以控制用户或服务账户在特定命名空间内的访问权限。这意味着可以为每个命名空间设置不同的访问策略。
  
### 3. 资源管理

- **资源配额**：可以在命名空间级别设置资源配额，以限制某个命名空间内可用的 CPU 和内存等资源。这对于防止某个团队或项目消耗过多资源非常有用。
  
### 4. 组合使用示例

- **Ingress**：可以在特定命名空间内创建 Ingress，对应于该命名空间中的 Service。例如，`namespace-a` 中的 Ingress 可以路由流量到 `namespace-a` 中的多个 Service。
  
- **Service**：Service 可以通过选择器（Selector）选择同一命名空间中的 Pod。这样，Service 可以将流量路由到特定命名空间中的后端 Pod。
  
- **Pod**：Pod 是 Kubernetes 中最基本的计算单元，可以在任意命名空间中创建。Pod 可以通过 Service 来暴露，允许外部流量访问。

### 结论

通过将命名空间与 Ingress、Service 和 Pod 组合使用，Kubernetes 提供了一种灵活且强大的方式来管理和隔离集群内的资源。这种组合可以使得资源的组织、管理和访问控制变得更加清晰和高效。

# 知识总结
