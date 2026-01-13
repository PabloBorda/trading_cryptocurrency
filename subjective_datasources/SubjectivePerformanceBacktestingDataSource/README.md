# SubjectivePerformanceBacktestingDataSource

Subjective datasource implementation for SubjectivePerformanceBacktestingDataSource.

## Usage

```python
from subjective_datasources.SubjectivePerformanceBacktestingDataSource import SubjectivePerformanceBacktestingDataSource

source = SubjectivePerformanceBacktestingDataSource(params={})
source.fetch()
```

## Parameters

Use the params dictionary when constructing the datasource to provide connection and runtime values.
Refer to get_connection_data() for required fields.
