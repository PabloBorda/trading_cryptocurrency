# SubjectivePerformanceMetricsDataSource

Subjective datasource implementation for SubjectivePerformanceMetricsDataSource.

## Usage

```python
from subjective_datasources.SubjectiveBinancePerformanceMetricsDataSource import SubjectivePerformanceMetricsDataSource

source = SubjectivePerformanceMetricsDataSource(params={})
source.fetch()
```

## Parameters

Use the params dictionary when constructing the datasource to provide connection and runtime values.
Refer to get_connection_data() for required fields.
