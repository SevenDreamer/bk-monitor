### 功能描述

重试部分实例或主机


#### 接口参数

| 字段        | 类型 | 必选 | 描述             |
| ----------- | ---- | ---- | ---------------- |
| bk_biz_id   | int  | 是   | 业务 ID          |
| id          | int  | 是   | 采集配置ID       |
| instance_id | int  | 是   | 需要重试的实例id |



#### 请求示例

```json
{
  "bk_bix_id": 2,
  "id": 100,
  "instance_id": 101
}
```

### 响应参数

| 字段    | 类型 | 描述         |
| ------- | ---- | ------------ |
| resul   | bool | 请求是否成功 |
| code    | int  | 返回的状态码 |
| message | str  | 描述信息     |
| data    | str  | 响应结果     |



#### 响应示例

```json
{
  "result": true,
  "code": 200,
  "message": "OK",
   "data":"success"
}
```

