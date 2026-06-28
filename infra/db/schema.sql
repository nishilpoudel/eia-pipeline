DROP TABLE IF EXISTS demand_predictions;
DROP TABLE IF EXISTS demand_actuals;

CREATE TABLE demand_actuals (
    period TIMESTAMPTZ PRIMARY KEY, 
    demand_mw INTEGER NOT NULL CHECK (demand_mw > 0),
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE demand_predictions (

    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    target_period TIMESTAMPTZ NOT NULL, 
    predicted_value REAL NOT NULL CHECK (predicted_value > 0),
    model_version TEXT NOT NULL,
    forecast_date DATE NOT NULL, 
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (target_period, forecast_date, model_version) 

); 
CREATE INDEX idx_predictions_forecast_date ON demand_predictions(forecast_date);