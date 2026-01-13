import time
from subjective_abstract_data_source_package.SubjectiveDataSource import SubjectiveDataSource
from brainboost_data_source_logger_package.BBLogger import BBLogger


class SubjectiveRealtimeTickerStreamMultipleSymbolsDataSource(SubjectiveDataSource):
    connection_type = "Socket"
    connection_fields = ["host", "port", "symbols"]
    icon_svg = "<svg width='24' height='24' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'><circle cx='12' cy='12' r='9' fill='#2d6a4f'/><path d='M7 12h10' stroke='#ffffff' stroke-width='2'/></svg>"

    def get_icon(self):
        return self.icon_svg

    def get_connection_data(self):
        return {"connection_type": self.connection_type, "fields": list(self.connection_fields)}

    def _get_param(self, key, default=None):
        return self.params.get(key, default)

    def _on_tick(self, data):
        self.update(data)
        self.increment_processed_items()

    def start(self):
        from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration

        symbols = self._get_param("symbols", [])
        if not symbols:
            raise ValueError("symbols is required for multiple symbol stream")
        self.set_total_items(0)
        self.set_processed_items(0)
        exchange = ExchangeConfiguration.get_default_exchange()
        exchange.subscribe_multiple_individual_symbols(callback=self._on_tick, symbols=symbols)

    def fetch(self):
        if self.status_callback:
            self.status_callback(self.get_name(), "stream_started")
        self.start()
        self.set_fetch_completed(True)
        BBLogger.log(f"Stream started for {self.get_name()}")
