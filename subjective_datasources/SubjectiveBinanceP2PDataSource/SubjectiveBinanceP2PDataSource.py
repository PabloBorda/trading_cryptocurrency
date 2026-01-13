import time
from subjective_abstract_data_source_package.SubjectiveDataSource import SubjectiveDataSource
from brainboost_data_source_logger_package.BBLogger import BBLogger


class SubjectiveBinanceP2PDataSource(SubjectiveDataSource):
    connection_type = "BinanceP2P"
    connection_fields = ["fiat", "asset", "trade_type", "pay_types", "amount", "sort_by"]
    icon_svg = "<svg width='24' height='24' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'><circle cx='12' cy='12' r='9' fill='#2d6a4f'/><path d='M7 12h10' stroke='#ffffff' stroke-width='2'/></svg>"

    def get_icon(self):
        return self.icon_svg

    def get_connection_data(self):
        return {"connection_type": self.connection_type, "fields": list(self.connection_fields)}

    def _get_param(self, key, default=None):
        return self.params.get(key, default)

    def _emit_result(self, result):
        if result is None:
            self.set_total_items(0)
            self.set_processed_items(0)
            return
        if isinstance(result, (list, tuple)):
            self.set_total_items(len(result))
            self.set_processed_items(0)
            for item in result:
                self.update(item)
                self.increment_processed_items()
            return
        self.set_total_items(1)
        self.set_processed_items(0)
        self.update(result)
        self.increment_processed_items()

    def fetch(self):
        start = time.perf_counter()
        if self.status_callback:
            self.status_callback(self.get_name(), "fetch_started")
        from com_goldenthinker_trade_p2p.binance_p2p import DEFAULT_BINANCE_P2P_URL, get_p2p_orders

        operation = self._get_param("trade_type", "BUY")
        asset = self._get_param("asset", "USDT")
        fiat = self._get_param("fiat", "USD")
        pay_types = self._get_param("pay_types", [])
        amount = float(self._get_param("amount", 0))
        sort_by = self._get_param("sort_by", "Price")
        binance_p2p_url = self._get_param("binance_p2p_url", DEFAULT_BINANCE_P2P_URL)
        orders = get_p2p_orders(
            binance_p2p_url=binance_p2p_url,
            operation=operation,
            asset=asset,
            fiat_currency=fiat,
            payment_methods=pay_types,
            amount=amount,
            sort_by=sort_by,
        )
        self._emit_result({"operation": operation, "asset": asset, "fiat": fiat, "orders": orders})
        duration = time.perf_counter() - start
        self.set_total_processing_time(duration)
        self.set_fetch_completed(True)
        if self.progress_callback:
            self.progress_callback(self.get_name(), self.get_total_to_process(), self.get_total_processed(), self.estimated_remaining_time())
        if self.status_callback:
            self.status_callback(self.get_name(), "fetch_completed")
        BBLogger.log(f"Fetch completed for {self.get_name()}")
