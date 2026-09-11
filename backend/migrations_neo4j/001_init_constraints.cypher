CREATE CONSTRAINT product_id_unique IF NOT EXISTS FOR (p:Product) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT channel_id_unique IF NOT EXISTS FOR (c:Channel) REQUIRE c.id IS UNIQUE;
CREATE INDEX category_name_index IF NOT EXISTS FOR (cat:Category) ON (cat.name);
CREATE INDEX trend_signal_observed_at_index IF NOT EXISTS FOR (t:TrendSignal) ON (t.observed_at);
