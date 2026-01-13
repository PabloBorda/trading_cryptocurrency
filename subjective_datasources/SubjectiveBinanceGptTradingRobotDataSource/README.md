# SubjectiveGptTradingRobotDataSource

Subjective datasource implementation for SubjectiveGptTradingRobotDataSource.

## Usage

```python
from subjective_datasources.SubjectiveBinanceGptTradingRobotDataSource import SubjectiveGptTradingRobotDataSource

source = SubjectiveGptTradingRobotDataSource(params={})
source.fetch()
```

## Parameters

Use the params dictionary when constructing the datasource to provide connection and runtime values.
Refer to get_connection_data() for required fields.
