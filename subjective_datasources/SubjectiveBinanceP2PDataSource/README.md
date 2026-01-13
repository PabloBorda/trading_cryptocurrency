# SubjectiveBinanceP2PDataSource

Subjective datasource implementation for SubjectiveBinanceP2PDataSource.

## Usage

```python
from subjective_datasources.SubjectiveBinanceP2PDataSource import SubjectiveBinanceP2PDataSource

source = SubjectiveBinanceP2PDataSource(params={})
source.fetch()
```

## Parameters

Use the params dictionary when constructing the datasource to provide connection and runtime values.
Refer to get_connection_data() for required fields.
