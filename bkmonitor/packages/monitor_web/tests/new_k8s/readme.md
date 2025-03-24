# 单测使用说明

## pytest 执行单元测试的方法

### run test

```bash
pytest alarm_backends/tests/service/detect
```

## TODO

- [x] 需要检查 TestFilter 是否需要添加对新增容器场景的过滤

- [x] TestGetScenarioMetric
  - [x] performance
  - [x] network

- [x] TestListBCSCluster
- [x] TestScenarioMetricList
- [ ] TestListK8sResource
- [ ] TestGetResourceDetail
- [ ] TestWorkloadOverview
- [ ] TestResourceTrend
