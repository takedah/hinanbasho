DROP TABLE IF EXISTS evacuation_sites;
CREATE TABLE evacuation_sites(
  id SERIAL NOT NULL,
  site_id integer NOT NULL PRIMARY KEY,
  site_name TEXT NOT NULL,
  postal_code VARCHAR(8),
  address TEXT,
  phone_number VARCHAR(16),
  latitude decimal NOT NULL,
  longitude decimal NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL
);
CREATE INDEX ON evacuation_sites (site_id);
