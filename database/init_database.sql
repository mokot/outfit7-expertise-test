-- Create a currency_usd table if it doesn't exist
CREATE TABLE IF NOT EXISTS "currency_usd" (
  currency_usd_id SERIAL NOT NULL PRIMARY KEY,
  currency_usd_name VARCHAR(3) NOT NULL UNIQUE,
  currency_usd_value DECIMAL(10, 6) NOT NULL,
  currency_usd_created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  currency_usd_updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create a ad_network table if it doesn't exist
CREATE TABLE IF NOT EXISTS "ad_network" (
  ad_network_id SERIAL NOT NULL PRIMARY KEY,
  ad_network_name VARCHAR(63) NOT NULL UNIQUE,
  ad_network_url VARCHAR(255) NOT NULL,
  ad_network_date_format VARCHAR(15) NOT NULL,
  ad_network_created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  ad_network_updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create a daily report table if it doesn't exist
CREATE TABLE IF NOT EXISTS "daily_report" (
  report_id SERIAL NOT NULL PRIMARY KEY,
  report_date DATE NOT NULL,
  report_app VARCHAR(255) NOT NULL,
  report_platform VARCHAR(63) NOT NULL,
  report_requests INT NOT NULL,
  report_impressions INT NOT NULL,
  report_revenue DECIMAL(10, 2) NOT NULL,
  report_created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  report_updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  currency_usd_id INT REFERENCES currency_usd(currency_usd_id) ON DELETE
  SET
    NULL,
    ad_network_id INT REFERENCES ad_network(ad_network_id) ON DELETE
  SET
    NULL
);