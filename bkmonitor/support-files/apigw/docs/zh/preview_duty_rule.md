### 功能描述

保存轮值规则


#### 接口参数

| 字段             | 类型     | 必须   | 描述                              |
|----------------|--------|------|---------------------------------|
| id             | int    | 否    | 轮值规则ID（source_type为DB的时候必填）     |
| bk_biz_id      | int    | 是    | 业务ID                            |
| begin_time | string | 是    | 预览生效开始时间（日期时间格式）                |
| days           | int    | 否    | 默认生效时间开始30天                     |
| source_type    | string | 否    | 数据来源类型 `API（接口参数）` `DB（DB存储内容）` |
| config         | dict   | 否    | 数据来源类型为API的时候必填，格式参考保存轮值规则      |


#### DB数据预览示例数据

```json
{
  "source_type": "DB",
  "id": 2,
  "begin_time": "2023-12-01 00:00:00",
  "days": 7,
  "bk_biz_id": 2
}
```

# 通过API获取
```json
{
  "source_type": "API",
  "id": 2,
  "begin_time": "2023-12-01 00:00:00",
  "days": 7,
  "bk_biz_id": 2,
  "config": {
            "name": "handoff duty",
            "bk_biz_id": 2,
            "effective_time": "2023-07-25 11:00:00",
            "end_time": "",
            "labels": ["mysql", "redis", "business"],
            "enabled": true,
            "category": "handoff",
            "duty_arranges": [
                {
            "duty_time": [{"work_type": "daily",
                           "work_days": [],
                           "work_time_type": "time_range",
                           "work_time": ["00:00--23:59"],
                           "period_settings": {
                               "window_unit": "day",
                               "duration": 2
                           }
                           }],
            "duty_users": [
                [
                    {
                        "id": "admin",
                        "type": "user"
                    },
                    {
                        "id": "admin1",
                        "type": "user"
                    },
                    {
                        "id": "admin2",
                        "type": "user"
                    }, {
                    "id": "admin3",
                    "type": "user"
                }, {
                    "id": "admin4",
                    "type": "user"
                }, {
                    "id": "admin5",
                    "type": "user"
                }
                ]
            ],
            "group_type": "auto",
            "group_number": 2,
            "backups": []
        }
            ]
        }
}
```

### 响应参数

| 字段         | 类型           | 描述        |
|------------|--------------|-----------|
| result     | bool         | 请求是否成功    |
| code       | int          | 返回的状态码    |
| message    | string       | 描述信息      |
| data       | list[object] | 预览数据      |
| request_id | str          | ESB记录请求ID |

#### data 格式说明： 
| 字段    | 类型         | 描述 |
|-------|------------|--|
| users | list[user] | 值班用户，格式参考用户 |
| work_times | list[work_time]       | 值班时间 |


#### work_time 格式说明：
| 字段    | 类型         | 描述 |
|-------|------------|--|
| start_time | string | 时间格式 `2023-12-01 00:00`|
| end_time | string | 时间格式 `2023-12-01 23:59`|



